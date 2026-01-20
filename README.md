# 🏋️ RAG-Based AI Fitness & Diet Planner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-orange.svg)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

### ⚡ Production-Ready AI Fitness & Diet Planning Platform

An intelligent, full-stack application that generates **personalized workout and diet plans** using **Retrieval-Augmented Generation (RAG)** technology. Say goodbye to generic advice—every recommendation is grounded in verified fitness and nutrition data.

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [🏗️ Architecture](#-architecture) • [📚 API](#-api-documentation) • [🧠 RAG Pipeline](#-rag-pipeline)

</div>

---

## 📋 Quick Navigation

<table>
<tr>
<td align="center" width="25%">

### [📖 Overview](#-overview)

Getting started guide

</td>
<td align="center" width="25%">

### [⚙️ Installation](#-installation)

Setup in 5 minutes

</td>
<td align="center" width="25%">

### [🎯 Usage](#-usage)

Run and deploy

</td>
<td align="center" width="25%">

### [📚 Documentation](#-api-documentation)

Full API reference

</td>
</tr>
</table>

---

## 🎯 Overview

**The Problem:** Traditional fitness apps give generic advice. AI chatbots can hallucinate exercises and diets.

**The Solution:** This application uses **Retrieval-Augmented Generation (RAG)** to ground all recommendations in verified, evidence-based fitness and nutrition data. Every suggestion is backed by real information from your knowledge base.

### Why RAG? 🤔

```
Traditional LLM:
User Query → Black Box → Plausible-sounding (but possibly wrong) Response ❌

Our RAG System:
User Query → Embed → Search Knowledge Base → Retrieve Verified Data →
Generate Response with Context → Evidence-Based Recommendation ✅
```

**Key Benefits:**

- ✅ No hallucinations—all data is verified
- ✅ Transparent citations—users see where recommendations come from
- ✅ Culturally aware—extensive Indian diet support
- ✅ Safety first—no medical misinformation
- ✅ Adaptive—improves based on user progress

---

## ✨ Features

### 🎯 Core Capabilities

| Feature                   | Description                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| 📋 **Goal-Based Plans**   | Customized for muscle gain, fat loss, or lean muscle goals            |
| 🏋️ **Smart Workouts**     | AI-generated routines based on experience level, equipment & schedule |
| 🥗 **Diet Plans**         | Culturally-aware meals (Indian veg/non-veg, vegan, keto, balanced)    |
| 📊 **Calorie Calculator** | Automatic BMR, TDEE & macro calculations                              |
| 📈 **Progress Tracking**  | Log weight, measurements, workouts & calories                         |
| 📉 **Visual Analytics**   | Interactive charts and progress insights                              |

### 🚀 Advanced Features

| Feature                    | Description                                    |
| -------------------------- | ---------------------------------------------- |
| 🤖 **RAG-Powered AI**      | Responses grounded in verified fitness science |
| 🔄 **Adaptive Planning**   | Regenerate plans based on actual progress data |
| 📚 **Source Citations**    | See exactly where recommendations come from    |
| 🛡️ **Medical Safety**      | Never gives medical advice—educates instead    |
| 🇮🇳 **Indian Diet Support** | Extensive vegetarian & non-vegetarian options  |
| 🔐 **Secure Profiles**     | User data protection & privacy controls        |

---

## 🛠️ Tech Stack

### Backend

- **FastAPI** — Modern, fast web framework
- **SQLAlchemy** — SQL toolkit & ORM
- **Pydantic** — Data validation & typing
- **SQLite** — Lightweight user database

### AI/ML Layer

- **LangChain** — LLM application framework
- **Google Gemini** — Large language model
- **Pinecone** — Vector database for semantic search
- **HuggingFace** — Embeddings (fallback)

### Frontend

- **Streamlit** — Web app framework
- **Plotly** — Interactive charts
- **Pandas** — Data analysis

---

## 🏗️ Architecture

### System Design

```
┌────────────────────────────────────────────────────────────┐
│              STREAMLIT FRONTEND                             │
│  ┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │
│  │  Home   │ │Profile │ │Workout │ │ Diet  │ │Progress │   │
│  └─────────┘ └────────┘ └────────┘ └────────┘ └────────┘   │
└────────────┬─────────────────────────────────────────────────┘
             │ REST API
             ▼
┌────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND                                │
│  Routes: Users | Plans | Progress | Health | RAG          │
│  Services: User | Plan | Progress | Calorie             │
└────────────┬─────────────────────────────────────────────────┘
             │
    ┌────────┼────────┬────────────────────┐
    ▼        ▼        ▼                    ▼
  ┌──────┐ ┌────┐ ┌────────────────────────────────┐
  │SQLite│ │ RAG Pipeline                        │
  │ DB   │ │  ┌──────────────┐                  │
  └──────┘ │  │ Embeddings   │                  │
           │  │ (Gemini)     │                  │
           │  └──────────────┘                  │
           │  ┌──────────────┐ ┌─────────────┐ │
           │  │ Retriever    │◄│ Pinecone DB │ │
           │  │ (Semantic)   │ │ (Vectors)   │ │
           │  └──────────────┘ └─────────────┘ │
           │  ┌──────────────┐                  │
           │  │ Gemini LLM   │                  │
           │  │ (Generation) │                  │
           │  └──────────────┘                  │
           └────────────────────────────────────┘
```

### Data Flow

**User Request Path:**

```
User Query
    ↓
Embed Query (Gemini Embeddings)
    ↓
Search Pinecone Vector DB
    ↓
Retrieve Top-K Relevant Documents
    ↓
Augment Prompt with Context + User Profile
    ↓
Generate Response (Gemini LLM)
    ↓
Return Evidence-Based Recommendation with Sources
```

---

## � Quick Start

### Prerequisites

- Python 3.9+
- Git
- API Keys: Google Gemini, Pinecone

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/fitness-diet-rag-planner.git
cd fitness-diet-rag-planner

# 2. Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with API keys
cp .env.example .env
# Edit .env with your API keys

# 5. Initialize database
python scripts/generate_sample_data.py
python scripts/ingest_data.py

# 6. Start backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# 7. Start frontend (Terminal 2)
streamlit run frontend/app.py

# Open http://localhost:8501 in browser
```

### Environment Setup

Create a `.env` file in the project root:

```env
# Application
APP_NAME="AI Fitness & Diet Planner"
APP_VERSION="1.0.0"
DEBUG=true

# API
API_HOST=0.0.0.0
API_PORT=8000
API_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./fitness_planner.db

# Pinecone Vector Database
PINECONE_API_KEY=your-api-key-here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=fitness-diet-planner

# Google Gemini
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Security
SECRET_KEY=your-secret-key-here
```

### Getting API Keys

#### Google Gemini API

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Sign in with Google account
3. Click "Create API Key" → Copy

#### Pinecone API Key

1. Go to [Pinecone](https://pinecone.io)
2. Sign up (free tier available)
3. Navigate to API Keys in dashboard
4. Copy key and environment

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/fitness-diet-rag-planner.git
cd fitness-diet-rag-planner
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root with your API keys (see Environment Setup above).

### Step 5: Initialize Data (Optional)

```bash
# Generate sample data
python scripts/generate_sample_data.py

# Ingest data into Pinecone
python scripts/ingest_data.py
```

---

## 🎯 Usage

### Running the Application

**Terminal 1 - Start Backend API**

```bash
cd fitness-diet-rag-planner
uvicorn backend.main:app --reload --port 8000
```

**Available at:**

- API: http://localhost:8000
- Interactive Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

**Terminal 2 - Start Frontend**

```bash
streamlit run frontend/app.py
```

**Open at:** http://localhost:8501

### User Workflow

1. **Create Profile** → Enter health stats, goals, preferences
2. **Generate Plans** → Get AI-powered workout & diet plans
3. **Log Progress** → Track weight, workouts, meals
4. **View Analytics** → See charts and progress trends
5. **Regenerate** → Update plans based on progress

### Example API Request

```bash
# Create a user profile
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Johnson",
    "email": "alex@example.com",
    "age": 28,
    "gender": "male",
    "height_cm": 180,
    "weight_kg": 75,
    "fitness_goal": "muscle_gain",
    "activity_level": "moderately_active",
    "dietary_preference": "indian_veg",
    "experience_level": "intermediate",
    "workout_location": "gym",
    "workout_days_per_week": 4
  }'
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints Overview

