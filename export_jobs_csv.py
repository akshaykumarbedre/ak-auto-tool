#!/usr/bin/env python3
"""
Job4Freshers CSV Export Script

This script exports all jobs from the database to a CSV file for storage in GitHub.
"""

import logging
import sys
import os
from datetime import datetime
from scraper import Job4Fresherscraper
from extract_all_jobs import JobExtractionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csv_export.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run job extraction and CSV export"""
    logger.info("=" * 60)
    logger.info("JOB4FRESHERS CSV EXPORT SCRIPT")
    logger.info("=" * 60)
    logger.info(f"Start time: {datetime.now()}")
    
    try:
        # Initialize extraction manager
        extraction_manager = JobExtractionManager()
        
        # Check if database has data
        stats = extraction_manager.scraper.get_job_statistics()
        total_jobs = stats.get('total_jobs', 0)
        
        if total_jobs == 0:
            logger.info("Database is empty. Running full extraction first...")
            # Run extraction with CSV export
            jobs = extraction_manager.run_complete_extraction(export_csv=True)
            
            if not jobs:
                logger.warning("No jobs were extracted. Creating sample CSV with demo data...")
                create_sample_csv()
            
        else:
            logger.info(f"Database contains {total_jobs} jobs. Exporting to CSV...")
            # Just export existing data to CSV
            csv_filename = extraction_manager.export_to_csv()
            
            if csv_filename:
                logger.info(f"✅ Export completed successfully: {csv_filename}")
            else:
                logger.error("❌ Export failed")
        
        logger.info("=" * 60)
        logger.info("CSV EXPORT SCRIPT COMPLETED")
        logger.info(f"End time: {datetime.now()}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Script failed: {e}")
        sys.exit(1)

def create_sample_csv():
    """Create a sample CSV file with demo job data"""
    logger.info("Creating sample CSV file with demo job data...")
    
    # Generate sample data
    sample_jobs = [
        {
            'id': 1,
            'title': 'Software Engineer - Entry Level',
            'company': 'Tech Solutions Inc',
            'location': 'Bangalore, Karnataka',
            'experience': '0-1 years',
            'skills': 'Python, Java, SQL, Git',
            'salary': '3-5 LPA',
            'description': 'Looking for fresh graduates with programming skills in Python and Java. Good understanding of databases and version control systems required.',
            'posted_date': '2024-01-15',
            'job_type': 'Full-time',
            'education': 'B.Tech/BE in Computer Science',
            'eligibility': 'Fresh graduates with strong programming fundamentals',
            'last_date': '2024-02-15',
            'application_link': 'https://job4freshers.co.in/tech-solutions-software-engineer/',
            'url': 'https://job4freshers.co.in/tech-solutions-software-engineer/',
            'scraped_at': '2024-01-10 10:30:00'
        },
        {
            'id': 2,
            'title': 'Data Analyst - Fresher',
            'company': 'Analytics Corp',
            'location': 'Mumbai, Maharashtra',
            'experience': '0-2 years',
            'skills': 'Excel, SQL, Python, Power BI',
            'salary': '2.5-4 LPA',
            'description': 'Entry-level data analyst position for candidates with analytical skills and knowledge of data visualization tools.',
            'posted_date': '2024-01-12',
            'job_type': 'Full-time',
            'education': 'B.Tech/BE, BCA, MCA',
            'eligibility': 'Strong analytical skills and knowledge of data tools',
            'last_date': '2024-02-10',
            'application_link': 'https://job4freshers.co.in/analytics-corp-data-analyst/',
            'url': 'https://job4freshers.co.in/analytics-corp-data-analyst/',
            'scraped_at': '2024-01-10 11:15:00'
        },
        {
            'id': 3,
            'title': 'Business Analyst - Graduate Trainee',
            'company': 'Consulting Services Ltd',
            'location': 'Hyderabad, Telangana',
            'experience': '0-1 years',
            'skills': 'Business Analysis, Excel, Communication, Problem Solving',
            'salary': '3-4.5 LPA',
            'description': 'Graduate trainee program for business analyst role. Training will be provided on business analysis methodologies and tools.',
            'posted_date': '2024-01-08',
            'job_type': 'Full-time',
            'education': 'MBA, B.Tech, BBA',
            'eligibility': 'Fresh graduates with good communication skills',
            'last_date': '2024-02-05',
            'application_link': 'https://job4freshers.co.in/consulting-services-business-analyst/',
            'url': 'https://job4freshers.co.in/consulting-services-business-analyst/',
            'scraped_at': '2024-01-10 12:00:00'
        }
    ]
    
    # Create CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"job4freshers_sample_jobs_{timestamp}.csv"
    
    import csv
    csv_columns = [
        'id', 'title', 'company', 'location', 'experience', 'skills', 
        'salary', 'description', 'posted_date', 'job_type', 'education',
        'eligibility', 'last_date', 'application_link', 'url', 'scraped_at'
    ]
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(sample_jobs)
    
    logger.info(f"Sample CSV created: {csv_filename}")
    logger.info(f"Sample data contains {len(sample_jobs)} job records")
    
    return csv_filename

if __name__ == "__main__":
    main()