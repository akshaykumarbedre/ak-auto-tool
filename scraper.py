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
    
    def scrape_job_listings(self, max_pages: int = 50) -> List[Dict]:
        """Scrape job listings from the website with comprehensive pagination"""
        jobs = []
        consecutive_empty_pages = 0
        max_consecutive_empty = 3
        
        logger.info(f"Starting to scrape job listings (max pages: {max_pages})")
        
        for page in range(1, max_pages + 1):
            try:
                # Try multiple URL patterns to ensure we get all jobs
                urls_to_try = [
                    f"{self.base_url}/jobs/page/{page}",
                    f"{self.base_url}/page/{page}",
                    f"{self.base_url}/jobs/{page}",
                    f"{self.base_url}/?page={page}",
                ]
                
                page_jobs = []
                for url in urls_to_try:
                    page_jobs = self.scrape_single_page(url, page)
                    if page_jobs:
                        break  # Found jobs, no need to try other URL patterns
                
                if not page_jobs:
                    consecutive_empty_pages += 1
                    logger.warning(f"No jobs found on page {page}")
                    
                    if consecutive_empty_pages >= max_consecutive_empty:
                        logger.info(f"Stopping after {max_consecutive_empty} consecutive empty pages")
                        break
                else:
                    consecutive_empty_pages = 0
                    jobs.extend(page_jobs)
                    logger.info(f"Found {len(page_jobs)} jobs on page {page} (total: {len(jobs)})")
                
                # Rate limiting to be respectful
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                continue
        
        logger.info(f"Scraping completed. Total jobs found: {len(jobs)}")
        return jobs
    
    def scrape_single_page(self, url: str, page_num: int) -> List[Dict]:
        """Scrape a single page with retry logic"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Scraping page {page_num} (attempt {attempt + 1}): {url}")
                
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                jobs = self.extract_jobs_from_page(soup, url)
                
                return jobs
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed for {url} (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to scrape {url} after {self.max_retries} attempts")
                    return []
        
        return []
    
    def extract_jobs_from_page(self, soup: BeautifulSoup, page_url: str = "") -> List[Dict]:
        """Extract job information from a single page using multiple strategies"""
        jobs = []
        
        # Try multiple strategies to find job listings
        job_selectors = [
            # Common job listing patterns
            {'selector': 'div', 'class_pattern': r'job|listing|card|item|post'},
            {'selector': 'article', 'class_pattern': r'job|listing|card|item|post'},
            {'selector': 'section', 'class_pattern': r'job|listing|card|item|post'},
            {'selector': 'div', 'class_pattern': r'entry|content|main'},
            {'selector': 'li', 'class_pattern': r'job|listing|card|item'},
            
            # Specific patterns for job4freshers (to be updated based on actual structure)
            {'selector': 'div', 'class_pattern': r'.*job.*'},
            {'selector': 'div', 'class_pattern': r'.*post.*'},
            {'selector': 'div', 'class_pattern': r'.*content.*'},
        ]
        
        for selector_config in job_selectors:
            job_elements = soup.find_all(
                selector_config['selector'], 
                class_=re.compile(selector_config['class_pattern'], re.I)
            )
            
            if job_elements:
                logger.info(f"Found {len(job_elements)} potential job elements using {selector_config}")
                
                for element in job_elements:
                    try:
                        job_data = self.extract_job_data(element, page_url)
                        if job_data and self.is_valid_job_data(job_data):
                            jobs.append(job_data)
                    except Exception as e:
                        logger.debug(f"Error extracting job data from element: {e}")
                        continue
                
                # If we found jobs with this selector, use them
                if jobs:
                    break
        
        # If no jobs found with class-based selectors, try to find job links
        if not jobs:
            jobs = self.extract_jobs_from_links(soup, page_url)
        
        return jobs
    
    def extract_job_data(self, element, page_url: str = "") -> Optional[Dict]:
        """Extract comprehensive job data from a job listing element"""
        try:
            # Extract title with multiple strategies
            title = self.extract_text_by_patterns(element, [
                {'tag': ['h1', 'h2', 'h3', 'h4', 'h5'], 'class_pattern': r'title|heading|name'},
                {'tag': ['a'], 'class_pattern': r'title|heading|name'},
                {'tag': ['div', 'span'], 'class_pattern': r'title|heading|name'},
                {'tag': ['strong', 'b'], 'class_pattern': None},
            ])
            
            if not title or title.lower() in ['n/a', 'na', '', ' ']:
                return None
            
            # Extract company
            company = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'company|employer|organization'},
                {'tag': ['a'], 'class_pattern': r'company|employer'},
                {'tag': ['strong', 'b'], 'class_pattern': r'company|employer'},
            ])
            
            # Extract location
            location = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'location|city|place|address'},
                {'tag': ['i'], 'class_pattern': r'location|city|place'},
            ])
            
            # Extract experience
            experience = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'experience|exp|years'},
                {'tag': ['li'], 'class_pattern': r'experience|exp'},
            ])
            
            # Extract skills
            skills = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'skills|technologies|tech|requirements'},
                {'tag': ['ul', 'li'], 'class_pattern': r'skills|tech'},
            ])
            
            # Extract salary
            salary = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'salary|pay|compensation|package|ctc'},
                {'tag': ['strong', 'b'], 'class_pattern': r'salary|pay'},
            ])
            
            # Extract education/eligibility
            education = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'education|qualification|degree|eligible'},
                {'tag': ['li'], 'class_pattern': r'education|qualification'},
            ])
            
            # Extract eligibility
            eligibility = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'eligibility|criteria|requirement'},
                {'tag': ['ul', 'li'], 'class_pattern': r'eligibility|criteria'},
            ])
            
            # Extract last date
            last_date = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'last.*date|deadline|expire|apply.*by'},
                {'tag': ['time'], 'class_pattern': None},
            ])
            
            # Extract job URL and application link
            job_url = ""
            application_link = ""
            
            link_elem = element.find('a', href=True)
            if link_elem:
                job_url = link_elem['href']
                if job_url.startswith('/'):
                    job_url = self.base_url + job_url
                
                # Check if this is an application link
                if any(word in job_url.lower() for word in ['apply', 'application', 'submit']):
                    application_link = job_url
            
            # Extract description
            description = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'p'], 'class_pattern': r'description|summary|content|details'},
                {'tag': ['div'], 'class_pattern': r'excerpt|preview'},
            ])
            
            # If no description found, get all text content (truncated)
            if not description:
                description = element.get_text(strip=True)[:500]
            
            # Extract job type
            job_type = self.extract_text_by_patterns(element, [
                {'tag': ['div', 'span', 'p'], 'class_pattern': r'type|category|mode'},
                {'tag': ['span'], 'class_pattern': r'tag|label'},
            ])
            
            # Clean and validate data
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
                'url': job_url or "N/A"
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job element: {e}")
            return None
    
    def extract_text_by_patterns(self, element, patterns: List[Dict]) -> str:
        """Extract text using multiple patterns"""
        for pattern in patterns:
            tags = pattern['tag']
            class_pattern = pattern.get('class_pattern')
            
            if class_pattern:
                elem = element.find(tags, class_=re.compile(class_pattern, re.I))
            else:
                elem = element.find(tags)
            
            if elem:
                text = elem.get_text(strip=True)
                if text and text.lower() not in ['n/a', 'na', '', ' ']:
                    return text
        
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
    
    def extract_jobs_from_links(self, soup: BeautifulSoup, page_url: str) -> List[Dict]:
        """Extract jobs from job links when direct extraction fails"""
        jobs = []
        
        # Find all links that might lead to job pages
        job_links = soup.find_all('a', href=True)
        
        for link in job_links:
            try:
                href = link['href']
                link_text = link.get_text(strip=True)
                
                # Check if this looks like a job link
                if self.is_job_link(href, link_text):
                    job_url = href
                    if job_url.startswith('/'):
                        job_url = self.base_url + job_url
                    
                    # Create basic job data from link
                    job_data = {
                        'title': link_text,
                        'company': "N/A",
                        'location': "N/A",
                        'experience': "N/A",
                        'skills': "N/A",
                        'salary': "N/A",
                        'description': "N/A",
                        'posted_date': datetime.now().strftime('%Y-%m-%d'),
                        'job_type': "Full-time",
                        'education': "N/A",
                        'eligibility': "N/A",
                        'last_date': "N/A",
                        'application_link': "N/A",
                        'url': job_url
                    }
                    
                    if self.is_valid_job_data(job_data):
                        jobs.append(job_data)
                        
            except Exception as e:
                logger.debug(f"Error processing job link: {e}")
                continue
        
        return jobs
    
    def is_job_link(self, href: str, link_text: str) -> bool:
        """Check if a link is likely to be a job link"""
        if not href or not link_text:
            return False
        
        # Check URL patterns
        job_url_patterns = [
            r'/job/', r'/jobs/', r'/position/', r'/career/',
            r'/vacancy/', r'/opening/', r'/recruitment/'
        ]
        
        for pattern in job_url_patterns:
            if re.search(pattern, href, re.I):
                return True
        
        # Check link text patterns
        job_text_patterns = [
            r'developer', r'engineer', r'manager', r'analyst',
            r'coordinator', r'executive', r'associate', r'specialist',
            r'intern', r'trainee', r'assistant', r'consultant'
        ]
        
        for pattern in job_text_patterns:
            if re.search(pattern, link_text, re.I):
                return True
        
        return False
    
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
    
    def run_scraper(self, max_pages: int = 50):
        """Run the complete comprehensive scraping process"""
        logger.info("Starting comprehensive job scraping process...")
        logger.info(f"Target: Extract ALL job posts from {self.base_url}")
        logger.info(f"Maximum pages to scrape: {max_pages}")
        
        start_time = datetime.now()
        
        # Get initial database count
        initial_stats = self.get_job_statistics()
        initial_count = initial_stats.get('total_jobs', 0)
        logger.info(f"Initial database contains {initial_count} jobs")
        
        # Run the scraping
        jobs = self.scrape_job_listings(max_pages)
        
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
            logger.info(f"Scraped {len(jobs)} jobs from {max_pages} pages")
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
        """Run a complete extraction of all jobs from the website"""
        logger.info("Starting FULL EXTRACTION of all jobs from job4freshers.co.in")
        
        # Start with a large number of pages to ensure we get everything
        max_pages = 100
        
        # Try multiple extraction strategies
        all_jobs = []
        
        # Strategy 1: Standard pagination
        logger.info("Strategy 1: Standard pagination")
        jobs1 = self.scrape_job_listings(max_pages)
        all_jobs.extend(jobs1)
        
        # Strategy 2: Try different URL patterns
        logger.info("Strategy 2: Alternative URL patterns")
        jobs2 = self.scrape_with_alternative_urls(max_pages)
        all_jobs.extend(jobs2)
        
        # Remove duplicates based on URL
        unique_jobs = []
        seen_urls = set()
        
        for job in all_jobs:
            url = job.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_jobs.append(job)
        
        logger.info(f"Found {len(all_jobs)} total jobs, {len(unique_jobs)} unique jobs")
        
        if unique_jobs:
            saved_count = self.save_jobs_to_db(unique_jobs)
            logger.info(f"FULL EXTRACTION COMPLETED: {saved_count} jobs saved to database")
        
        return unique_jobs
    
    def scrape_with_alternative_urls(self, max_pages: int) -> List[Dict]:
        """Try scraping with alternative URL patterns"""
        jobs = []
        
        # Alternative URL patterns to try
        url_patterns = [
            f"{self.base_url}/category/jobs/page/{{page}}",
            f"{self.base_url}/jobs/all/page/{{page}}",
            f"{self.base_url}/all-jobs/page/{{page}}",
            f"{self.base_url}/latest-jobs/page/{{page}}",
        ]
        
        for pattern in url_patterns:
            logger.info(f"Trying URL pattern: {pattern}")
            
            for page in range(1, min(max_pages, 10) + 1):  # Limit alternative patterns
                try:
                    url = pattern.format(page=page)
                    page_jobs = self.scrape_single_page(url, page)
                    
                    if page_jobs:
                        jobs.extend(page_jobs)
                        logger.info(f"Found {len(page_jobs)} jobs with pattern {pattern} page {page}")
                    else:
                        break  # No jobs found, try next pattern
                        
                except Exception as e:
                    logger.debug(f"Error with pattern {pattern}: {e}")
                    break
        
        return jobs

if __name__ == "__main__":
    scraper = Job4Fresherscraper()
    
    # Run comprehensive extraction
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