#### 🏥 Health Check

```
GET  /health              → App status
GET  /health/db           → Database connection
GET  /health/vectorstore  → Pinecone connection
```

#### 👤 User Management

```
POST   /users/                   → Create profile
GET    /users/{user_id}          → Retrieve user
GET    /users/email/{email}      → Find by email
PUT    /users/{user_id}          → Update profile
DELETE /users/{user_id}          → Delete user
GET    /users/{user_id}/stats    → Get computed stats
```

#### 📋 Plan Generation

```
POST /plans/generate              → Generate workout + diet
POST /plans/{user_id}/workout     → Generate workout only
POST /plans/{user_id}/diet        → Generate diet only
GET  /plans/{user_id}/active      → Retrieve active plans
POST /plans/{user_id}/regenerate/{type} → Update based on progress
```

#### 📈 Progress Tracking

```
POST /progress/{user_id}/weight    → Log weight
POST /progress/{user_id}/calories  → Log daily intake
POST /progress/{user_id}/workout   → Log workout
GET  /progress/{user_id}/summary   → Get progress summary
GET  /progress/{user_id}/charts    → Get chart data
```

#### 🤖 RAG Operations

```
POST /rag/query           → Query RAG system
POST /rag/ingest          → Ingest single document
POST /rag/ingest/bulk     → Bulk ingest from directory
GET  /rag/stats           → Vector DB statistics
```

