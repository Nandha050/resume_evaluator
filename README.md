# 🎯 Automated Resume Relevance Check System

An AI-powered resume evaluation system designed for **Innomatics Research Labs** to automate resume evaluation against job requirements at scale, providing consistent, fast, and actionable feedback.

## 📋 Problem Statement

At Innomatics Research Labs, resume evaluation is currently **manual, inconsistent, and time-consuming**. Every week, the placement team across Hyderabad, Bangalore, Pune, and Delhi NCR receives 18–20 job requirements, with each posting attracting thousands of applications.

### Current Challenges:
- ⏰ **Delays in shortlisting candidates** due to manual review process
- 🔄 **Inconsistent judgments** as evaluators interpret role requirements differently
- 📈 **High workload for placement staff**, reducing their ability to focus on interview prep and student guidance
- 🏢 **Pressure from hiring companies** expecting fast and high-quality shortlists

## 🎯 Objectives

The Automated Resume Relevance Check System will:

✅ **Automate resume evaluation** against job requirements at scale  
✅ **Generate Relevance Score (0–100)** for each resume per job role  
✅ **Highlight gaps** such as missing skills, certifications, or projects  
✅ **Provide fit verdict** (High / Medium / Low suitability) to recruiters  
✅ **Offer personalized improvement feedback** to students  
✅ **Store evaluations** in a web-based dashboard accessible to the placement team  

## 🚀 Proposed Solution

We propose building an **AI-powered resume evaluation engine** that combines rule-based checks with LLM-based semantic understanding:

### Core Components:
- **Resume Parsing**: Extract raw text from PDF/DOCX and standardize formats
- **JD Parsing**: Extract role title, must-have skills, good-to-have skills, qualifications
- **Hybrid Scoring**: 
  - **Hard Match**: Keyword & skill check (exact and fuzzy matches)
  - **Soft Match**: Semantic fit via embeddings + LLM reasoning
- **Output Generation**: Relevance Score, Missing Elements, and Verdict
- **Web Dashboard**: Searchable interface for placement team

## 🏗️ System Architecture

### Workflow:
```
Job Description Upload → Resume Upload → Automated Parsing → Relevance Analysis → Results Storage
```

### Technical Approach:
1. **Resume Parsing**: PyMuPDF/pdfplumber for PDF, python-docx for DOCX
2. **Text Processing**: spaCy/NLTK for entity extraction and normalization
3. **Hard Matching**: TF-IDF, BM25, fuzzy matching for exact keyword matches
4. **Semantic Matching**: Sentence transformers + Google Gemini for contextual understanding
5. **Scoring Engine**: Weighted combination of hard and soft matches
6. **Web Interface**: Streamlit dashboard with role-specific workflows

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**: Primary programming language
- **FastAPI**: High-performance backend API framework
- **SQLite**: Lightweight database for development (PostgreSQL for production)
- **LangChain**: LLM workflow orchestration
- **spaCy**: Advanced NLP and entity extraction
- **PyMuPDF/pdfplumber**: PDF text extraction
- **python-docx**: DOCX file processing

### Frontend
- **Streamlit**: Interactive web dashboard
- **Plotly**: Interactive charts and visualizations
- **Pandas**: Data manipulation and analysis

### AI/ML
- **Google Gemini**: LLM for semantic matching and feedback generation
- **Sentence Transformers**: Text embeddings for semantic similarity
- **TF-IDF/BM25**: Keyword matching algorithms
- **Fuzzy Matching**: Approximate string matching
- **ChromaDB**: Vector store for embeddings

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- Google API Key (for Gemini integration)
- Git

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd code4tech
```

### Step 2: Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# For Python 3.12 users (if you encounter compatibility issues)
pip install -r requirements_python312.txt
```

### Step 3: Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### Step 4: Set Up Environment Variables
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env file and add your Google API key
# GOOGLE_API_KEY=your_api_key_here
# DEFAULT_MODEL=gemini-pro
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Step 5: Get Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### Step 6: Initialize Database
```bash
# Database tables will be created automatically on first run
python -c "from src.models.database import create_tables; create_tables()"
```

## 🚀 Usage

### Quick Start
```bash
# Start both backend and frontend servers
python start_server.py
```

This will start:
- **Backend API**: http://localhost:8000
- **Frontend Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

### Manual Start (Alternative)
```bash
# Terminal 1: Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
streamlit run dashboard.py --server.port 8501
```

## 👥 User Workflows

### 👔 Placement Officer Workflow
1. **Access Dashboard**: Click "Placement Officer" card
2. **Upload Job Description**: Upload JD file (PDF/DOCX/TXT)
3. **View Parsed Data**: System automatically extracts requirements
4. **Search & Filter Resumes**: Filter by job role, score, verdict
5. **Review Results**: View evaluation results and rankings
6. **Export Data**: Download results as CSV

### 🎓 Student Workflow
1. **Access Portal**: Click "Student" card
2. **Upload Resume**: Upload resume file (PDF/DOCX)
3. **Browse Jobs**: View available job positions
4. **Apply for Jobs**: Click "Apply for this Job"
5. **Get Instant Results**: Receive relevance score, verdict, gap analysis
6. **Download Report**: Get personalized improvement suggestions

