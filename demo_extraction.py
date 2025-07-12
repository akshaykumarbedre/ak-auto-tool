#!/usr/bin/env python3
"""
Demo Script for Job4Freshers Complete Job Extraction

This script demonstrates the complete job extraction functionality,
including creating sample data and running all the components.
"""

import os
import logging
from datetime import datetime
from scraper import Job4Fresherscraper
from extract_all_jobs import JobExtractionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_jobs():
    """Create sample job data for demonstration"""
    return [
        {
            'title': 'Python Developer',
            'company': 'Tech Innovations Ltd',
            'location': 'Bangalore',
            'experience': '2-3 years',
            'skills': 'Python, Django, REST API, PostgreSQL',
            'salary': '6-9 LPA',
            'description': 'We are looking for an experienced Python developer to join our team. Must have experience with Django framework and REST API development.',
            'posted_date': '2024-01-15',
            'job_type': 'Full-time',
            'education': 'B.Tech/B.E in Computer Science',
            'eligibility': 'BE/BTech/MCA with 2+ years experience',
            'last_date': '2024-02-15',
            'application_link': 'https://job4freshers.co.in/apply/python-dev-1',
            'url': 'https://job4freshers.co.in/job/python-developer-tech-innovations'
        },
        {
            'title': 'Data Scientist',
            'company': 'Analytics Pro Solutions',
            'location': 'Mumbai',
            'experience': '1-2 years',
            'skills': 'Python, Machine Learning, Pandas, NumPy, Scikit-learn',
            'salary': '7-12 LPA',
            'description': 'Entry-level data scientist position with excellent growth opportunities. Work on cutting-edge ML projects.',
            'posted_date': '2024-01-16',
            'job_type': 'Full-time',
            'education': 'M.Tech/MCA in relevant field',
            'eligibility': 'Masters degree in Computer Science, Statistics or related field',
            'last_date': '2024-02-20',
            'application_link': 'https://job4freshers.co.in/apply/data-scientist-1',
            'url': 'https://job4freshers.co.in/job/data-scientist-analytics-pro'
        },
        {
            'title': 'Frontend Developer',
            'company': 'Web Solutions Inc',
            'location': 'Remote',
            'experience': 'Fresher',
            'skills': 'JavaScript, React, HTML5, CSS3, Bootstrap',
            'salary': '3-5 LPA',
            'description': 'Fresher-friendly frontend developer position. Training provided for React and modern web technologies.',
            'posted_date': '2024-01-17',
            'job_type': 'Full-time',
            'education': 'B.Tech/BCA/MCA',
            'eligibility': 'Any graduate with basic programming knowledge',
            'last_date': '2024-02-10',
            'application_link': 'https://job4freshers.co.in/apply/frontend-dev-1',
            'url': 'https://job4freshers.co.in/job/frontend-developer-web-solutions'
        },
        {
            'title': 'Java Developer',
            'company': 'Enterprise Systems Ltd',
            'location': 'Hyderabad',
            'experience': '3-5 years',
            'skills': 'Java, Spring Boot, Microservices, MySQL',
            'salary': '8-12 LPA',
            'description': 'Senior Java developer role working on enterprise applications. Experience with microservices architecture required.',
            'posted_date': '2024-01-18',
            'job_type': 'Full-time',
            'education': 'B.Tech/M.Tech in Computer Science',
            'eligibility': 'Engineering graduate with 3+ years Java experience',
            'last_date': '2024-02-25',
            'application_link': 'https://job4freshers.co.in/apply/java-dev-1',
            'url': 'https://job4freshers.co.in/job/java-developer-enterprise-systems'
        },
        {
            'title': 'DevOps Engineer',
            'company': 'Cloud First Technologies',
            'location': 'Pune',
            'experience': '2-4 years',
            'skills': 'Docker, Kubernetes, AWS, Jenkins, Git',
            'salary': '7-10 LPA',
            'description': 'DevOps engineer role focused on cloud infrastructure and CI/CD pipelines. AWS certification preferred.',
            'posted_date': '2024-01-19',
            'job_type': 'Full-time',
            'education': 'B.Tech/B.E in relevant field',
            'eligibility': 'Engineering graduate with cloud experience',
            'last_date': '2024-02-28',
            'application_link': 'https://job4freshers.co.in/apply/devops-1',
            'url': 'https://job4freshers.co.in/job/devops-engineer-cloud-first'
        },
        {
            'title': 'Mobile App Developer',
            'company': 'Mobile Innovations',
            'location': 'Chennai',
            'experience': '1-3 years',
            'skills': 'Flutter, Dart, Android, iOS, Firebase',
            'salary': '5-8 LPA',
            'description': 'Mobile app developer specializing in Flutter development. Work on innovative mobile applications.',
            'posted_date': '2024-01-20',
            'job_type': 'Full-time',
            'education': 'B.Tech/MCA',
            'eligibility': 'Any graduate with mobile development experience',
            'last_date': '2024-02-18',
            'application_link': 'https://job4freshers.co.in/apply/mobile-dev-1',
            'url': 'https://job4freshers.co.in/job/mobile-developer-innovations'
        },
        {
            'title': 'Software Test Engineer',
            'company': 'Quality Assurance Corp',
            'location': 'Bangalore',
            'experience': '1-2 years',
            'skills': 'Manual Testing, Selenium, TestNG, API Testing',
            'salary': '4-6 LPA',
            'description': 'Software test engineer role with focus on both manual and automated testing. Selenium experience preferred.',
            'posted_date': '2024-01-21',
            'job_type': 'Full-time',
            'education': 'B.Tech/B.E/MCA',
            'eligibility': 'Engineering graduate with testing knowledge',
            'last_date': '2024-02-22',
            'application_link': 'https://job4freshers.co.in/apply/test-engineer-1',
            'url': 'https://job4freshers.co.in/job/test-engineer-qa-corp'
        },
        {
            'title': 'Full Stack Developer',
            'company': 'Startup Hub',
            'location': 'Gurgaon',
            'experience': '2-4 years',
            'skills': 'MEAN Stack, Node.js, Angular, MongoDB',
            'salary': '6-10 LPA',
            'description': 'Full stack developer role in a fast-paced startup environment. MEAN stack experience required.',
            'posted_date': '2024-01-22',
            'job_type': 'Full-time',
            'education': 'B.Tech/MCA',
            'eligibility': 'Graduate with full stack development experience',
            'last_date': '2024-02-12',
            'application_link': 'https://job4freshers.co.in/apply/fullstack-dev-1',
            'url': 'https://job4freshers.co.in/job/fullstack-developer-startup-hub'
        }
    ]

