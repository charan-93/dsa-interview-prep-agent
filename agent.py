"""
DSA Interview Prep Agent - Multi-Agent System for Personalized Interview Preparation
Kaggle Agents Intensive Capstone Project - Concierge Track

This agent system helps CS students prepare for technical interviews by:
1. Generating custom DSA problems based on user's skill level and topics
2. Evaluating submitted solutions with detailed feedback
3. Tracking progress and recommending next study topics
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from google import genai
from google.genai.types import Tool, FunctionDeclaration

# Configure logging for observability
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

class ProgressTracker:
    """Manages user progress, session state, and memory"""
    
    def __init__(self):
        self.user_data = {
            'problems_solved': [],
            'topics_covered': set(),
            'weak_areas': [],
            'streak_days': 0,
            'total_problems': 0,
            'last_session': None
        }
        logger.info("ProgressTracker initialized")
    
    def update_progress(self, problem_id: str, topic: str, difficulty: str, solved: bool):
        """Update user's progress after attempting a problem"""
        logger.info(f"Updating progress: {topic} - {difficulty} - Solved: {solved}")
        
        self.user_data['problems_solved'].append({
            'id': problem_id,
            'topic': topic,
            'difficulty': difficulty,
            'solved': solved,
            'timestamp': datetime.now().isoformat()
        })
        
        self.user_data['topics_covered'].add(topic)
        self.user_data['total_problems'] += 1
        
        if not solved:
            if topic not in self.user_data['weak_areas']:
                self.user_data['weak_areas'].append(topic)
        
        return self.get_progress_summary()
    
    def get_progress_summary(self) -> Dict:
        """Get current progress summary"""
        solved_count = sum(1 for p in self.user_data['problems_solved'] if p['solved'])
        accuracy = (solved_count / self.user_data['total_problems'] * 100) if self.user_data['total_problems'] > 0 else 0
        
        return {
            'total_problems': self.user_data['total_problems'],
            'problems_solved': solved_count,
            'accuracy': round(accuracy, 2),
            'topics_covered': list(self.user_data['topics_covered']),
            'weak_areas': self.user_data['weak_areas']
        }
    
    def recommend_next_topic(self) -> str:
        """Recommend next topic based on weak areas and coverage"""
        all_topics = ['Arrays', 'Linked Lists', 'Trees', 'Graphs', 'Dynamic Programming', 
                     'Backtracking', 'Greedy', 'Sorting', 'Searching', 'Strings']
        
        # Prioritize weak areas
        if self.user_data['weak_areas']:
            return self.user_data['weak_areas'][0]
        
        # Return uncovered topics
        uncovered = [t for t in all_topics if t not in self.user_data['topics_covered']]
        return uncovered[0] if uncovered else all_topics[0]

class ProblemGeneratorAgent:
    """Agent responsible for generating custom DSA problems"""
    
    def __init__(self, client):
        self.client = client
        self.model = 'gemini-2.0-flash-exp'
        logger.info("ProblemGeneratorAgent initialized")
    
    def generate_problem(self, topic: str, difficulty: str, user_level: str) -> Dict:
        """Generate a custom DSA problem"""
        logger.info(f"Generating problem: {topic} - {difficulty} - Level: {user_level}")
        
        prompt = f"""You are an expert DSA problem creator for technical interviews.
        
        Create a {difficulty} level {topic} problem suitable for a {user_level} programmer preparing for technical interviews.
        
        Provide:
        1. Problem Title
        2. Problem Description (clear and concise)
        3. Input Format
        4. Output Format
        5. Constraints
        6. Sample Test Cases (2-3 examples with explanations)
        7. Hints (2-3 hints without giving away the solution)
        
        Format the response as JSON with keys: title, description, input_format, output_format, constraints, test_cases, hints
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse response
            problem_text = response.text
            
            # Create problem object
            problem = {
                'id': f"{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'topic': topic,
                'difficulty': difficulty,
                'content': problem_text,
                'generated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Problem generated successfully: {problem['id']}")
            return problem
            
        except Exception as e:
            logger.error(f"Error generating problem: {str(e)}")
            return {'error': str(e)}

class SolutionEvaluatorAgent:
    """Agent responsible for evaluating user solutions"""
    
    def __init__(self, client):
        self.client = client
        self.model = 'gemini-2.0-flash-exp'
        logger.info("SolutionEvaluatorAgent initialized")
    
    def evaluate_solution(self, problem: Dict, solution_code: str, language: str) -> Dict:
        """Evaluate submitted solution"""
        logger.info(f"Evaluating solution for problem: {problem.get('id', 'unknown')}")
        
        prompt = f"""You are an expert code reviewer for technical interviews.
        
        Problem:
        {problem.get('content', '')}
        
        Submitted Solution ({language}):
        ```{language}
        {solution_code}
        ```
        
        Evaluate the solution and provide:
        1. Correctness (Does it solve the problem?)
        2. Time Complexity
        3. Space Complexity
        4. Code Quality (readability, style)
        5. Edge Cases Handled
        6. Suggestions for Improvement
        7. Overall Score (0-100)
        
        Format as JSON with keys: correctness, time_complexity, space_complexity, code_quality, edge_cases, suggestions, score
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            evaluation = {
                'problem_id': problem.get('id'),
                'feedback': response.text,
                'evaluated_at': datetime.now().isoformat()
            }
            
            logger.info(f"Solution evaluated successfully")
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating solution: {str(e)}")
            return {'error': str(e)}

