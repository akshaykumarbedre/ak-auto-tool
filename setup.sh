#!/bin/bash

# Job4Freshers AI Chatbot Setup Script

echo "🚀 Job4Freshers AI Chatbot Setup"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
"

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "
from scraper import Job4Fresherscraper
scraper = Job4Fresherscraper()
print('Database initialized successfully!')
"

# Create sample job data for testing
echo "🧪 Creating sample job data..."
python3 -c "
import sqlite3
from datetime import datetime

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

sample_jobs = [
    ('Python Developer', 'TechCorp', 'Bangalore', '2-3 years', 'Python, Django, SQL, AWS', '8-12 LPA', 'We are looking for an experienced Python developer to join our team...', '2024-01-15', 'Full-time', 'B.Tech/B.E', 'https://example.com/job1'),
    ('Data Scientist', 'DataTech Solutions', 'Mumbai', '1-2 years', 'Python, Machine Learning, SQL, Pandas', '10-15 LPA', 'Join our data science team to work on cutting-edge AI projects...', '2024-01-14', 'Full-time', 'M.Tech/M.S', 'https://example.com/job2'),
    ('Frontend Developer', 'WebWorks', 'Remote', 'Fresher', 'React, JavaScript, HTML, CSS', '5-8 LPA', 'Looking for a passionate frontend developer to build amazing user interfaces...', '2024-01-13', 'Full-time', 'B.Tech/B.E', 'https://example.com/job3'),
    ('Java Developer', 'Enterprise Solutions', 'Hyderabad', '3-5 years', 'Java, Spring Boot, Microservices, REST API', '12-18 LPA', 'Senior Java developer position with excellent growth opportunities...', '2024-01-12', 'Full-time', 'B.Tech/B.E', 'https://example.com/job4'),
    ('DevOps Engineer', 'CloudTech', 'Pune', '2-4 years', 'AWS, Docker, Kubernetes, Jenkins', '15-20 LPA', 'DevOps engineer to manage cloud infrastructure and CI/CD pipelines...', '2024-01-11', 'Full-time', 'B.Tech/B.E', 'https://example.com/job5'),
    ('UI/UX Designer', 'DesignStudio', 'Chennai', '1-3 years', 'Figma, Adobe XD, User Research, Prototyping', '6-10 LPA', 'Creative UI/UX designer to create intuitive user experiences...', '2024-01-10', 'Full-time', 'Design Degree', 'https://example.com/job6'),
    ('Mobile App Developer', 'MobileFirst', 'Bangalore', '2-3 years', 'React Native, Flutter, iOS, Android', '10-14 LPA', 'Mobile app developer for cross-platform mobile applications...', '2024-01-09', 'Full-time', 'B.Tech/B.E', 'https://example.com/job7'),
    ('Business Analyst', 'Analytics Pro', 'Delhi', '1-2 years', 'SQL, Excel, Power BI, Business Intelligence', '7-11 LPA', 'Business analyst to work with stakeholders and analyze business requirements...', '2024-01-08', 'Full-time', 'MBA/B.Tech', 'https://example.com/job8'),
    ('Software Tester', 'QualityFirst', 'Noida', 'Fresher', 'Manual Testing, Selenium, Test Automation', '4-7 LPA', 'Software tester position for freshers with testing fundamentals...', '2024-01-07', 'Full-time', 'B.Tech/B.E', 'https://example.com/job9'),
    ('Full Stack Developer', 'InnovateTech', 'Remote', '2-4 years', 'MEAN Stack, Node.js, Angular, MongoDB', '12-16 LPA', 'Full stack developer for modern web applications using MEAN stack...', '2024-01-06', 'Full-time', 'B.Tech/B.E', 'https://example.com/job10')
]

for job in sample_jobs:
    cursor.execute('''
        INSERT INTO jobs (title, company, location, experience, skills, salary, description, posted_date, job_type, education, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', job)

conn.commit()
conn.close()
print('Sample job data created successfully!')
"

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start the chatbot server: python3 app.py"
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "🔧 Available commands:"
echo "- Run scraper: python3 scraper.py"
echo "- Test job matching: python3 job_matcher.py"
echo "- Test chatbot: python3 chatbot.py"
echo ""
echo "Happy coding! 🚀"