# DSA Interview Prep Agent

> **Kaggle Agents Intensive Capstone Project - Concierge Track**

AI-powered multi-agent system for personalized DSA interview preparation and coding practice, built with Google's Gemini AI.

## 📋 Problem Statement

Computer Science students preparing for technical interviews face several challenges:
- **Overwhelming Content**: Thousands of DSA problems with no clear path
- **Lack of Personalization**: Generic practice plans don't adapt to individual weak areas
- **No Feedback Loop**: Limited guidance on solution quality and improvement areas
- **Progress Tracking**: Difficulty maintaining consistent practice and measuring growth

This leads to inefficient preparation, wasted time, and increased interview anxiety.

## 💡 Solution

An intelligent multi-agent system that:
1. **Generates** custom DSA problems tailored to your skill level and focus topics
2. **Evaluates** submitted solutions with detailed feedback on correctness, complexity, and code quality
3. **Tracks** progress over time and identifies weak areas
4. **Recommends** personalized study plans based on your performance

## 🏗️ Architecture

### Multi-Agent System Design

The system follows a **Sequential Multi-Agent Pattern** with three specialized agents coordinated by a main controller:

```
┌─────────────────────────────────────────┐
│     DSAInterviewPrepAgent (Main)       │
│         (Coordinator Pattern)           │
└──────────┬──────────────────────────────┘
           │
           ├──────┬──────────┬──────────────┐
           ▼      ▼          ▼              ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │  Problem     │  │  Solution    │  │  Progress    │
    │  Generator   │──│  Evaluator   │──│  Tracker     │
    │  Agent       │  │  Agent       │  │  Agent       │
    └──────────────┘  └──────────────┘  └──────────────┘
         Uses              Uses             Manages
       Gemini 2.0         Gemini 2.0       Memory &
         Flash              Flash           State
```

### Key Components

#### 1. **ProblemGeneratorAgent**
- Generates custom DSA problems using Gemini AI
- Adapts difficulty based on user level
- Creates problems across 10+ topics (Arrays, Trees, Graphs, DP, etc.)
- Provides hints, test cases, and constraints

#### 2. **SolutionEvaluatorAgent**
- Evaluates code correctness and quality
- Analyzes time and space complexity
- Identifies edge cases and provides improvement suggestions
- Scores solutions (0-100)

#### 3. **ProgressTracker**
- Manages user session state and memory
- Tracks solved problems, topics covered, and weak areas
- Calculates accuracy metrics
- Recommends next study topics

#### 4. **DSAInterviewPrepAgent (Coordinator)**
- Orchestrates workflow between agents
- Manages session lifecycle
- Provides unified API for client interactions

## 🎯 Features Meeting ADK Requirements

This project demonstrates **4+ key concepts** from the Agents Intensive Course:

### ✅ 1. Multi-Agent System
- **Sequential workflow** with 3 specialized agents
- **Coordinator pattern** for orchestration
- **Agent delegation** - main agent delegates tasks to specialized sub-agents

### ✅ 2. Tools Integration
- **Gemini AI** (Built-in LLM tool) for problem generation and evaluation
- **Custom tools** (ProgressTracker for memory management)
- **Function calling** with structured prompts

### ✅ 3. Sessions & Memory
- **State management** using ProgressTracker
- **Long-term memory** tracking user history across sessions
- **Session data** includes problems solved, accuracy, weak areas, streaks
- **Memory-based recommendations** for personalized study plans

### ✅ 4. Observability
- **Comprehensive logging** using Python's logging module
- **Structured log messages** for all agent actions
- **Tracing** through timestamp-based operation logs
- **Metrics tracking** (accuracy, problems solved, coverage)

## 🚀 Installation & Setup

### Prerequisites
```bash
Python 3.9+
Google Gemini API Key
```

### Install Dependencies
```bash
pip install google-genai
```

### Environment Setup

#### 1. Enable Gemini API in Google Cloud Console

