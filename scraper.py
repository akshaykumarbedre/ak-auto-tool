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
import csv
import os

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.max_retries = 3
        self.retry_delay = 2
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
                eligibility TEXT,
                last_date TEXT,
                application_link TEXT,
                url TEXT UNIQUE,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster searches
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON jobs(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_company ON jobs(company)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON jobs(location)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scraped_at ON jobs(scraped_at)')
        
        conn.commit()
        conn.close()
    
    def get_all_job_urls_from_sitemap(self) -> List[str]:
        """Extract all job URLs from the sitemap"""
        logger.info("Extracting job URLs from sitemap...")
        
        sitemap_url = f"{self.base_url}/sitemap/"
        job_urls = []
        
        try:
            response = self.session.get(sitemap_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            logger.info(f"Found {len(links)} total links in sitemap")
            
            # Filter for job URLs
            job_patterns = self.get_job_url_patterns()
            non_job_patterns = self.get_non_job_url_patterns()
            
            for link in links:
                href = link['href']
                
                # Normalize URL
                if href.startswith('/'):
                    href = self.base_url + href
                elif not href.startswith('http'):
                    continue
                
                # Check if this is a job URL
                if self.is_job_url(href, job_patterns, non_job_patterns):
                    job_urls.append(href)
            
            logger.info(f"Identified {len(job_urls)} job URLs from sitemap")
            return job_urls
            
        except Exception as e:
            logger.error(f"Error extracting URLs from sitemap: {e}")
            return []
    
    def get_job_url_patterns(self) -> List[str]:
        """Get patterns that identify job URLs"""
        return [
            # Job URLs typically have this pattern: https://job4freshers.co.in/company-position-title/
            r'^https://job4freshers\.co\.in/[a-zA-Z0-9\-]+-[a-zA-Z0-9\-]+.*/$',
            # More general pattern for job URLs
            r'^https://job4freshers\.co\.in/[^/]+/$',
        ]
    
    def get_non_job_url_patterns(self) -> List[str]:
        """Get patterns that identify non-job URLs"""
        return [
            'latest-government-jobs',
            'job-by-location',
            'job-by-category',
            'category/',
            'tag/',
            'author/',
            'page/',
            'sitemap',
            'contact',
            'about',
            'privacy',
            'terms',
            '/wp-',
            '/#',
            'mailto:',
            'tel:',
            '.pdf',
            '.doc',
            '.jpg',
            '.png',
            '.gif'
        ]
    
    def is_job_url(self, url: str, job_patterns: List[str], non_job_patterns: List[str]) -> bool:
        """Check if a URL is a job URL"""
        # First check if it's explicitly a non-job URL
        for pattern in non_job_patterns:
            if pattern in url.lower():
                return False
        
        # Check if it matches job URL patterns
        if url.startswith('https://job4freshers.co.in/') and url.endswith('/'):
            # Extract the slug part
            slug = url.replace('https://job4freshers.co.in/', '').strip('/')
            
            # Should be a single slug, not nested paths
            if '/' not in slug and len(slug) > 3:
                # Additional checks for job-like patterns
                if any(keyword in slug.lower() for keyword in [
                    'job', 'vacancy', 'position', 'career', 'hiring', 'recruitment',
                    'engineer', 'developer', 'analyst', 'manager', 'associate',
                    'consultant', 'specialist', 'coordinator', 'executive',
                    'trainee', 'intern', 'assistant', 'lead', 'senior'
                ]):
                    return True
                
                # If it looks like a company-position pattern (contains hyphens)
                if '-' in slug and len(slug.split('-')) >= 2:
                    return True
        
        return False
    
    def scrape_job_listings(self, max_jobs: int = None) -> List[Dict]:
        """Scrape job listings using sitemap-based approach"""
        logger.info("Starting sitemap-based job extraction...")
        
        # Get all job URLs from sitemap
        job_urls = self.get_all_job_urls_from_sitemap()
        
        if not job_urls:
            logger.error("No job URLs found in sitemap")
            return []
        
        # Limit the number of jobs if specified
        if max_jobs:
            job_urls = job_urls[:max_jobs]
            logger.info(f"Limited to first {max_jobs} job URLs")
        
        logger.info(f"Processing {len(job_urls)} job URLs...")
        
        jobs = []
        failed_count = 0
        
        for i, job_url in enumerate(job_urls, 1):
            try:
                logger.info(f"Processing job {i}/{len(job_urls)}: {job_url}")
                
                job_data = self.scrape_individual_job(job_url)
                
                if job_data and self.is_valid_job_data(job_data):
                    jobs.append(job_data)
                    logger.info(f"Successfully extracted: {job_data.get('title', 'N/A')}")
                else:
                    failed_count += 1
                    logger.warning(f"Failed to extract valid data from: {job_url}")
                
                # Rate limiting
                time.sleep(1)
                
                # Progress logging
                if i % 10 == 0:
                    logger.info(f"Progress: {i}/{len(job_urls)} processed, {len(jobs)} jobs extracted")
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Error processing {job_url}: {e}")
                continue
        
        logger.info(f"Sitemap-based extraction completed: {len(jobs)} jobs extracted, {failed_count} failed")
        return jobs
    
    def scrape_individual_job(self, job_url: str) -> Optional[Dict]:
        """Scrape detailed job information from an individual job page"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(job_url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_data = self.extract_job_data_from_page(soup, job_url)
                
                return job_data
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed for {job_url} (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to scrape {job_url} after {self.max_retries} attempts")
                    return None
        
        return None
    
    def extract_job_data_from_page(self, soup: BeautifulSoup, job_url: str) -> Optional[Dict]:
        """Extract comprehensive job data from an individual job page"""
        try:
            # Extract title - try multiple strategies
            title = self.extract_job_title(soup)
            if not title:
                return None
            
            # Extract other job details
            company = self.extract_job_company(soup)
            location = self.extract_job_location(soup)
            experience = self.extract_job_experience(soup)
            skills = self.extract_job_skills(soup)
            salary = self.extract_job_salary(soup)
            description = self.extract_job_description(soup)
            job_type = self.extract_job_type(soup)
            education = self.extract_job_education(soup)
            eligibility = self.extract_job_eligibility(soup)
            last_date = self.extract_job_last_date(soup)
            application_link = self.extract_application_link(soup, job_url)
            
            # Create job data object
            job_data = {
                'title': self.clean_text(title),
                'company': self.clean_text(company) or "N/A",
                'location': self.clean_text(location) or "N/A",
                'experience': self.clean_text(experience) or "N/A",
                'skills': self.clean_text(skills) or "N/A",
                'salary': self.clean_text(salary) or "N/A",
                'description': self.clean_text(description) or "N/A",
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'job_type': self.clean_text(job_type) or "Full-time",
                'education': self.clean_text(education) or "N/A",
                'eligibility': self.clean_text(eligibility) or "N/A",
                'last_date': self.clean_text(last_date) or "N/A",
                'application_link': application_link or "N/A",
                'url': job_url
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error extracting job data from {job_url}: {e}")
            return None
    
    def extract_job_title(self, soup: BeautifulSoup) -> str:
        """Extract job title from page"""
        selectors = [
            'h1.entry-title',
            'h1.post-title',
            'h1.job-title',
            'h1',
            '.entry-title',
            '.post-title',
            '.job-title',
            'h2.entry-title',
            'h2.post-title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 3:
                    return title
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove site name from title
            title = title.replace('- Job4Freshers', '').replace('Job4Freshers', '').strip()
            if title and len(title) > 3:
                return title
        
        return ""
    
    def extract_job_company(self, soup: BeautifulSoup) -> str:
        """Extract company name"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['company', 'employer', 'organization']},
            {'tag': ['strong', 'b'], 'text_contains': ['company', 'employer']},
            {'tag': ['li'], 'text_contains': ['company', 'employer']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_location(self, soup: BeautifulSoup) -> str:
        """Extract job location"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['location', 'city', 'place', 'address']},
            {'tag': ['strong', 'b'], 'text_contains': ['location', 'city', 'place']},
            {'tag': ['li'], 'text_contains': ['location', 'city']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_experience(self, soup: BeautifulSoup) -> str:
        """Extract experience requirements"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['experience', 'exp', 'years']},
            {'tag': ['strong', 'b'], 'text_contains': ['experience', 'exp', 'years']},
            {'tag': ['li'], 'text_contains': ['experience', 'exp']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_skills(self, soup: BeautifulSoup) -> str:
        """Extract required skills"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['skills', 'technologies', 'tech', 'requirements']},
            {'tag': ['ul', 'li'], 'class_contains': ['skills', 'tech']},
            {'tag': ['strong', 'b'], 'text_contains': ['skills', 'tech', 'requirement']},
        ]
        
        result = self.extract_by_patterns(soup, patterns)
        
        # If no specific skills section, try to extract from content
        if not result or result == "N/A":
            content = soup.get_text()
            skill_keywords = [
                'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Node.js',
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'AWS', 'Azure',
                'Docker', 'Kubernetes', 'Git', 'Jenkins', 'Selenium',
                'C++', 'C#', '.NET', 'PHP', 'Ruby', 'Go', 'Rust'
            ]
            
            found_skills = [skill for skill in skill_keywords if skill in content]
            if found_skills:
                result = ', '.join(found_skills[:5])  # Limit to top 5 skills
        
        return result
    
    def extract_job_salary(self, soup: BeautifulSoup) -> str:
        """Extract salary information"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['salary', 'pay', 'compensation', 'package', 'ctc']},
            {'tag': ['strong', 'b'], 'text_contains': ['salary', 'pay', 'package', 'ctc']},
            {'tag': ['li'], 'text_contains': ['salary', 'pay']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_description(self, soup: BeautifulSoup) -> str:
        """Extract job description"""
        # Try to find main content area
        content_selectors = [
            '.entry-content',
            '.post-content',
            '.job-description',
            '.content',
            'article',
            '.main-content'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                # Remove script and style elements
                for script in element(["script", "style"]):
                    script.decompose()
                
                text = element.get_text(strip=True)
                if text and len(text) > 50:  # Meaningful description
                    return text[:1000]  # Limit length
        
        # Fallback to all text content
        all_text = soup.get_text(strip=True)
        return all_text[:500] if all_text else "N/A"
    
    def extract_job_type(self, soup: BeautifulSoup) -> str:
        """Extract job type"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['type', 'category', 'mode']},
            {'tag': ['span'], 'class_contains': ['tag', 'label']},
            {'tag': ['strong', 'b'], 'text_contains': ['type', 'mode']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_education(self, soup: BeautifulSoup) -> str:
        """Extract education requirements"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['education', 'qualification', 'degree']},
            {'tag': ['li'], 'text_contains': ['education', 'qualification', 'degree']},
            {'tag': ['strong', 'b'], 'text_contains': ['education', 'qualification']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_eligibility(self, soup: BeautifulSoup) -> str:
        """Extract eligibility criteria"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['eligibility', 'criteria', 'requirement']},
            {'tag': ['ul', 'li'], 'class_contains': ['eligibility', 'criteria']},
            {'tag': ['strong', 'b'], 'text_contains': ['eligibility', 'criteria']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_job_last_date(self, soup: BeautifulSoup) -> str:
        """Extract application deadline"""
        patterns = [
            {'tag': ['div', 'span', 'p'], 'class_contains': ['last-date', 'deadline', 'expire', 'apply-by']},
            {'tag': ['time'], 'class_contains': []},
            {'tag': ['strong', 'b'], 'text_contains': ['last date', 'deadline', 'apply by']},
        ]
        
        return self.extract_by_patterns(soup, patterns)
    
    def extract_application_link(self, soup: BeautifulSoup, job_url: str) -> str:
        """Extract application link"""
        # Look for apply buttons/links
        apply_selectors = [
            'a[href*="apply"]',
            'a.apply-btn',
            'a.apply-button',
            '.apply-link a',
            'a[href*="application"]'
        ]
        
        for selector in apply_selectors:
            element = soup.select_one(selector)
            if element and element.get('href'):
                href = element['href']
                if href.startswith('/'):
                    href = self.base_url + href
                return href
        
        # Fallback to the job page itself
        return job_url
    
    def extract_by_patterns(self, soup: BeautifulSoup, patterns: List[Dict]) -> str:
        """Extract text using multiple patterns"""
        for pattern in patterns:
            tags = pattern['tag']
            class_contains = pattern.get('class_contains', [])
            text_contains = pattern.get('text_contains', [])
            
            # Try class-based search
            if class_contains:
                for class_keyword in class_contains:
                    for tag in tags:
                        elements = soup.find_all(tag, class_=re.compile(class_keyword, re.I))
                        for element in elements:
                            text = element.get_text(strip=True)
                            if text and len(text) > 2:
                                return text
            
            # Try text-based search
            if text_contains:
                for text_keyword in text_contains:
                    for tag in tags:
                        elements = soup.find_all(tag)
                        for element in elements:
                            element_text = element.get_text(strip=True)
                            if text_keyword.lower() in element_text.lower() and len(element_text) > len(text_keyword) + 2:
                                return element_text
        
        return ""
    

    

    

    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common unwanted characters
        text = re.sub(r'[^\w\s\-\.,:/()&@]', '', text)
        
        return text
    
    def is_valid_job_data(self, job_data: Dict) -> bool:
        """Validate if job data is meaningful"""
        if not job_data:
            return False
        
        # Check if essential fields are present
        title = job_data.get('title', '').strip()
        company = job_data.get('company', '').strip()
        
        if not title or title.lower() in ['n/a', 'na', '']:
            return False
        
        if not company or company.lower() in ['n/a', 'na', '']:
            return False
        
        # Check if title looks like a job title (not just random text)
        if len(title) < 3 or len(title) > 200:
            return False
        
        return True
    

    

    
    def save_jobs_to_db(self, jobs: List[Dict]):
        """Save job listings to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        for job in jobs:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO jobs 
                    (title, company, location, experience, skills, salary, description, 
                     posted_date, job_type, education, eligibility, last_date, application_link, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    job['title'], job['company'], job['location'], job['experience'],
                    job['skills'], job['salary'], job['description'], job['posted_date'],
                    job['job_type'], job['education'], job['eligibility'], job['last_date'],
                    job['application_link'], job['url']
                ))
                saved_count += 1
            except Exception as e:
                logger.error(f"Error saving job to database: {e}")
                continue
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {saved_count} jobs to database")
        return saved_count
    
    def get_job_statistics(self) -> Dict:
        """Get statistics about scraped jobs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Total jobs
            cursor.execute('SELECT COUNT(*) FROM jobs')
            total_jobs = cursor.fetchone()[0]
            
            # Jobs by company
            cursor.execute('SELECT company, COUNT(*) FROM jobs GROUP BY company ORDER BY COUNT(*) DESC LIMIT 10')
            top_companies = dict(cursor.fetchall())
            
            # Jobs by location
            cursor.execute('SELECT location, COUNT(*) FROM jobs GROUP BY location ORDER BY COUNT(*) DESC LIMIT 10')
            top_locations = dict(cursor.fetchall())
            
            # Recent jobs (last 7 days)
            cursor.execute('''
                SELECT COUNT(*) FROM jobs 
                WHERE scraped_at >= datetime('now', '-7 days')
            ''')
            recent_jobs = cursor.fetchone()[0]
            
            stats = {
                'total_jobs': total_jobs,
                'top_companies': top_companies,
                'top_locations': top_locations,
                'recent_jobs': recent_jobs
            }
            
            conn.close()
            return stats
            
        except Exception as e:
            logger.error(f"Error getting job statistics: {e}")
            conn.close()
            return {}
    
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
    
    def run_scraper(self, max_jobs: int = None):
        """Run the complete sitemap-based scraping process"""
        logger.info("Starting sitemap-based job scraping process...")
        logger.info(f"Target: Extract ALL job posts from {self.base_url}")
        logger.info(f"Method: Sitemap-based extraction from {self.base_url}/sitemap/")
        
        start_time = datetime.now()
        
        # Get initial database count
        initial_stats = self.get_job_statistics()
        initial_count = initial_stats.get('total_jobs', 0)
        logger.info(f"Initial database contains {initial_count} jobs")
        
        # Run the sitemap-based scraping
        jobs = self.scrape_job_listings(max_jobs)
        
        if jobs:
            saved_count = self.save_jobs_to_db(jobs)
            
            # Get final statistics
            final_stats = self.get_job_statistics()
            final_count = final_stats.get('total_jobs', 0)
            
            # Report results
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 50)
            logger.info("SCRAPING COMPLETED")
            logger.info("=" * 50)
            logger.info(f"Scraped {len(jobs)} jobs from sitemap")
            logger.info(f"Saved {saved_count} jobs to database")
            logger.info(f"Database now contains {final_count} total jobs")
            logger.info(f"Net new jobs added: {final_count - initial_count}")
            logger.info(f"Time taken: {duration:.2f} seconds")
            logger.info("=" * 50)
            
            # Display top companies and locations
            if final_stats.get('top_companies'):
                logger.info("Top hiring companies:")
                for company, count in list(final_stats['top_companies'].items())[:5]:
                    logger.info(f"  {company}: {count} jobs")
            
            if final_stats.get('top_locations'):
                logger.info("Top job locations:")
                for location, count in list(final_stats['top_locations'].items())[:5]:
                    logger.info(f"  {location}: {count} jobs")
            
        else:
            logger.warning("No jobs found during scraping.")
        
        return jobs
    
    def run_full_extraction(self):
        """Run a complete extraction of all jobs from the website using sitemap"""
        logger.info("Starting FULL EXTRACTION of all jobs from job4freshers.co.in")
        logger.info("Using sitemap-based approach for comprehensive coverage")
        
        # Extract all jobs from sitemap (no limit)
        jobs = self.scrape_job_listings(max_jobs=None)
        
        if jobs:
            saved_count = self.save_jobs_to_db(jobs)
            logger.info(f"FULL EXTRACTION COMPLETED: {saved_count} jobs saved to database")
        else:
            logger.warning("No jobs extracted from sitemap")
        
        return jobs
    
    def export_jobs_to_csv(self, csv_filename: str = None) -> str:
        """Export all jobs from database to CSV file"""
        if csv_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"job4freshers_jobs_{timestamp}.csv"
        
        logger.info(f"Exporting jobs to CSV file: {csv_filename}")
        
        try:
            # Get all jobs from database
            jobs = self.get_all_jobs()
            
            if not jobs:
                logger.warning("No jobs found in database to export")
                return ""
            
            # Define CSV columns - all database fields
            csv_columns = [
                'id', 'title', 'company', 'location', 'experience', 'skills', 
                'salary', 'description', 'posted_date', 'job_type', 'education',
                'eligibility', 'last_date', 'application_link', 'url', 'scraped_at'
            ]
            
            # Write to CSV
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
                writer.writeheader()
                
                for job in jobs:
                    # Clean up the job data for CSV
                    cleaned_job = {}
                    for column in csv_columns:
                        value = job.get(column, '')
                        if value is None:
                            value = ''
                        # Clean up text for CSV
                        if isinstance(value, str):
                            value = value.replace('\n', ' ').replace('\r', ' ').strip()
                        cleaned_job[column] = value
                    
                    writer.writerow(cleaned_job)
            
            logger.info(f"Successfully exported {len(jobs)} jobs to {csv_filename}")
            
            # Generate summary report
            self.generate_csv_export_summary(csv_filename, jobs)
            
            return csv_filename
            
        except Exception as e:
            logger.error(f"Error exporting jobs to CSV: {e}")
            return ""
    
    def generate_csv_export_summary(self, csv_filename: str, jobs: List[Dict]):
        """Generate a summary report for CSV export"""
        logger.info("=" * 60)
        logger.info("CSV EXPORT SUMMARY")
        logger.info("=" * 60)
        logger.info(f"File: {csv_filename}")
        logger.info(f"Total jobs exported: {len(jobs)}")
        logger.info(f"Export time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # File size
        if os.path.exists(csv_filename):
            file_size = os.path.getsize(csv_filename)
            logger.info(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        # Data summary
        companies = set()
        locations = set()
        with_urls = 0
        
        for job in jobs:
            if job.get('company') and job['company'] not in ['N/A', '']:
                companies.add(job['company'])
            if job.get('location') and job['location'] not in ['N/A', '']:
                locations.add(job['location'])
            if job.get('url') and job['url'] not in ['N/A', '']:
                with_urls += 1
        
        logger.info(f"Unique companies: {len(companies)}")
        logger.info(f"Unique locations: {len(locations)}")
        logger.info(f"Jobs with URLs: {with_urls}")
        logger.info(f"Data completeness: {(with_urls/len(jobs)*100):.1f}%")
        logger.info("=" * 60)


if __name__ == "__main__":
    scraper = Job4Fresherscraper()
    
    # Run sitemap-based extraction
    scraper.run_full_extraction()
    
    # Display final statistics
    stats = scraper.get_job_statistics()
    print("\n" + "="*50)
    print("EXTRACTION SUMMARY")
    print("="*50)
    print(f"Total jobs in database: {stats.get('total_jobs', 0)}")
    print(f"Recent jobs (last 7 days): {stats.get('recent_jobs', 0)}")
    print("\nTop companies:")
    for company, count in list(stats.get('top_companies', {}).items())[:5]:
        print(f"  {company}: {count} jobs")
    print("\nTop locations:")
    for location, count in list(stats.get('top_locations', {}).items())[:5]:
        print(f"  {location}: {count} jobs")
    print("="*50)