def main():
    """Main demo function"""
    print("=" * 80)
    print("JOB4FRESHERS COMPLETE JOB EXTRACTION SYSTEM DEMO")
    print("=" * 80)
    
    db_path = "demo_jobs.db"
    
    # Clean up previous demo database
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info("Cleaned up previous demo database")
    
    # Create extraction manager
    manager = JobExtractionManager(db_path)
    
    # Create sample jobs to simulate extraction
    sample_jobs = create_sample_jobs()
    logger.info(f"Created {len(sample_jobs)} sample jobs")
    
    # Save sample jobs to database
    saved_count = manager.scraper.save_jobs_to_db(sample_jobs)
    logger.info(f"Saved {saved_count} jobs to database")
    
    # Generate comprehensive report
    stats = manager.scraper.get_job_statistics()
    manager.generate_extraction_report(0, len(sample_jobs), sample_jobs, stats)
    
    # Demonstrate search functionality
    print("\n" + "=" * 80)
    print("SEARCH FUNCTIONALITY DEMO")
    print("=" * 80)
    
    # Test different search queries
    test_queries = [
        "Python developer",
        "Data science jobs",
        "Frontend developer remote",
        "Java developer Hyderabad",
        "Fresher positions"
    ]
    
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        
        # Simple search through database
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Search in title, skills, and description
        cursor.execute("""
            SELECT title, company, location, skills, salary 
            FROM jobs 
            WHERE title LIKE ? OR skills LIKE ? OR description LIKE ?
            LIMIT 3
        """, (f"%{query}%", f"%{query}%", f"%{query}%"))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            for i, (title, company, location, skills, salary) in enumerate(results, 1):
                print(f"  {i}. {title} at {company}")
                print(f"     Location: {location}, Salary: {salary}")
                print(f"     Skills: {skills}")
        else:
            print("  No matches found")
    
    # Display final statistics
    print("\n" + "=" * 80)
    print("FINAL STATISTICS")
    print("=" * 80)
    print(f"Total jobs in database: {stats['total_jobs']}")
    print(f"Recent jobs (last 7 days): {stats['recent_jobs']}")
    
    print("\nTop Companies:")
    for i, (company, count) in enumerate(list(stats['top_companies'].items())[:5], 1):
        print(f"  {i}. {company}: {count} jobs")
    
    print("\nTop Locations:")
    for i, (location, count) in enumerate(list(stats['top_locations'].items())[:5], 1):
        print(f"  {i}. {location}: {count} jobs")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"Demo database created: {db_path}")
    print("You can now:")
    print("  1. Run the Flask app: python3 app.py")
    print("  2. Use the extraction script: python3 extract_all_jobs.py")
    print("  3. Access the web interface at http://localhost:5000")
    print("=" * 80)

if __name__ == "__main__":
    main()