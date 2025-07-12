# Job4Freshers CSV Export Documentation

## Overview
This document describes the CSV export functionality for job data extracted from job4freshers.co.in.

## CSV Files
- **job4freshers_jobs_data.csv**: The main CSV file containing all extracted job data
- **job4freshers_jobs_YYYYMMDD_HHMMSS.csv**: Timestamped CSV files for specific extraction runs

## CSV File Structure
The CSV file contains the following columns:

| Column | Description |
|--------|-------------|
| id | Unique job ID |
| title | Job title |
| company | Company name |
| location | Job location |
| experience | Required experience |
| skills | Required skills (comma-separated) |
| salary | Salary range |
| description | Job description |
| posted_date | Date when job was posted |
| job_type | Type of job (Full-time, Part-time, etc.) |
| education | Educational requirements |
| eligibility | Eligibility criteria |
| last_date | Application deadline |
| application_link | Direct link to apply |
| url | Job posting URL |
| scraped_at | Date and time when data was scraped |

## How to Export Jobs to CSV

### Method 1: Using the Enhanced Scraper
```python
from scraper import Job4Fresherscraper

# Initialize scraper
scraper = Job4Fresherscraper()

# Run extraction (if needed)
jobs = scraper.run_full_extraction()

# Export to CSV
csv_filename = scraper.export_jobs_to_csv()
print(f"Jobs exported to: {csv_filename}")
```

### Method 2: Using the Extraction Manager
```python
from extract_all_jobs import JobExtractionManager

# Initialize manager
manager = JobExtractionManager()

# Run complete extraction with CSV export
jobs = manager.run_complete_extraction(export_csv=True)
```

### Method 3: Create Sample CSV
```python
# Run the sample CSV creation script
python create_sample_csv.py
```

## CSV Export Features

### Automatic CSV Generation
- CSV files are automatically generated with timestamps
- Data is cleaned and formatted for CSV compatibility
- File size and statistics are reported

### Data Quality
- All database fields are included
- Text fields are cleaned (newlines removed)
- Missing values are handled appropriately
- UTF-8 encoding for international characters

### Export Statistics
The export process provides:
- Total number of jobs exported
- File size information
- Data completeness metrics
- Company and location statistics

## File Storage
- CSV files are stored in the repository root
- Files are tracked by Git for version control
- Standard naming convention: `job4freshers_jobs_YYYYMMDD_HHMMSS.csv`
- Main data file: `job4freshers_jobs_data.csv`

## Usage Examples

### Load CSV in Python
```python
import pandas as pd

# Load the CSV file
df = pd.read_csv('job4freshers_jobs_data.csv')
print(f"Loaded {len(df)} jobs")
print(df.head())
```

### Load CSV in Excel
1. Open Excel
2. Go to Data → Get Data → From File → From CSV
3. Select the CSV file
4. Follow the import wizard

### View CSV Statistics
```python
import pandas as pd

df = pd.read_csv('job4freshers_jobs_data.csv')

# Basic statistics
print(f"Total jobs: {len(df)}")
print(f"Unique companies: {df['company'].nunique()}")
print(f"Unique locations: {df['location'].nunique()}")

# Top companies
print("\nTop hiring companies:")
print(df['company'].value_counts().head(10))

# Top locations
print("\nTop job locations:")
print(df['location'].value_counts().head(10))
```

## Data Integration
The CSV files can be easily integrated into:
- Data analysis tools (Excel, Google Sheets)
- Business intelligence platforms
- Machine learning pipelines
- Database systems
- Web applications

## Automated Updates
The extraction system can be run periodically to:
- Update the CSV file with new job postings
- Maintain historical data
- Track job market trends
- Generate regular reports

## Data Schema
The CSV follows a standardized schema that matches the database structure:
- All fields are text-based for compatibility
- Date fields use ISO format (YYYY-MM-DD)
- Skills are comma-separated for easy parsing
- URLs are fully qualified

This CSV export functionality enables easy data sharing, analysis, and integration with external systems.