#!/usr/bin/env python3
"""
Test script for the new sitemap-based job extraction
"""

import logging
from scraper import Job4Fresherscraper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_job_url_filtering():
    """Test the job URL filtering logic"""
    scraper = Job4Fresherscraper()
    
    # Test URLs
    test_urls = [
        # Job URLs (should return True)
        "https://job4freshers.co.in/optum-off-campus-data-analyst/",
        "https://job4freshers.co.in/qualcomm-associate-engineer/",
        "https://job4freshers.co.in/microsoft-software-developer/",
        "https://job4freshers.co.in/google-data-scientist-intern/",
        
        # Non-job URLs (should return False)
        "https://job4freshers.co.in/latest-government-jobs/",
        "https://job4freshers.co.in/job-by-location-2/",
        "https://job4freshers.co.in/category/tech-jobs/",
        "https://job4freshers.co.in/tag/software/",
        "https://job4freshers.co.in/author/admin/",
        "https://job4freshers.co.in/sitemap/",
        "https://job4freshers.co.in/contact/",
        "https://job4freshers.co.in/about/",
    ]
    
    job_patterns = scraper.get_job_url_patterns()
    non_job_patterns = scraper.get_non_job_url_patterns()
    
    logger.info("Testing job URL filtering...")
    logger.info(f"Job patterns: {job_patterns}")
    logger.info(f"Non-job patterns: {non_job_patterns}")
    
    for url in test_urls:
        is_job = scraper.is_job_url(url, job_patterns, non_job_patterns)
        expected = "job" if any(keyword in url for keyword in ["optum", "qualcomm", "microsoft", "google"]) else "non-job"
        status = "✅" if ((is_job and expected == "job") or (not is_job and expected == "non-job")) else "❌"
        logger.info(f"{status} {url} -> {is_job} (expected: {expected})")

def test_sitemap_extraction():
    """Test the sitemap extraction (without actually calling the website)"""
    scraper = Job4Fresherscraper()
    
    logger.info("Testing sitemap extraction logic...")
    logger.info(f"Base URL: {scraper.base_url}")
    logger.info(f"Sitemap URL: {scraper.base_url}/sitemap/")
    
    # Test the job URL patterns
    test_job_url_filtering()
    
    logger.info("Sitemap extraction test completed")

def test_job_data_validation():
    """Test job data validation"""
    scraper = Job4Fresherscraper()
    
    # Valid job data
    valid_job = {
        'title': 'Software Engineer',
        'company': 'Tech Corp',
        'location': 'Bangalore',
        'experience': '2-4 years',
        'skills': 'Python, Java',
        'salary': '8-12 LPA',
        'description': 'Great opportunity for software engineers...',
        'posted_date': '2024-01-01',
        'job_type': 'Full-time',
        'education': 'B.Tech',
        'eligibility': 'Fresh graduates',
        'last_date': '2024-02-01',
        'application_link': 'https://example.com/apply',
        'url': 'https://job4freshers.co.in/tech-corp-software-engineer/'
    }
    
    # Invalid job data
    invalid_job = {
        'title': '',
        'company': 'N/A',
        'location': 'N/A'
    }
    
    logger.info("Testing job data validation...")
    logger.info(f"Valid job data: {scraper.is_valid_job_data(valid_job)}")
    logger.info(f"Invalid job data: {scraper.is_valid_job_data(invalid_job)}")

if __name__ == "__main__":
    logger.info("Starting sitemap extraction tests...")
    
    try:
        test_sitemap_extraction()
        test_job_data_validation()
        logger.info("✅ All tests completed successfully")
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")