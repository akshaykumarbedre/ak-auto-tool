#!/usr/bin/env python3
"""
Job4Freshers AI Chatbot - Conversational Interface

This module implements the chatbot conversation logic and natural language processing
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatbotConversationManager:
    """Manages chatbot conversations and responses"""
    
    def __init__(self, job_matcher):
        self.job_matcher = job_matcher
        self.conversation_history = []
        self.user_profile = {}
        self.current_context = None
        self.greeting_responses = [
            "Hello! I'm your Job4Freshers AI assistant. I can help you find the perfect job that matches your skills and preferences.",
            "Hi there! I'm here to help you discover amazing job opportunities. What kind of role are you looking for?",
            "Welcome to Job4Freshers! I'm your personal job search assistant. Tell me about your dream job and I'll help you find it.",
            "Hello! Ready to find your next career opportunity? I can help you search through thousands of jobs to find the perfect match."
        ]
        
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
                r'\b(start|begin)\b'
            ],
            'job_search': [
                r'\b(find|search|looking for|want|need)\b.*\b(job|position|role|career|work|employment)\b',
                r'\b(job|position|role)\b.*\b(in|for|with)\b',
                r'\b(hiring|openings|opportunities|vacancies)\b'
            ],
            'skill_based': [
                r'\b(python|java|javascript|react|angular|php|sql|aws|docker|kubernetes)\b',
                r'\b(developer|engineer|programmer|analyst|designer|manager)\b',
                r'\b(experience|skills|expertise|knowledge)\b.*\b(in|with)\b'
            ],
            'location_based': [
                r'\b(in|at|from)\b.*\b(bangalore|mumbai|delhi|hyderabad|pune|chennai|remote)\b',
                r'\b(location|city|place|area)\b',
                r'\b(work from home|remote|onsite)\b'
            ],
            'experience_based': [
                r'\b(fresher|entry level|junior|senior|experienced)\b',
                r'\b(\d+)\s*(years?|yrs?)\b.*\b(experience|exp)\b',
                r'\b(experience|exp)\b.*\b(\d+)\s*(years?|yrs?)\b'
            ],
            'salary_based': [
                r'\b(salary|pay|compensation|package|ctc)\b',
                r'\b(\d+)\s*(lpa|lakhs?|k|thousand)\b',
                r'\b(budget|range|expectation)\b'
            ],
            'company_based': [
                r'\b(company|organization|firm|startup|mnc)\b',
                r'\b(google|microsoft|amazon|infosys|tcs|wipro|accenture)\b'
            ],
            'help': [
                r'\b(help|assist|support|guide|how)\b',
                r'\b(what can you do|capabilities|features)\b'
            ],
            'statistics': [
                r'\b(stats|statistics|data|numbers|trends)\b',
                r'\b(how many|total|count)\b.*\b(jobs|positions|openings)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|thanks|thank you|exit|quit)\b',
                r'\b(that\'s all|done|finished)\b'
            ]
        }
    
    def detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'general'
    
    def extract_entities(self, message: str) -> Dict:
        """Extract entities from user message"""
        entities = {
            'skills': [],
            'location': [],
            'experience': None,
            'salary': None,
            'job_type': None,
            'company': None
        }
        
        message_lower = message.lower()
        
        # Extract skills
        skills_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'node.js', 'php',
            'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'html', 'css', 'bootstrap', 'django', 'flask',
            'spring', 'hibernate', 'rest', 'api', 'microservices', 'devops',
            'machine learning', 'ai', 'data science', 'analytics', 'tableau',
            'power bi', 'excel', 'salesforce', 'sap', 'oracle', 'testing',
            'selenium', 'junit', 'android', 'ios', 'swift', 'kotlin', 'flutter'
        ]
        
        for skill in skills_keywords:
            if skill in message_lower:
                entities['skills'].append(skill)
        
        # Extract locations
        locations = [
            'bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai',
            'kolkata', 'ahmedabad', 'gurgaon', 'noida', 'remote', 'work from home'
        ]
        
        for location in locations:
            if location in message_lower:
                entities['location'].append(location)
        
        # Extract experience
        exp_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)',
            r'fresher', r'entry level', r'junior', r'senior'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, message_lower)
            if match:
                entities['experience'] = match.group()
                break
        
        # Extract salary
        salary_patterns = [
            r'(\d+)\s*(?:lpa|lakhs?|k|thousand)',
            r'salary\s*(?:of\s*)?(\d+)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)\s*(?:lpa|lakhs?)'
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, message_lower)
            if match:
                entities['salary'] = match.group()
                break
        
        return entities
    
    def update_user_profile(self, entities: Dict):
        """Update user profile with extracted entities"""
        for key, value in entities.items():
            if value:
                if key in ['skills', 'location'] and isinstance(value, list):
                    if key not in self.user_profile:
                        self.user_profile[key] = []
                    self.user_profile[key].extend(value)
                    # Remove duplicates
                    self.user_profile[key] = list(set(self.user_profile[key]))
                else:
                    self.user_profile[key] = value
    
    def generate_response(self, message: str) -> Dict:
        """Generate response based on user message"""
        intent = self.detect_intent(message)
        entities = self.extract_entities(message)
        self.update_user_profile(entities)
        
        response = {
            'message': '',
            'jobs': [],
            'suggestions': [],
            'intent': intent,
            'entities': entities,
            'timestamp': datetime.now().isoformat()
        }
        
        if intent == 'greeting':
            response['message'] = random.choice(self.greeting_responses)
            response['suggestions'] = [
                "Find Python developer jobs",
                "Show me remote opportunities",
                "Jobs for freshers",
                "Data science positions",
                "What can you help me with?"
            ]
        
        elif intent == 'job_search':
            jobs = self.job_matcher.find_matching_jobs(message, top_k=5)
            response['jobs'] = jobs
            
            if jobs:
                response['message'] = f"I found {len(jobs)} jobs that match your criteria. Here are the top matches:"
                response['suggestions'] = [
                    "Show me more similar jobs",
                    "Filter by location",
                    "Jobs at specific companies",
                    "Get job statistics"
                ]
            else:
                response['message'] = "I couldn't find any jobs matching your exact criteria. Let me suggest some similar opportunities or you can try modifying your search."
                response['suggestions'] = [
                    "Show me all available jobs",
                    "Broaden my search criteria",
                    "Get job market statistics",
                    "Help me refine my search"
                ]
        
        elif intent == 'skill_based':
            skills_query = ' '.join(entities['skills']) if entities['skills'] else message
            jobs = self.job_matcher.find_matching_jobs(skills_query, top_k=5)
            response['jobs'] = jobs
            
            if jobs:
                response['message'] = f"Found {len(jobs)} jobs matching your skills. Here are the best matches:"
            else:
                response['message'] = "No exact matches found for your skills. Let me show you related opportunities."
                # Try broader search
                jobs = self.job_matcher.find_matching_jobs(message, top_k=3)
                response['jobs'] = jobs
            
            response['suggestions'] = [
                "Show more jobs with these skills",
                "Filter by experience level",
                "Find jobs in specific locations",
                "Get salary information"
            ]
        
        elif intent == 'location_based':
            location_query = ' '.join(entities['location']) if entities['location'] else message
            jobs = self.job_matcher.find_matching_jobs(location_query, top_k=5)
            response['jobs'] = jobs
            
            response['message'] = f"Found {len(jobs)} jobs in your preferred location(s)."
            response['suggestions'] = [
                "Show more jobs in this area",
                "Filter by skill requirements",
                "Compare salaries by location",
                "Remote work opportunities"
            ]
        
        elif intent == 'experience_based':
            exp_query = entities['experience'] if entities['experience'] else message
            jobs = self.job_matcher.find_matching_jobs(exp_query, top_k=5)
            response['jobs'] = jobs
            
            response['message'] = f"Here are jobs suitable for your experience level:"
            response['suggestions'] = [
                "Show entry-level positions",
                "Senior level opportunities",
                "Skills required for advancement",
                "Career growth paths"
            ]
        
        elif intent == 'statistics':
            stats = self.job_matcher.get_job_statistics()
            if stats:
                response['message'] = self.format_statistics(stats)
            else:
                response['message'] = "I don't have enough job data to provide statistics yet. Please try searching for specific jobs first."
            
            response['suggestions'] = [
                "Show trending skills",
                "Top hiring companies",
                "Salary trends",
                "Popular job locations"
            ]
        
        elif intent == 'help':
            response['message'] = self.get_help_message()
            response['suggestions'] = [
                "Find Python jobs",
                "Show remote opportunities",
                "Jobs for freshers",
                "Get job market stats",
                "Search by company name"
            ]
        
        elif intent == 'goodbye':
            response['message'] = "Thank you for using Job4Freshers! Good luck with your job search. Feel free to come back anytime for more opportunities."
        
        else:  # general intent
            # Try to find jobs based on the general query
            jobs = self.job_matcher.find_matching_jobs(message, top_k=3)
            response['jobs'] = jobs
            
            if jobs:
                response['message'] = "I found some job opportunities that might interest you:"
            else:
                response['message'] = "I'd be happy to help you find jobs! Please tell me more about what you're looking for - skills, location, experience level, or company preferences."
            
            response['suggestions'] = [
                "Find jobs by skills",
                "Search by location",
                "Filter by experience",
                "Show all available jobs",
                "Get help with search"
            ]
        
        # Add conversation to history
        self.conversation_history.append({
            'user_message': message,
            'bot_response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def format_statistics(self, stats: Dict) -> str:
        """Format job statistics for display"""
        message = f"📊 **Job Market Statistics**\n\n"
        message += f"🔹 **Total Jobs Available**: {stats.get('total_jobs', 0)}\n"
        message += f"🔹 **Recently Posted**: {stats.get('recent_jobs', 0)}\n\n"
        
        if stats.get('top_companies'):
            message += "🏢 **Top Hiring Companies**:\n"
            for company, count in list(stats['top_companies'].items())[:5]:
                message += f"   • {company}: {count} jobs\n"
            message += "\n"
        
        if stats.get('top_locations'):
            message += "📍 **Popular Job Locations**:\n"
            for location, count in list(stats['top_locations'].items())[:5]:
                message += f"   • {location}: {count} jobs\n"
            message += "\n"
        
        if stats.get('top_skills'):
            message += "🚀 **In-Demand Skills**:\n"
            for skill, count in list(stats['top_skills'].items())[:5]:
                message += f"   • {skill}: {count} jobs\n"
        
        return message
    
    def get_help_message(self) -> str:
        """Generate help message"""
        help_msg = """