class DSAInterviewPrepAgent:
    """Main coordinator agent - manages the multi-agent workflow"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        
        # Initialize sub-agents
        self.problem_generator = ProblemGeneratorAgent(self.client)
        self.solution_evaluator = SolutionEvaluatorAgent(self.client)
        self.progress_tracker = ProgressTracker()
        
        logger.info("DSAInterviewPrepAgent initialized with all sub-agents")
    
    def start_session(self, user_level: str = 'intermediate') -> Dict:
        """Start a new practice session"""
        logger.info(f"Starting new session for {user_level} user")
        
        # Get recommended topic
        topic = self.progress_tracker.recommend_next_topic()
        
        # Generate problem
        problem = self.problem_generator.generate_problem(
            topic=topic,
            difficulty='Medium',
            user_level=user_level
        )
        
        return {
            'status': 'session_started',
            'problem': problem,
            'progress': self.progress_tracker.get_progress_summary()
        }
    
    def submit_solution(self, problem_id: str, solution_code: str, language: str = 'python') -> Dict:
        """Submit solution for evaluation"""
        logger.info(f"Solution submitted for problem: {problem_id}")
        
        # Find problem in history
        problem = {'id': problem_id, 'content': 'Problem content placeholder'}
        
        # Evaluate solution
        evaluation = self.solution_evaluator.evaluate_solution(
            problem=problem,
            solution_code=solution_code,
            language=language
        )
        
        # Update progress (mock - in real implementation, parse evaluation score)
        solved = True  # Would be determined from evaluation
        self.progress_tracker.update_progress(
            problem_id=problem_id,
            topic='Dynamic Programming',  # Would be from problem
            difficulty='Medium',
            solved=solved
        )
        
        return {
            'status': 'solution_evaluated',
            'evaluation': evaluation,
            'progress': self.progress_tracker.get_progress_summary()
        }
    
    def get_study_plan(self) -> Dict:
        """Get personalized study plan based on progress"""
        logger.info("Generating study plan")
        
        progress = self.progress_tracker.get_progress_summary()
        next_topic = self.progress_tracker.recommend_next_topic()
        
        return {
            'current_progress': progress,
            'recommended_topic': next_topic,
            'weak_areas': progress['weak_areas'],
            'suggestions': self._generate_study_suggestions(progress)
        }
    
    def _generate_study_suggestions(self, progress: Dict) -> List[str]:
        """Generate study suggestions"""
        suggestions = []
        
        if progress['total_problems'] < 10:
            suggestions.append("Build consistency by solving at least 2 problems daily")
        
        if progress['accuracy'] < 50:
            suggestions.append("Focus on understanding concepts before attempting more problems")
        
        if progress['weak_areas']:
            suggestions.append(f"Review {progress['weak_areas'][0]} fundamentals")
        
        return suggestions

# Example usage
if __name__ == "__main__":
    # Initialize the main agent
    api_key = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
    agent = DSAInterviewPrepAgent(api_key)
    
    # Start a session
    session = agent.start_session(user_level='intermediate')
    print(json.dumps(session, indent=2))
    
    # Get study plan
    study_plan = agent.get_study_plan()
    print(json.dumps(study_plan, indent=2))
