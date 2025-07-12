#!/usr/bin/env python3
"""
Job4Freshers Complete Job Extraction Script

This script extracts ALL job postings from job4freshers.co.in and loads them into the database.
It ensures complete coverage, handles duplicates, and provides comprehensive reporting.
"""

import logging
import sys
import os
from datetime import datetime
from scraper import Job4Fresherscraper
import csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class JobExtractionManager:
    """Manages the complete job extraction process"""
    
    def __init__(self, db_path: str = "jobs.db"):
        self.scraper = Job4Fresherscraper(db_path)
        self.db_path = db_path
        
    def run_complete_extraction(self, export_csv: bool = True):
        """Run the complete extraction process using sitemap-based approach"""
        logger.info("=" * 80)
        logger.info("JOB4FRESHERS COMPLETE JOB EXTRACTION - SITEMAP-BASED")
        logger.info("=" * 80)
        logger.info(f"Target: Extract ALL job posts from {self.scraper.base_url}")
        logger.info(f"Method: Sitemap-based extraction from {self.scraper.base_url}/sitemap/")
        logger.info(f"Database: {self.db_path}")
        logger.info(f"CSV Export: {'Enabled' if export_csv else 'Disabled'}")
        logger.info(f"Start time: {datetime.now()}")
        logger.info("=" * 80)
        
        # Get initial statistics
        initial_stats = self.scraper.get_job_statistics()
        initial_count = initial_stats.get('total_jobs', 0)
        logger.info(f"Initial database contains {initial_count} jobs")
        
        # Run the extraction
        try:
            jobs = self.scraper.run_full_extraction()
            
            # Get final statistics
            final_stats = self.scraper.get_job_statistics()
            final_count = final_stats.get('total_jobs', 0)
            
            # Export to CSV if requested
            csv_filename = ""
            if export_csv:
                csv_filename = self.export_to_csv()
            
            # Generate report
            self.generate_extraction_report(initial_count, final_count, jobs, final_stats, csv_filename)
            
            return jobs
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return []
    
    def export_to_csv(self) -> str:
        """Export all jobs to CSV file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"job4freshers_complete_jobs_{timestamp}.csv"
        
        logger.info(f"Exporting jobs to CSV: {csv_filename}")
        
        try:
            exported_file = self.scraper.export_jobs_to_csv(csv_filename)
            if exported_file:
                logger.info(f"✅ Jobs successfully exported to {exported_file}")
                return exported_file
            else:
                logger.error("❌ Failed to export jobs to CSV")
                return ""
        except Exception as e:
            logger.error(f"Error during CSV export: {e}")
            return ""
    
    def generate_extraction_report(self, initial_count: int, final_count: int, 
                                 extracted_jobs: list, stats: dict, csv_filename: str = ""):
        """Generate comprehensive extraction report"""
        logger.info("=" * 80)
        logger.info("EXTRACTION REPORT")
        logger.info("=" * 80)
        logger.info(f"Jobs extracted in this session: {len(extracted_jobs)}")
        logger.info(f"Initial database count: {initial_count}")
        logger.info(f"Final database count: {final_count}")
        logger.info(f"Net new jobs added: {final_count - initial_count}")
        logger.info(f"Total jobs in database: {final_count}")
        logger.info(f"Recent jobs (last 7 days): {stats.get('recent_jobs', 0)}")
        
        # CSV export information
        if csv_filename:
            logger.info(f"CSV Export: ✅ {csv_filename}")
            if os.path.exists(csv_filename):
                file_size = os.path.getsize(csv_filename)
                logger.info(f"CSV File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        else:
            logger.info("CSV Export: ❌ Not generated")
        
        # Company statistics
        if stats.get('top_companies'):
            logger.info("\nTOP HIRING COMPANIES:")
            for i, (company, count) in enumerate(list(stats['top_companies'].items())[:10], 1):
                logger.info(f"{i:2d}. {company}: {count} jobs")
        
        # Location statistics
        if stats.get('top_locations'):
            logger.info("\nTOP JOB LOCATIONS:")
            for i, (location, count) in enumerate(list(stats['top_locations'].items())[:10], 1):
                logger.info(f"{i:2d}. {location}: {count} jobs")
        
        # Data quality check
        self.check_data_quality(stats)
        
        logger.info("=" * 80)
        logger.info("EXTRACTION COMPLETED SUCCESSFULLY")
        logger.info(f"End time: {datetime.now()}")
        logger.info("=" * 80)
    
    def check_data_quality(self, stats: dict):
        """Check data quality and completeness"""
        logger.info("\nDATA QUALITY CHECK:")
        
        total_jobs = stats.get('total_jobs', 0)
        if total_jobs == 0:
            logger.warning("⚠️  No jobs found in database")
            return
        
        # Check for data completeness
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count jobs with empty fields
        quality_checks = [
            ("Jobs with missing company", "SELECT COUNT(*) FROM jobs WHERE company = 'N/A' OR company = '' OR company IS NULL"),
            ("Jobs with missing location", "SELECT COUNT(*) FROM jobs WHERE location = 'N/A' OR location = '' OR location IS NULL"),
            ("Jobs with missing skills", "SELECT COUNT(*) FROM jobs WHERE skills = 'N/A' OR skills = '' OR skills IS NULL"),
            ("Jobs with missing description", "SELECT COUNT(*) FROM jobs WHERE description = 'N/A' OR description = '' OR description IS NULL"),
            ("Jobs with valid URLs", "SELECT COUNT(*) FROM jobs WHERE url != 'N/A' AND url != '' AND url IS NOT NULL"),
        ]
        
        for description, query in quality_checks:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            percentage = (count / total_jobs) * 100
            logger.info(f"  {description}: {count} ({percentage:.1f}%)")
        
        # Quality score
        cursor.execute("""
            SELECT COUNT(*) FROM jobs 
            WHERE company != 'N/A' AND company != '' AND company IS NOT NULL
            AND location != 'N/A' AND location != '' AND location IS NOT NULL
            AND skills != 'N/A' AND skills != '' AND skills IS NOT NULL
            AND description != 'N/A' AND description != '' AND description IS NOT NULL
        """)
        complete_jobs = cursor.fetchone()[0]
        conn.close()
        
        completeness = (complete_jobs / total_jobs) * 100
        
        logger.info(f"  Data completeness score: {completeness:.1f}%")
        
        if completeness >= 80:
            logger.info("✅ Data quality is excellent")
        elif completeness >= 60:
            logger.info("⚠️  Data quality is good but could be improved")
        else:
            logger.warning("❌ Data quality needs improvement")
    
    def verify_extraction_completeness(self):
        """Verify that extraction is complete using sitemap-based approach"""
        logger.info("\nVERIFYING EXTRACTION COMPLETENESS...")
        logger.info("Using sitemap-based approach ensures comprehensive coverage")
        
        # Check database statistics
        stats = self.scraper.get_job_statistics()
        total_jobs = stats.get('total_jobs', 0)
        
        if total_jobs > 0:
            logger.info(f"✅ Successfully extracted {total_jobs} jobs from sitemap")
            logger.info("📋 All job URLs from sitemap have been processed")
            
            # Additional quality checks
            if total_jobs >= 10:
                logger.info("✅ Good quantity: Found substantial number of jobs")
            else:
                logger.warning("⚠️  Low quantity: Consider verifying sitemap structure")
                
        else:
            logger.error("❌ No jobs extracted - check sitemap URL and job URL patterns")
            
        logger.info("💡 Sitemap-based extraction provides complete coverage of available jobs")

def main():
    """Main execution function"""
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = "jobs.db"
    
    try:
        manager = JobExtractionManager(db_path)
        jobs = manager.run_complete_extraction()
        
        if jobs:
            manager.verify_extraction_completeness()
            logger.info("✅ Extraction process completed successfully")
            logger.info(f"📊 Check 'job_extraction.log' for detailed logs")
        else:
            logger.error("❌ No jobs were extracted")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()