🤖 **Job4Freshers AI Assistant - Help**

I can help you find the perfect job! Here's what I can do:

🔍 **Job Search**:
   • "Find Python developer jobs"
   • "Show me remote opportunities"
   • "Jobs for freshers in Bangalore"

🎯 **Skill-Based Search**:
   • "I know Java and SQL"
   • "React developer positions"
   • "Data science jobs"

📍 **Location-Based Search**:
   • "Jobs in Mumbai"
   • "Remote work opportunities"
   • "Positions in Hyderabad"

💼 **Experience-Based Search**:
   • "Entry level positions"
   • "2 years experience jobs"
   • "Senior developer roles"

📊 **Get Statistics**:
   • "Show job market trends"
   • "Top hiring companies"
   • "In-demand skills"

Just tell me what you're looking for and I'll help you find the best opportunities!
        """
        return help_msg
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset conversation history and user profile"""
        self.conversation_history = []
        self.user_profile = {}
        self.current_context = None

if __name__ == "__main__":
    # Test the chatbot
    from job_matcher import JobMatchingEngine
    
    job_matcher = JobMatchingEngine()
    chatbot = ChatbotConversationManager(job_matcher)
    
    # Test conversations
    test_messages = [
        "Hello",
        "I'm looking for Python developer jobs",
        "Show me remote opportunities",
        "What are the job statistics?",
        "Help me find jobs"
    ]
    
    for message in test_messages:
        print(f"User: {message}")
        response = chatbot.generate_response(message)
        print(f"Bot: {response['message']}")
        print(f"Found {len(response['jobs'])} jobs")
        print("-" * 50)