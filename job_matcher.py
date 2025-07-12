#!/usr/bin/env python3
"""
Job4Freshers AI Chatbot - AI Job Matching Engine

This module implements intelligent job matching using ML techniques
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import sqlite3
import re
import logging
from typing import List, Dict, Tuple, Optional
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobMatchingEngine:
    """AI-powered job matching engine"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.sentence_model = None
        self.jobs_df = None
        self.job_vectors = None
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize ML models and load job data"""
        try:
            # Load sentence transformer model (lightweight alternative to OpenAI)
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            logger.warning(f"Sentence transformer not available, using TF-IDF only: {e}")
            self.sentence_model = None
        
        self.load_job_data()
    
    def load_job_data(self):
        """Load job data from database and create feature vectors"""
        try:
            conn = sqlite3.connect(self.db_path)
            self.jobs_df = pd.read_sql_query("SELECT * FROM jobs", conn)
            conn.close()
            
            if not self.jobs_df.empty:
                self.create_job_vectors()
                logger.info(f"Loaded {len(self.jobs_df)} jobs for matching")
            else:
                logger.warning("No jobs found in database")
                
        except Exception as e:
            logger.error(f"Error loading job data: {e}")
            self.jobs_df = pd.DataFrame()
    
    def create_job_vectors(self):
        """Create TF-IDF vectors for job descriptions"""
        if self.jobs_df.empty:
            return
        
        # Combine relevant text fields for vectorization
        job_texts = []
        for _, job in self.jobs_df.iterrows():
            text = f"{job['title']} {job['company']} {job['skills']} {job['description']}"
            job_texts.append(text)
        
        # Create TF-IDF vectors
        self.job_vectors = self.tfidf_vectorizer.fit_transform(job_texts)
        logger.info("Job vectors created successfully")
    
    def preprocess_query(self, query: str) -> str:
        """Preprocess user query for better matching"""
        # Remove special characters and normalize
        query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
        query = query.lower().strip()
        return query
    
    def extract_requirements(self, query: str) -> Dict:
        """Extract job requirements from user query using NLP"""
        requirements = {
            'skills': [],
            'location': [],
            'experience': None,
            'salary': None,
            'job_type': None,
            'education': None
        }
        
        query_lower = query.lower()
        
        # Extract skills (common programming languages and technologies)
        skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'php',
            'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'html', 'css', 'bootstrap', 'django', 'flask',
            'spring', 'hibernate', 'rest', 'api', 'microservices', 'devops',
            'machine learning', 'ai', 'data science', 'analytics', 'tableau',
            'power bi', 'excel', 'salesforce', 'sap', 'oracle', 'testing',
            'selenium', 'junit', 'android', 'ios', 'swift', 'kotlin', 'flutter',
            'react native', 'unity', 'game development', 'blockchain', 'web3'
        ]
        
        for skill in skills_keywords:
            if skill in query_lower:
                requirements['skills'].append(skill)
        
        # Extract location
        location_keywords = [
            'bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai',
            'kolkata', 'ahmedabad', 'gurgaon', 'noida', 'remote', 'work from home'
        ]
        
        for location in location_keywords:
            if location in query_lower:
                requirements['location'].append(location)
        
        # Extract experience
        exp_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)',
            r'fresher', r'entry level', r'junior', r'senior'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, query_lower)
            if match:
                requirements['experience'] = match.group()
                break
        
        # Extract salary
        salary_patterns = [
            r'(\d+)\s*(?:lpa|lakhs?|k|thousand)',
            r'salary\s*(?:of\s*)?(\d+)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)\s*(?:lpa|lakhs?)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, query_lower)
            if match:
                requirements['salary'] = match.group()
                break
        
        # Extract job type
        if any(word in query_lower for word in ['full time', 'full-time', 'permanent']):
            requirements['job_type'] = 'full-time'
        elif any(word in query_lower for word in ['part time', 'part-time']):
            requirements['job_type'] = 'part-time'
        elif any(word in query_lower for word in ['internship', 'intern']):
            requirements['job_type'] = 'internship'
        elif any(word in query_lower for word in ['contract', 'freelance']):
            requirements['job_type'] = 'contract'
        
        return requirements
    
    def calculate_job_score(self, job: pd.Series, requirements: Dict, query: str) -> float:
        """Calculate matching score for a job based on requirements"""
        score = 0.0
        
        # Title and description relevance (40% weight)
        job_text = f"{job['title']} {job['description']} {job['skills']}"
        if self.sentence_model:
            try:
                query_embedding = self.sentence_model.encode([query])
                job_embedding = self.sentence_model.encode([job_text])
                similarity = cosine_similarity(query_embedding, job_embedding)[0][0]
                score += similarity * 0.4
            except:
                # Fall back to TF-IDF if sentence transformer fails
                score += self.calculate_tfidf_similarity(query, job_text) * 0.4
        else:
            # Use TF-IDF similarity when sentence transformer is not available
            score += self.calculate_tfidf_similarity(query, job_text) * 0.4
        
        # Skills matching (30% weight)
        if requirements['skills']:
            job_skills = job['skills'].lower()
            matched_skills = sum(1 for skill in requirements['skills'] if skill in job_skills)
            skills_score = matched_skills / len(requirements['skills'])
            score += skills_score * 0.3
        
        # Location matching (15% weight)
        if requirements['location']:
            job_location = job['location'].lower()
            location_match = any(loc in job_location for loc in requirements['location'])
            if location_match:
                score += 0.15
        
        # Experience matching (10% weight)
        if requirements['experience']:
            job_exp = job['experience'].lower()
            if 'fresher' in requirements['experience'] and 'fresher' in job_exp:
                score += 0.1
            elif any(char.isdigit() for char in requirements['experience']):
                # Extract numeric experience requirements
                req_exp = re.findall(r'\d+', requirements['experience'])
                job_exp_nums = re.findall(r'\d+', job_exp)
                if req_exp and job_exp_nums:
                    if int(req_exp[0]) <= int(job_exp_nums[0]):
                        score += 0.1
        
        # Job type matching (5% weight)
        if requirements['job_type']:
            job_type = job['job_type'].lower()
            if requirements['job_type'] in job_type:
                score += 0.05
        
        return score
    
    def calculate_tfidf_similarity(self, query: str, job_text: str) -> float:
        """Calculate TF-IDF similarity between query and job text"""
        try:
            # Create a simple TF-IDF comparison
            texts = [query.lower(), job_text.lower()]
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            # Fallback to simple word matching
            query_words = set(query.lower().split())
            job_words = set(job_text.lower().split())
            intersection = query_words.intersection(job_words)
            union = query_words.union(job_words)
            return len(intersection) / len(union) if union else 0.0
    
    def find_matching_jobs(self, query: str, top_k: int = 10) -> List[Dict]:
        """Find top matching jobs for a user query"""
        if self.jobs_df.empty:
            return []
        
        # Preprocess query and extract requirements
        processed_query = self.preprocess_query(query)
        requirements = self.extract_requirements(query)
        
        # Calculate scores for all jobs
        job_scores = []
        for idx, job in self.jobs_df.iterrows():
            score = self.calculate_job_score(job, requirements, processed_query)
            job_scores.append((idx, score))
        
        # Sort by score and get top matches
        job_scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = job_scores[:top_k]
        
        # Format results
        results = []
        for idx, score in top_matches:
            job = self.jobs_df.iloc[idx]
            result = {
                'id': int(job['id']),  # Convert numpy int64 to Python int
                'title': str(job['title']),
                'company': str(job['company']),
                'location': str(job['location']),
                'experience': str(job['experience']),
                'skills': str(job['skills']),
                'salary': str(job['salary']),
                'description': str(job['description'])[:200] + '...' if len(str(job['description'])) > 200 else str(job['description']),
                'url': str(job['url']),
                'match_score': float(score),  # Ensure it's a Python float
                'posted_date': str(job['posted_date']),
                'job_type': str(job.get('job_type', 'N/A')),
                'education': str(job.get('education', 'N/A')),
                'eligibility': str(job.get('eligibility', 'N/A')),
                'last_date': str(job.get('last_date', 'N/A')),
                'application_link': str(job.get('application_link', 'N/A'))
            }
            results.append(result)
        
        return results
    
    def get_job_recommendations(self, user_profile: Dict, top_k: int = 5) -> List[Dict]:
        """Get job recommendations based on user profile"""
        if self.jobs_df.empty:
            return []
        
        # Create query from user profile
        query_parts = []
        if 'skills' in user_profile:
            query_parts.extend(user_profile['skills'])
        if 'experience' in user_profile:
            query_parts.append(f"{user_profile['experience']} experience")
        if 'location' in user_profile:
            query_parts.append(user_profile['location'])
        
        query = ' '.join(query_parts)
        return self.find_matching_jobs(query, top_k)
    
    def get_job_statistics(self) -> Dict:
        """Get statistics about available jobs"""
        if self.jobs_df.empty:
            return {}
        
        stats = {
            'total_jobs': len(self.jobs_df),
            'top_companies': self.jobs_df['company'].value_counts().head(10).to_dict(),
            'top_locations': self.jobs_df['location'].value_counts().head(10).to_dict(),
            'top_skills': self.extract_top_skills(),
            'experience_distribution': self.jobs_df['experience'].value_counts().to_dict(),
            'recent_jobs': len(self.jobs_df[self.jobs_df['posted_date'] >= pd.Timestamp.now().strftime('%Y-%m-%d')])
        }
        
        return stats
    
    def extract_top_skills(self) -> Dict:
        """Extract top skills from job listings"""
        skill_counts = {}
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'html', 'css', 'php', 'node.js'
        ]
        
        for _, job in self.jobs_df.iterrows():
            skills_text = job['skills'].lower()
            for skill in common_skills:
                if skill in skills_text:
                    skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Sort by count
        sorted_skills = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
        return dict(list(sorted_skills.items())[:15])

if __name__ == "__main__":
    engine = JobMatchingEngine()
    
    # Test query
    test_query = "python developer with 2 years experience in bangalore"
    results = engine.find_matching_jobs(test_query)
    
    print(f"Found {len(results)} matching jobs:")
    for job in results[:3]:
        print(f"- {job['title']} at {job['company']} (Score: {job['match_score']})")