### API Response Format

All responses follow a consistent format:

```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed",
  "timestamp": "2026-01-20T10:30:00Z"
}
```

---

## 🧠 RAG Pipeline Deep Dive

### Phase 1: Data Ingestion

```
Raw Data (JSON)
    ↓
Document Loader
    ↓
Text Splitter (Chunking)
    ↓
Embedding Generation (Gemini)
    ↓
Vector Storage (Pinecone)
```

**Process:**

1. Load fitness/diet data from JSON files
2. Split into manageable chunks
3. Generate embeddings using Gemini
4. Store vectors with metadata in Pinecone
5. Index for fast semantic search

### Phase 2: Query Processing

```
User Query + Profile Context
    ↓
Enhanced Query Embedding
    ↓
Pinecone Similarity Search
    ↓
Retrieve Top-K Documents
```

### Phase 3: Response Generation

```
Retrieved Documents
    ↓
Augment Prompt
    ↓
Add User Profile Data
    ↓
Generate with Gemini LLM
    ↓
Format with Citations
```

### Prompt Engineering Strategy

The system uses carefully crafted prompts that:

✅ **Ground in Context** — ONLY use retrieved documents  
✅ **Prevent Hallucination** — Explicit constraints  
✅ **Safety First** — Medical disclaimer enforcement  
✅ **Ask for Clarity** — Request missing information  
✅ **Cite Sources** — Show document references

**Example Prompt Structure:**

```
Using ONLY the fitness data and user profile provided below, generate
a personalized 4-week workout plan.

=== USER PROFILE ===
[User stats and goals]

=== RETRIEVED WORKOUTS ===
[Relevant routines from knowledge base]

=== CRITICAL RULES ===
- ONLY use information from above
- NEVER invent exercises or rep schemes
- Never provide medical advice
- Ask follow-up questions if missing info

Plan:
```

---

## 📁 Project Structure

