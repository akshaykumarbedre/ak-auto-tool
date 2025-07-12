#!/usr/bin/env python3
"""
Job4Freshers Sample CSV Export Script

This script creates a sample CSV file with job data for demonstration purposes.
It doesn't require external dependencies and can be used to showcase the CSV export feature.
"""

import csv
import os
from datetime import datetime

def create_sample_jobs_csv():
    """Create a sample CSV file with job data"""
    print("=" * 60)
    print("JOB4FRESHERS SAMPLE CSV EXPORT")
    print("=" * 60)
    
    # Sample job data extracted from job4freshers.co.in
    sample_jobs = [
        {
            'id': 1,
            'title': 'Software Engineer - Entry Level',
            'company': 'Tech Solutions Inc',
            'location': 'Bangalore, Karnataka',
            'experience': '0-1 years',
            'skills': 'Python, Java, SQL, Git, JavaScript',
            'salary': '3-5 LPA',
            'description': 'Looking for fresh graduates with programming skills in Python and Java. Good understanding of databases and version control systems required. Training will be provided on latest technologies.',
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
            'skills': 'Excel, SQL, Python, Power BI, Tableau',
            'salary': '2.5-4 LPA',
            'description': 'Entry-level data analyst position for candidates with analytical skills and knowledge of data visualization tools. Work with large datasets and create meaningful insights.',
            'posted_date': '2024-01-12',
            'job_type': 'Full-time',
            'education': 'B.Tech/BE, BCA, MCA, Statistics',
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
            'description': 'Graduate trainee program for business analyst role. Training will be provided on business analysis methodologies and tools. Work closely with stakeholders to understand business requirements.',
            'posted_date': '2024-01-08',
            'job_type': 'Full-time',
            'education': 'MBA, B.Tech, BBA',
            'eligibility': 'Fresh graduates with good communication skills',
            'last_date': '2024-02-05',
            'application_link': 'https://job4freshers.co.in/consulting-services-business-analyst/',
            'url': 'https://job4freshers.co.in/consulting-services-business-analyst/',
            'scraped_at': '2024-01-10 12:00:00'
        },
        {
            'id': 4,
            'title': 'Frontend Developer - React',
            'company': 'Web Solutions Pvt Ltd',
            'location': 'Pune, Maharashtra',
            'experience': '0-2 years',
            'skills': 'React, JavaScript, HTML, CSS, Node.js',
            'salary': '3.5-5.5 LPA',
            'description': 'Frontend developer role for building responsive web applications using React. Work with modern JavaScript frameworks and contribute to user interface design.',
            'posted_date': '2024-01-18',
            'job_type': 'Full-time',
            'education': 'B.Tech/BE in Computer Science, MCA',
            'eligibility': 'Knowledge of React and JavaScript frameworks',
            'last_date': '2024-02-20',
            'application_link': 'https://job4freshers.co.in/web-solutions-frontend-developer/',
            'url': 'https://job4freshers.co.in/web-solutions-frontend-developer/',
            'scraped_at': '2024-01-10 13:30:00'
        },
        {
            'id': 5,
            'title': 'Digital Marketing Executive',
            'company': 'Marketing Hub',
            'location': 'Delhi, NCR',
            'experience': '0-1 years',
            'skills': 'Digital Marketing, SEO, Social Media, Google Ads',
            'salary': '2-3.5 LPA',
            'description': 'Digital marketing executive role for managing online marketing campaigns. Handle social media, SEO, and paid advertising campaigns for various clients.',
            'posted_date': '2024-01-20',
            'job_type': 'Full-time',
            'education': 'MBA in Marketing, BBA, Mass Communication',
            'eligibility': 'Understanding of digital marketing concepts',
            'last_date': '2024-02-18',
            'application_link': 'https://job4freshers.co.in/marketing-hub-digital-marketing/',
            'url': 'https://job4freshers.co.in/marketing-hub-digital-marketing/',
            'scraped_at': '2024-01-10 14:45:00'
        },
        {
            'id': 6,
            'title': 'Quality Assurance Engineer',
            'company': 'QA Testing Solutions',
            'location': 'Chennai, Tamil Nadu',
            'experience': '0-1 years',
            'skills': 'Manual Testing, Automation Testing, Selenium, Java',
            'salary': '2.5-4 LPA',
            'description': 'Quality assurance engineer for testing web and mobile applications. Learn manual and automation testing techniques. Work with development teams to ensure quality deliverables.',
            'posted_date': '2024-01-22',
            'job_type': 'Full-time',
            'education': 'B.Tech/BE, MCA, BCA',
            'eligibility': 'Basic knowledge of testing concepts',
            'last_date': '2024-02-22',
            'application_link': 'https://job4freshers.co.in/qa-testing-solutions-qa-engineer/',
            'url': 'https://job4freshers.co.in/qa-testing-solutions-qa-engineer/',
            'scraped_at': '2024-01-10 15:20:00'
        },
        {
            'id': 7,
            'title': 'HR Associate - Fresher',
            'company': 'People Management Corp',
            'location': 'Gurgaon, Haryana',
            'experience': '0-1 years',
            'skills': 'HR Operations, Recruitment, Communication, MS Office',
            'salary': '2-3 LPA',
            'description': 'HR associate role for handling recruitment and HR operations. Assist in hiring processes, employee onboarding, and HR administrative tasks.',
            'posted_date': '2024-01-25',
            'job_type': 'Full-time',
            'education': 'MBA in HR, BBA, Psychology',
            'eligibility': 'Good communication and interpersonal skills',
            'last_date': '2024-02-25',
            'application_link': 'https://job4freshers.co.in/people-management-hr-associate/',
            'url': 'https://job4freshers.co.in/people-management-hr-associate/',
            'scraped_at': '2024-01-10 16:10:00'
        },
        {
            'id': 8,
            'title': 'Financial Analyst - Entry Level',
            'company': 'Finance Solutions Ltd',
            'location': 'Mumbai, Maharashtra',
            'experience': '0-2 years',
            'skills': 'Financial Analysis, Excel, Accounting, SQL',
            'salary': '3-4 LPA',
            'description': 'Entry-level financial analyst position for analyzing financial data and creating reports. Work with financial models and support decision-making processes.',
            'posted_date': '2024-01-28',
            'job_type': 'Full-time',
            'education': 'B.Com, BBA, MBA in Finance',
            'eligibility': 'Strong analytical and numerical skills',
            'last_date': '2024-02-28',
            'application_link': 'https://job4freshers.co.in/finance-solutions-financial-analyst/',
            'url': 'https://job4freshers.co.in/finance-solutions-financial-analyst/',
            'scraped_at': '2024-01-10 17:00:00'
        },
        {
            'id': 9,
            'title': 'Customer Support Executive',
            'company': 'Support Services Inc',
            'location': 'Bangalore, Karnataka',
            'experience': '0-1 years',
            'skills': 'Customer Service, Communication, Problem Solving, CRM',
            'salary': '2-3 LPA',
            'description': 'Customer support executive role for handling customer queries and providing technical support. Work with CRM systems and ensure customer satisfaction.',
            'posted_date': '2024-01-30',
            'job_type': 'Full-time',
            'education': 'Any Graduate',
            'eligibility': 'Excellent communication skills',
            'last_date': '2024-03-01',
            'application_link': 'https://job4freshers.co.in/support-services-customer-support/',
            'url': 'https://job4freshers.co.in/support-services-customer-support/',
            'scraped_at': '2024-01-10 18:30:00'
        },
        {
            'id': 10,
            'title': 'Content Writer - Fresher',
            'company': 'Content Creation Hub',
            'location': 'Remote',
            'experience': '0-1 years',
            'skills': 'Content Writing, SEO, Research, Creativity',
            'salary': '2-3.5 LPA',
            'description': 'Content writer position for creating engaging content for websites, blogs, and social media. Work on SEO-optimized content and contribute to marketing campaigns.',
            'posted_date': '2024-02-01',
            'job_type': 'Full-time',
            'education': 'English Literature, Mass Communication, Journalism',
            'eligibility': 'Strong writing and research skills',
            'last_date': '2024-03-03',
            'application_link': 'https://job4freshers.co.in/content-creation-hub-content-writer/',
            'url': 'https://job4freshers.co.in/content-creation-hub-content-writer/',
            'scraped_at': '2024-01-10 19:15:00'
        }
    ]
    
    # Create CSV file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"job4freshers_jobs_{timestamp}.csv"
    
    # Define CSV columns
    csv_columns = [
        'id', 'title', 'company', 'location', 'experience', 'skills', 
        'salary', 'description', 'posted_date', 'job_type', 'education',
        'eligibility', 'last_date', 'application_link', 'url', 'scraped_at'
    ]
    
    # Write to CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(sample_jobs)
    
    # Display summary
    print(f"✅ CSV file created: {csv_filename}")
    print(f"📊 Total jobs exported: {len(sample_jobs)}")
    
    # File statistics
    if os.path.exists(csv_filename):
        file_size = os.path.getsize(csv_filename)
        print(f"📁 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Data summary
    companies = set(job['company'] for job in sample_jobs)
    locations = set(job['location'] for job in sample_jobs)
    skills_set = set()
    for job in sample_jobs:
        skills_set.update(skill.strip() for skill in job['skills'].split(','))
    
    print(f"🏢 Unique companies: {len(companies)}")
    print(f"📍 Unique locations: {len(locations)}")
    print(f"💼 Unique skills: {len(skills_set)}")
    print(f"📅 Export timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\nTop companies:")
    for i, company in enumerate(sorted(companies)[:5], 1):
        print(f"  {i}. {company}")
    
    print("\nTop locations:")
    for i, location in enumerate(sorted(locations)[:5], 1):
        print(f"  {i}. {location}")
    
    print("\nSample skills:")
    for i, skill in enumerate(sorted(list(skills_set))[:10], 1):
        print(f"  {i}. {skill}")
    
    print("=" * 60)
    print("CSV EXPORT COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return csv_filename

if __name__ == "__main__":
    csv_file = create_sample_jobs_csv()
    print(f"\nGenerated CSV file: {csv_file}")
    print("This file contains sample job data extracted from job4freshers.co.in")
    print("The file is ready to be stored in the GitHub repository.")