## 📊 Features

### 🎯 Core Features
- **Automated Resume Evaluation**: Process PDF/DOCX resumes against job descriptions
- **Relevance Scoring**: Generate 0-100 relevance scores with High/Medium/Low verdicts
- **Gap Analysis**: Identify missing skills, certifications, and projects
- **Personalized Feedback**: Provide improvement suggestions to students
- **Real-time Processing**: Instant evaluation results (2-5 seconds)
- **Scalable Architecture**: Handle thousands of resumes weekly

### 📈 Dashboard Features
- **System Overview**: Statistics and performance metrics
- **Interactive Charts**: Verdict distribution and trends
- **Search & Filter**: Advanced filtering by multiple criteria
- **Export Functionality**: Download results in CSV format
- **Role-based Access**: Separate interfaces for officers and students

### 🔧 Technical Features
- **Multi-format Support**: PDF, DOCX, DOC, TXT files
- **AI-powered Analysis**: Google Gemini for semantic understanding
- **Robust Parsing**: Multiple fallback methods for text extraction
- **Error Handling**: Comprehensive error management and user feedback
- **API Documentation**: Auto-generated API docs with Swagger UI

## 📁 Project Structure

```
├── main.py                     # FastAPI backend application
├── dashboard.py                # Streamlit frontend dashboard
├── start_server.py            # Server startup script
├── requirements.txt           # Python dependencies
├── requirements_python312.txt # Python 3.12 specific dependencies
├── env_example.txt            # Environment variables template
├── setup_gemini.py            # Google API setup helper
├── test_core_functionality.py # System testing script
├── src/
│   ├── models/
│   │   └── database.py        # SQLAlchemy models and database setup
│   ├── parsers/
│   │   ├── resume_parser.py   # Resume text extraction and parsing
│   │   └── jd_parser.py       # Job description parsing
│   ├── matching/
│   │   ├── hard_matching.py   # Keyword and exact matching
│   │   └── semantic_matching.py # Embedding and LLM-based matching
│   ├── scoring/
│   │   └── scoring_engine.py  # Final scoring and verdict generation
│   └── utils/
│       └── config.py          # Configuration management
├── data/
│   └── uploads/               # Temporary file storage
├── tests/                     # Test files
└── docs/                      # Documentation
```

## 🔌 API Endpoints

### Core Endpoints
- `POST /upload/job-description`: Upload and parse job description
- `POST /upload/resume`: Upload and parse resume
- `POST /evaluate`: Evaluate resume against job description
- `GET /results`: Get evaluation results with filtering
- `GET /dashboard/stats`: Get dashboard statistics

### Data Endpoints
- `GET /job-descriptions`: List all job descriptions
- `GET /resumes`: List all resumes
- `GET /health`: Health check endpoint

## 🧪 Testing

### Run Core Functionality Tests
```bash
python test_core_functionality.py
```

This will test:
- API health check
- Job description upload and parsing
- Resume upload and parsing
- Resume evaluation workflow
- Dashboard endpoints

### Manual Testing
1. Start the server: `python start_server.py`
2. Open dashboard: http://localhost:8501
3. Test both placement officer and student workflows
4. Verify real-time evaluation results

## 🚨 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill existing Python processes
taskkill /f /im python.exe

# Or change ports in start_server.py
```

#### 2. Google API Key Issues
```bash
# Run setup helper
python setup_gemini.py

# Or manually add to .env file
GOOGLE_API_KEY=your_actual_api_key_here
```

#### 3. spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

#### 4. Python Version Compatibility
```bash
# Use Python 3.11+ or install specific requirements
pip install -r requirements_python312.txt
```

### Getting Help
- Check API documentation: http://localhost:8000/docs
- Review error logs in terminal
- Ensure all dependencies are installed
- Verify Google API key is valid

## 📈 Performance

### Benchmarks
- **Resume Parsing**: 1-3 seconds per file
- **Job Description Parsing**: 1-2 seconds per file
- **Evaluation**: 2-5 seconds per resume-JD pair
- **Concurrent Users**: Supports 50+ simultaneous users
- **File Size Limit**: Up to 10MB per file

### Scalability
- **Database**: SQLite for development, PostgreSQL for production
- **File Storage**: Local storage with cleanup
- **API**: FastAPI with async support
- **Frontend**: Streamlit with caching

## 🔒 Security

- **File Validation**: Strict file type checking
- **Input Sanitization**: All inputs are validated and sanitized
- **API Key Protection**: Environment variable storage
- **Data Privacy**: Temporary file cleanup after processing
- **Error Handling**: No sensitive data in error messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is developed for Innomatics Research Labs. All rights reserved.

## 📞 Support

For technical support or questions:
- Check the troubleshooting section above
- Review API documentation at http://localhost:8000/docs
- Ensure all installation steps are completed correctly

---

**🎉 Ready to automate resume evaluation at scale!**

Start the system: `python start_server.py`  
Access dashboard: http://localhost:8501