Before setting up your API key, you must enable the Generative Language API:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** → **Library** from the left sidebar
4. Search for "Generative Language API" or "Gemini API"
5. Click on the API and hit **Enable**
6. Go to **APIs & Services** → **Credentials** to create or verify your API key

> **Note:** Your API key must have the Generative Language API enabled. If you get "API key not valid" errors, verify that:
> - The API is enabled for your project
> - Your API key has no restrictions blocking the Generative Language API
> - You've waited a few minutes after enabling the API for changes to propagate

#### 2. Set Your API Key
```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

## 💻 Usage

### Basic Usage
```python
from agent import DSAInterviewPrepAgent
import os

# Initialize agent
api_key = os.getenv('GEMINI_API_KEY')
agent = DSAInterviewPrepAgent(api_key)

# Start a practice session
session = agent.start_session(user_level='intermediate')
print(session['problem'])  # Get generated problem

# Submit solution
evaluation = agent.submit_solution(
    problem_id=session['problem']['id'],
    solution_code="your code here",
    language='python'
)
print(evaluation['feedback'])  # Get detailed feedback

# Get personalized study plan
plan = agent.get_study_plan()
print(plan['recommended_topic'])  # Next topic to focus on
print(plan['suggestions'])  # Study recommendations
```

### Example Workflow

1. **Start Session**: Agent recommends a topic based on your progress
2. **Get Problem**: Receive a custom-generated DSA problem
3. **Solve**: Work on the problem
4. **Submit**: Send your solution for evaluation
5. **Review**: Get detailed feedback on correctness, complexity, and quality
6. **Track**: System updates your progress and weak areas
7. **Repeat**: Get next recommended topic

## 📊 Value Proposition

### Time Savings
- **10+ hours/week** saved on manual problem selection and research
- Instant feedback vs waiting for human code review

### Improved Learning
- **Personalized** problem difficulty matching your skill level
- **Targeted practice** on weak areas identified automatically
- **Comprehensive feedback** on every submission

### Better Interview Performance
- **Structured preparation** with clear progress tracking
- **Real interview scenarios** with custom problem generation
- **Confidence building** through consistent practice and improvement metrics

## 🔧 Technical Implementation

### Technologies Used
- **Google Gemini 2.0 Flash**: LLM for problem generation and code evaluation
- **Python 3.9+**: Core implementation language
- **Python Logging**: Observability and debugging
- **JSON**: Data serialization for agent communication

### Design Patterns
- **Coordinator Pattern**: Main agent delegates to specialized sub-agents
- **State Management**: Centralized progress tracking
- **Sequential Processing**: Problems → Solutions → Feedback → Progress

## 📈 Future Enhancements

- [ ] Deploy to Cloud Run for public access
- [ ] Add real code execution sandbox for testing
- [ ] Integrate with LeetCode/Codeforces APIs
- [ ] Add collaborative learning features
- [ ] Build web UI for better user experience
- [ ] Add A2A protocol for agent-to-agent communication
- [ ] Implement context compaction for long conversations

## 📝 Project Structure

```
dsa-interview-prep-agent/
├── agent.py                 # Main multi-agent implementation
├── README.md               # This file
├── .gitignore              # Python gitignore
└── requirements.txt        # Python dependencies (to be added)
```

## 🎓 Learning Outcomes

Building this project demonstrated:
- Multi-agent system architecture and coordination
- LLM integration and prompt engineering
- State management and memory persistence
- Observability and logging best practices
- Problem decomposition into specialized agents

## 📜 License

MIT License - Free to use and modify

## 🙏 Acknowledgments

- **Google Kaggle** for hosting the Agents Intensive Course
- **Gemini AI Team** for providing the excellent LLM API
- **ADK Community** for documentation and examples

## 👨‍💻 Author

**Pata Hari Sai Charan**
- GitHub: [@charan-93](https://github.com/charan-93)
- Kaggle: [@charanpata](https://www.kaggle.com/charanpata)

---

*Built with ❤️ for the Kaggle Agents Intensive Capstone Project 2025*