```
fitness-diet-rag-planner/
│
├── 📄 README.md                    # Documentation
├── 📄 requirements.txt             # Dependencies
├── 📄 .env.example                 # Config template
│
├── 📁 backend/                     # FastAPI Backend
│   ├── 📄 main.py                  # App entry point
│   ├── 📄 config.py                # Configuration
│   │
│   ├── 📁 api/
│   │   ├── 📁 routes/
│   │   │   ├── health.py           # Health checks
│   │   │   ├── users.py            # User endpoints
│   │   │   ├── plans.py            # Plan generation
│   │   │   ├── progress.py         # Tracking endpoints
│   │   │   └── rag.py              # RAG endpoints
│   │   └── 📁 dependencies/
│   │       └── auth.py             # Auth middleware
│   │
│   ├── 📁 models/                  # Pydantic models
│   │   ├── user.py
│   │   ├── plan.py
│   │   ├── progress.py
│   │   ├── rag.py
│   │   └── responses.py
│   │
│   ├── 📁 database/                # Database layer
│   │   ├── connection.py           # DB setup
│   │   ├── models.py               # SQLAlchemy ORM
│   │   └── crud.py                 # CRUD operations
│   │
│   ├── 📁 services/                # Business logic
│   │   ├── user_service.py
│   │   ├── plan_service.py
│   │   ├── progress_service.py
│   │   └── calorie_service.py
│   │
│   ├── 📁 rag/                     # RAG System
│   │   ├── embeddings.py           # Embedding gen
│   │   ├── vectorstore.py          # Pinecone ops
│   │   ├── retriever.py            # Semantic search
│   │   ├── chain.py                # RAG chain
│   │   ├── prompts.py              # Prompt templates
│   │   └── ingestion.py            # Data loading
│   │
│   └── 📁 core/
│       ├── exceptions.py
│       ├── logging_config.py
│       ├── middleware.py
│       └── security.py
│
├── 📁 frontend/                    # Streamlit App
│   ├── 📄 app.py                   # Main app
│   ├── 📄 api_client.py            # API calls
│   ├── 📄 components.py            # UI widgets
│   │
│   └── 📁 pages/
│       ├── 1_🏠_Home.py
│       ├── 2_👤_Profile.py
│       ├── 3_🏋️_Workout_Plan.py
│       ├── 4_🥗_Diet_Plan.py
│       ├── 5_📈_Progress.py
│       └── 6_📊_Analytics.py
│
├── 📁 data/                        # Knowledge Base
│   └── 📁 raw/
│       ├── 📁 workouts/
│       │   ├── strength_training.json
│       │   ├── home_workouts.json
│       │   └── ...
│       └── 📁 diets/
│           ├── indian_veg.json
│           ├── indian_nonveg.json
│           └── ...
│
├── 📁 scripts/                     # Utilities
│   ├── generate_sample_data.py     # Create test data
│   ├── ingest_data.py              # Load to Pinecone
│   └── setup_pinecone.py           # Configure Pinecone
│
└── 📁 tests/                       # Test Suite
    ├── conftest.py
    ├── 📁 unit/
    └── 📁 integration/
```

---

## 🔧 Configuration

### Application Settings

Edit `backend/config.py` to customize:

- **Debug Mode** — Enable development features
- **Database URL** — SQLite or PostgreSQL
- **API Settings** — Host, port, base path
- **RAG Settings** — Chunk size, top-K results
- **Security** — Secret key, CORS settings

### Logging

Configure logging in `backend/core/logging_config.py`:

- Log level (DEBUG, INFO, WARNING, ERROR)
- Output format and style
- File rotation policies

---

## 🧪 Development

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_users.py

# With coverage
pytest --cov=backend tests/
```

### Code Quality

```bash
# Linting
flake8 backend/

# Type checking
mypy backend/

# Code formatting
black backend/
```

---

## 🚨 Troubleshooting

### Common Issues

| Issue                         | Solution                                |
| ----------------------------- | --------------------------------------- |
| **Pinecone Connection Error** | Check API key, environment, and network |
| **Gemini API Rate Limited**   | Implement backoff, upgrade API plan     |
| **Embeddings Empty**          | Run `python scripts/ingest_data.py`     |
| **Database Locked**           | Remove SQLite lock files, restart       |
| **Streamlit Won't Connect**   | Verify backend running on port 8000     |

### Debug Mode

Enable debug logging:

```bash
# Terminal
export DEBUG=true
uvicorn backend.main:app --reload

# Or in .env
DEBUG=true
```

---

## 📊 Performance Tips

1. **Batch Requests** — Use bulk ingest for better performance
2. **Cache Results** — Frontend caches API responses
3. **Optimize Chunks** — Adjust chunk size in config
4. **Index Tuning** — Fine-tune Pinecone index settings
5. **Database** — Use PostgreSQL for production

---

## 🤝 Contributing

We love contributions! Here's how to help:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

**Before submitting:**

- ✅ Run tests: `pytest`
- ✅ Check lint: `flake8 backend/`
- ✅ Format code: `black backend/`
- ✅ Update docs if needed

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) file for details.

---

## 📞 Support

- 📖 **Documentation** — See [High-Level System Architecture.txt](High-Level%20System%20Architecture.txt)
- 🐛 **Issues** — Report on GitHub Issues
- 💬 **Discussions** — Join our GitHub Discussions
- 📧 **Email** — Contact project maintainers

---

## 🎉 Acknowledgments

- **Google Gemini** for powerful LLM capabilities
- **Pinecone** for vector database infrastructure
- **LangChain** for RAG framework
- **FastAPI** for backend framework
- **Streamlit** for frontend framework

---

<div align="center">

**Made with ❤️ for fitness enthusiasts and developers**

[⬆ Back to top](#-ragbased-ai-fitness--diet-planner)

</div>
    ├── 📄 conftest.py
    ├── 📁 unit/
    └── 📁 integration/
```
