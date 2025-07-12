#!/usr/bin/env python3
"""
Job4Freshers AI Chatbot - Test Suite

This script tests the core functionality of the chatbot system
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import json

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper import Job4Fresherscraper
from job_matcher import JobMatchingEngine
from chatbot import ChatbotConversationManager

class TestJob4FreshersBot(unittest.TestCase):
    """Test suite for Job4Freshers AI Chatbot"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_db = "test_jobs.db"
        self.scraper = Job4Fresherscraper(self.test_db)
        self.job_matcher = JobMatchingEngine(self.test_db)
        self.chatbot = ChatbotConversationManager(self.job_matcher)
        
        # Create test data
        self.create_test_jobs()
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
    
    def create_test_jobs(self):
        """Create test job data"""
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        
        # Ensure table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                experience TEXT,
                skills TEXT,
                salary TEXT,
                description TEXT,
                posted_date TEXT,
                job_type TEXT,
                education TEXT,
                url TEXT UNIQUE,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        test_jobs = [
            ('Python Developer', 'TechCorp', 'Bangalore', '2-3 years', 'Python, Django, SQL', '10 LPA', 'Python development role', '2024-01-15', 'Full-time', 'B.Tech', 'https://example.com/job1'),
            ('Data Scientist', 'DataCorp', 'Mumbai', '1-2 years', 'Python, Machine Learning', '12 LPA', 'Data science role', '2024-01-14', 'Full-time', 'M.Tech', 'https://example.com/job2'),
            ('Frontend Developer', 'WebCorp', 'Remote', 'Fresher', 'React, JavaScript', '8 LPA', 'Frontend development', '2024-01-13', 'Full-time', 'B.Tech', 'https://example.com/job3')
        ]
        
        for job in test_jobs:
            cursor.execute('''
                INSERT INTO jobs (title, company, location, experience, skills, salary, description, posted_date, job_type, education, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', job)
        
        conn.commit()
        conn.close()
    
    def test_database_initialization(self):
        """Test database initialization"""
        self.assertTrue(os.path.exists(self.test_db))
        
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreater(count, 0, "Database should contain test jobs")
    
    def test_job_matching_engine(self):
        """Test job matching functionality"""
        # Test basic job search
        results = self.job_matcher.find_matching_jobs("Python developer", top_k=5)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find Python-related jobs")
        
        # Test skills extraction
        requirements = self.job_matcher.extract_requirements("I want Python jobs in Bangalore")
        self.assertIn('python', requirements['skills'])
        self.assertIn('bangalore', requirements['location'])
    
    def test_chatbot_intent_detection(self):
        """Test chatbot intent detection"""
        # Test greeting intent
        intent = self.chatbot.detect_intent("Hello")
        self.assertEqual(intent, 'greeting')
        
        # Test job search intent
        intent = self.chatbot.detect_intent("I'm looking for Python jobs")
        self.assertEqual(intent, 'job_search')
        
        # Test skill-based intent
        intent = self.chatbot.detect_intent("I know Python and Django")
        self.assertEqual(intent, 'skill_based')
    
    def test_chatbot_entity_extraction(self):
        """Test entity extraction from user messages"""
        entities = self.chatbot.extract_entities("I want Python developer jobs in Bangalore with 2 years experience")
        
        self.assertIn('python', entities['skills'])
        self.assertIn('bangalore', entities['location'])
        self.assertIsNotNone(entities['experience'])
    
    def test_chatbot_response_generation(self):
        """Test chatbot response generation"""
        # Test greeting response
        response = self.chatbot.generate_response("Hello")
        self.assertIn('message', response)
        self.assertIn('suggestions', response)
        self.assertEqual(response['intent'], 'greeting')
        
        # Test job search response
        response = self.chatbot.generate_response("Find Python jobs")
        self.assertIn('message', response)
        self.assertIn('jobs', response)
        self.assertEqual(response['intent'], 'job_search')
    
    def test_job_statistics(self):
        """Test job statistics generation"""
        stats = self.job_matcher.get_job_statistics()
        
        self.assertIn('total_jobs', stats)
        self.assertIn('top_companies', stats)
        self.assertIn('top_locations', stats)
        self.assertGreater(stats['total_jobs'], 0)
    
    def test_conversation_history(self):
        """Test conversation history management"""
        # Send a few messages
        self.chatbot.generate_response("Hello")
        self.chatbot.generate_response("Find Python jobs")
        self.chatbot.generate_response("Show me data science roles")
        
        history = self.chatbot.get_conversation_history()
        self.assertEqual(len(history), 3)
        
        # Test conversation reset
        self.chatbot.reset_conversation()
        history = self.chatbot.get_conversation_history()
        self.assertEqual(len(history), 0)
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        self.assertIsNotNone(self.scraper.session)
        self.assertTrue(os.path.exists(self.test_db))
    
    def test_job_data_retrieval(self):
        """Test job data retrieval"""
        jobs = self.scraper.get_all_jobs()
        self.assertIsInstance(jobs, list)
        self.assertGreater(len(jobs), 0)
        
        # Check job structure
        job = jobs[0]
        required_fields = ['title', 'company', 'location', 'skills']
        for field in required_fields:
            self.assertIn(field, job)

def run_tests():
    """Run all tests"""
    print("🧪 Running Job4Freshers AI Chatbot Tests")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJob4FreshersBot)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed:")
        for failure in result.failures:
            print(f"  - {failure[0]}: {failure[1]}")
        for error in result.errors:
            print(f"  - {error[0]}: {error[1]}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)