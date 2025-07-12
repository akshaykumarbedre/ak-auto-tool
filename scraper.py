#!/usr/bin/env python3
"""
Job4Freshers AI Chatbot - Web Scraper Module

This module handles web scraping of job listings from job4freshers.co.in
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Optional
import sqlite3
from datetime import datetime
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Job4Fresherscraper:
    """Web scraper for job4freshers.co.in"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.base_url = "https://job4freshers.co.in"
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing job listings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
        
        conn.commit()
        conn.close()
    
    def scrape_job_listings(self, max_pages: int = 10) -> List[Dict]:
        """Scrape job listings from the website"""
        jobs = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/jobs/page/{page}"
                logger.info(f"Scraping page {page}: {url}")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_jobs = self.extract_jobs_from_page(soup)
                
                if not page_jobs:
                    logger.info(f"No jobs found on page {page}, stopping")
                    break
                
                jobs.extend(page_jobs)
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                continue
        
        return jobs
    
    def extract_jobs_from_page(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract job information from a single page"""
        jobs = []
        
        # Common job listing selectors (to be adjusted based on actual website structure)
        job_elements = soup.find_all(['div', 'article'], class_=re.compile(r'job|listing|card', re.I))
        
        for element in job_elements:
            try:
                job_data = self.extract_job_data(element)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                logger.error(f"Error extracting job data: {e}")
                continue
        
        return jobs
    
    def extract_job_data(self, element) -> Optional[Dict]:
        """Extract job data from a job listing element"""
        try:
            # Extract title
            title_elem = element.find(['h1', 'h2', 'h3', 'h4'], class_=re.compile(r'title|heading', re.I))
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract company
            company_elem = element.find(['div', 'span', 'p'], class_=re.compile(r'company|employer', re.I))
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Extract location
            location_elem = element.find(['div', 'span', 'p'], class_=re.compile(r'location|city', re.I))
            location = location_elem.get_text(strip=True) if location_elem else "N/A"
            
            # Extract experience
            exp_elem = element.find(['div', 'span', 'p'], class_=re.compile(r'experience|exp', re.I))
            experience = exp_elem.get_text(strip=True) if exp_elem else "N/A"
            
            # Extract skills
            skills_elem = element.find(['div', 'span', 'p'], class_=re.compile(r'skills|technologies', re.I))
            skills = skills_elem.get_text(strip=True) if skills_elem else "N/A"
            
            # Extract salary
            salary_elem = element.find(['div', 'span', 'p'], class_=re.compile(r'salary|pay|compensation', re.I))
            salary = salary_elem.get_text(strip=True) if salary_elem else "N/A"
            
            # Extract job URL
            link_elem = element.find('a', href=True)
            job_url = link_elem['href'] if link_elem else "N/A"
            if job_url.startswith('/'):
                job_url = self.base_url + job_url
            
            # Extract description (if available)
            desc_elem = element.find(['div', 'p'], class_=re.compile(r'description|summary', re.I))
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'experience': experience,
                'skills': skills,
                'salary': salary,
                'description': description,
                'url': job_url,
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'job_type': 'Full-time',  # Default value
                'education': 'N/A'
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job element: {e}")
            return None
    
    def save_jobs_to_db(self, jobs: List[Dict]):
        """Save job listings to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for job in jobs:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs 
                    (title, company, location, experience, skills, salary, description, posted_date, job_type, education, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job['title'], job['company'], job['location'], job['experience'],
                    job['skills'], job['salary'], job['description'], job['posted_date'],
                    job['job_type'], job['education'], job['url']
                ))
            except Exception as e:
                logger.error(f"Error saving job to database: {e}")
                continue
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(jobs)} jobs to database")
    
    def get_all_jobs(self) -> List[Dict]:
        """Retrieve all jobs from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM jobs ORDER BY scraped_at DESC')
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        jobs = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return jobs
    
    def run_scraper(self, max_pages: int = 10):
        """Run the complete scraping process"""
        logger.info("Starting job scraping process...")
        
        jobs = self.scrape_job_listings(max_pages)
        
        if jobs:
            self.save_jobs_to_db(jobs)
            logger.info(f"Scraping completed. Found {len(jobs)} jobs.")
        else:
            logger.warning("No jobs found during scraping.")
        
        return jobs

if __name__ == "__main__":
    scraper = Job4Fresherscraper()
    scraper.run_scraper(max_pages=5)