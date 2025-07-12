# Job4Freshers AI Chatbot 🤖

An intelligent end-to-end AI chatbot designed to help job seekers find suitable opportunities on job4freshers.co.in. This chatbot uses advanced NLP and machine learning techniques to understand user requirements and provide personalized job recommendations.

## ✨ Features

- 🔍 **Intelligent Job Search**: Natural language processing to understand user queries
- 🎯 **Smart Job Matching**: AI-powered matching algorithm based on skills, location, and experience
- 💬 **Conversational Interface**: User-friendly chat interface with contextual responses
- 📊 **Real-time Statistics**: Job market insights and trending data
- 🌐 **Web Scraping**: Automated job data collection from job4freshers.co.in
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🔄 **Real-time Updates**: Live job recommendations and market trends
- 📁 **CSV Export**: Export job data to CSV files for analysis and integration

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Web UI)                        │
│                 HTML, CSS, JavaScript                       │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask API Server                         │
│                 REST API Endpoints                          │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Web Scraper   │  │ Job Matcher AI  │  │ Chatbot Engine  │
│  (job4freshers) │  │ (ML Algorithm)  │  │ (NLP & Context) │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                                │
                                ▼
                ┌─────────────────────────────────────┐
                │          SQLite Database           │
                │         (Job Listings)             │
                └─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akshaykumarbedre/Every_day_task.git
   cd Every_day_task
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

3. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Start the chatbot server**
   ```bash
   python3 app.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📋 Manual Installation

If you prefer manual installation:

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required ML models**
   ```bash
   python3 -c "
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('wordnet')
   "
   ```

4. **Initialize database**
   ```bash
   python3 scraper.py
   ```

## 🎯 Usage

### Web Interface

1. Open the web interface at `http://localhost:5000`
2. Start chatting with the AI assistant
3. Ask for job recommendations using natural language:
   - "Find Python developer jobs in Bangalore"
   - "Show me remote opportunities for data science"
   - "I need entry-level positions in Mumbai"

### API Endpoints

#### Chat with the bot
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "I'm looking for Python jobs",
  "session_id": "user_session_123"
}
```

#### Search jobs
```bash
POST /api/jobs/search
Content-Type: application/json

{
  "query": "Python developer Bangalore",
  "limit": 10
}
```

#### Get job statistics
```bash
GET /api/jobs/statistics
```

#### Trigger job scraping
```bash
POST /api/scrape
Content-Type: application/json

{
  "max_pages": 5
}
```

#### Export jobs to CSV
```bash
GET /api/jobs/export/csv
```

## 📁 CSV Export Feature

The system includes comprehensive CSV export functionality for job data:

### Export Options
1. **Manual Export**: Use the `/api/jobs/export/csv` endpoint
2. **Automatic Export**: Enable during full extraction runs
3. **Sample Export**: Generate sample data for testing

### CSV File Structure
- **job4freshers_jobs_data.csv**: Main data file
- **job4freshers_jobs_YYYYMMDD_HHMMSS.csv**: Timestamped exports
- All job fields included (title, company, location, skills, etc.)
- UTF-8 encoding for international characters

### Usage Examples
```python
# Export using scraper
from scraper import Job4Fresherscraper
scraper = Job4Fresherscraper()
csv_file = scraper.export_jobs_to_csv()

# Create sample CSV
python create_sample_csv.py
```

For detailed CSV documentation, see [CSV_EXPORT_DOCUMENTATION.md](CSV_EXPORT_DOCUMENTATION.md).

## 🧠 AI Features

### Natural Language Processing
- Intent detection (greeting, job search, skill-based queries)
- Entity extraction (skills, location, experience, salary)
- Context awareness and conversation history

### Machine Learning Job Matching
- TF-IDF vectorization for job descriptions
- Sentence transformers for semantic similarity
- Multi-factor scoring algorithm:
  - Skills matching (30% weight)
  - Location preferences (15% weight)
  - Experience level (10% weight)
  - Job type matching (5% weight)
  - Semantic similarity (40% weight)

### Intelligent Features
- Personalized job recommendations
- Real-time job market statistics
- Conversation context retention
- Smart suggestion system

## 🔧 Configuration

Edit the `.env` file to customize settings:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_PATH=jobs.db

# Scraping Configuration
SCRAPING_MAX_PAGES=10
SCRAPING_DELAY=1

# AI Model Configuration
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
TFIDF_MAX_FEATURES=5000

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
```

## 📊 Job Statistics

The chatbot provides real-time insights:
- Total available jobs
- Recently posted positions
- Top hiring companies
- Popular job locations
- In-demand skills
- Salary trends

## 🛠️ Development

### Running Individual Components

**Test the web scraper:**
```bash
python3 scraper.py
```

**Test the job matching engine:**
```bash
python3 job_matcher.py
```

**Test the chatbot conversation:**
```bash
python3 chatbot.py
```

### Adding New Features

1. **Custom scrapers**: Modify `scraper.py` to add new job sites
2. **Enhanced matching**: Update `job_matcher.py` for better algorithms
3. **Chatbot improvements**: Extend `chatbot.py` with new intents
4. **UI enhancements**: Customize templates and static files

## 🔍 How It Works

### 1. Web Scraping
- Automatically crawls job4freshers.co.in
- Extracts job titles, companies, locations, skills, and descriptions
- Stores structured data in SQLite database
- Handles rate limiting and error recovery

### 2. Job Matching Algorithm
- Processes user queries using NLP
- Extracts relevant entities (skills, location, experience)
- Calculates similarity scores using multiple factors
- Ranks jobs based on relevance and match quality

### 3. Conversational AI
- Detects user intent from natural language
- Maintains conversation context
- Provides personalized responses
- Offers smart suggestions and follow-ups

### 4. Real-time Updates
- Continuously updates job database
- Provides fresh market statistics
- Adapts to changing job market trends

## 🚨 Troubleshooting

### Common Issues

**1. ImportError: No module named 'xyz'**
```bash
pip install -r requirements.txt
```

**2. Database not found**
```bash
python3 scraper.py
```

**3. Port already in use**
```bash
# Change port in app.py or kill existing process
lsof -ti:5000 | xargs kill -9
```

**4. Scraping blocked**
- Check website accessibility
- Adjust scraping delays
- Verify website structure hasn't changed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- job4freshers.co.in for job data
- Hugging Face for transformer models
- Flask community for the web framework
- Scikit-learn for ML algorithms

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

**Happy job hunting! 🎯**

Made with ❤️ for job seekers everywhere