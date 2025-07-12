// Job4Freshers AI Chatbot JavaScript

class ChatBot {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.initializeEventListeners();
        this.loadStatistics();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    initializeEventListeners() {
        // Message input enter key
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Auto-focus on message input
        document.getElementById('messageInput').focus();
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Clear input
        input.value = '';

        // Add user message to chat
        this.addMessageToChat(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.status === 'success') {
                // Add bot response
                this.addMessageToChat(data.response, 'bot');

                // Display jobs if any
                if (data.jobs && data.jobs.length > 0) {
                    this.displayJobs(data.jobs);
                }

                // Update suggestions
                if (data.suggestions) {
                    this.updateSuggestions(data.suggestions);
                }
            } else {
                this.addMessageToChat('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.removeTypingIndicator();
            this.addMessageToChat('Sorry, I\'m having trouble connecting. Please try again.', 'bot');
        }
    }

    addMessageToChat(message, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        avatarDiv.innerHTML = sender === 'user' ? 
            '<i class="fas fa-user"></i>' : 
            '<i class="fas fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.innerHTML = this.formatMessage(message);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());

        contentDiv.appendChild(messageText);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    formatMessage(message) {
        // Convert markdown-style formatting to HTML
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;

        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    displayJobs(jobs) {
        const chatMessages = document.getElementById('chatMessages');
        const jobsContainer = document.createElement('div');
        jobsContainer.className = 'jobs-container';

        jobs.forEach(job => {
            const jobCard = document.createElement('div');
            jobCard.className = 'job-card';
            jobCard.onclick = () => this.showJobDetails(job);

            jobCard.innerHTML = `
                <div class="job-title">${job.title}</div>
                <div class="job-company">${job.company}</div>
                <div class="job-details">
                    <span><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
                    <span><i class="fas fa-briefcase"></i> ${job.experience}</span>
                    <span><i class="fas fa-calendar"></i> ${job.posted_date}</span>
                </div>
                <div class="job-skills">${job.skills}</div>
                <div class="job-match-score">Match: ${(job.match_score * 100).toFixed(1)}%</div>
            `;

            jobsContainer.appendChild(jobCard);
        });

        // Add jobs container to last bot message
        const lastBotMessage = document.querySelector('.bot-message:last-child .message-content');
        if (lastBotMessage) {
            lastBotMessage.appendChild(jobsContainer);
        }
    }

    showJobDetails(job) {
        const modal = document.getElementById('jobModal');
        const modalBody = document.getElementById('jobModalBody');

        modalBody.innerHTML = `
            <div class="job-detail-header">
                <h2>${job.title}</h2>
                <div class="job-company-large">${job.company}</div>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-map-marker-alt"></i> Location</h4>
                <p>${job.location}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-briefcase"></i> Experience Required</h4>
                <p>${job.experience}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-tools"></i> Skills Required</h4>
                <p>${job.skills}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-money-bill-wave"></i> Salary</h4>
                <p>${job.salary}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-info-circle"></i> Description</h4>
                <p>${job.description}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-calendar"></i> Posted Date</h4>
                <p>${job.posted_date}</p>
            </div>
            <div class="job-detail-section">
                <h4><i class="fas fa-chart-line"></i> Match Score</h4>
                <p>${(job.match_score * 100).toFixed(1)}% match with your requirements</p>
            </div>
            <div class="job-detail-actions">
                <a href="${job.url}" target="_blank" class="btn-primary">
                    <i class="fas fa-external-link-alt"></i> View Original Job
                </a>
            </div>
        `;

        modal.style.display = 'block';
    }

    updateSuggestions(suggestions) {
        const container = document.getElementById('suggestionsContainer');
        const suggestionsDiv = container.querySelector('.suggestions');
        
        suggestionsDiv.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.className = 'suggestion-btn';
            btn.textContent = suggestion;
            btn.onclick = () => this.sendSuggestion(suggestion);
            suggestionsDiv.appendChild(btn);
        });
    }

    sendSuggestion(suggestion) {
        document.getElementById('messageInput').value = suggestion;
        this.sendMessage();
    }

    async loadStatistics() {
        try {
            const response = await fetch('/api/jobs/statistics');
            const data = await response.json();
            
            if (data.status === 'success' && data.statistics) {
                this.updateStatistics(data.statistics);
            }
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    updateStatistics(stats) {
        // Update total jobs
        document.getElementById('totalJobs').textContent = stats.total_jobs || 0;
        document.getElementById('recentJobs').textContent = stats.recent_jobs || 0;

        // Update top companies
        const companiesList = document.getElementById('companiesList');
        companiesList.innerHTML = '';
        
        if (stats.top_companies) {
            Object.entries(stats.top_companies).slice(0, 5).forEach(([company, count]) => {
                const item = document.createElement('div');
                item.className = 'company-item';
                item.innerHTML = `
                    <span class="company-name">${company}</span>
                    <span class="company-count">${count}</span>
                `;
                companiesList.appendChild(item);
            });
        }

        // Update top locations
        const locationsList = document.getElementById('locationsList');
        locationsList.innerHTML = '';
        
        if (stats.top_locations) {
            Object.entries(stats.top_locations).slice(0, 5).forEach(([location, count]) => {
                const item = document.createElement('div');
                item.className = 'location-item';
                item.innerHTML = `
                    <span class="location-name">${location}</span>
                    <span class="location-count">${count}</span>
                `;
                locationsList.appendChild(item);
            });
        }
    }

    clearChat() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <p>Chat cleared! How can I help you find your next job opportunity?</p>
                    <div class="message-time">${this.formatTime(new Date())}</div>
                </div>
            </div>
        `;

        // Reset suggestions
        this.updateSuggestions([
            'Find Python developer jobs',
            'Show me remote opportunities',
            'Jobs for freshers',
            'Data science positions'
        ]);
    }
}

// Global functions for HTML onclick events
function sendMessage() {
    chatBot.sendMessage();
}

function sendSuggestion(suggestion) {
    chatBot.sendSuggestion(suggestion);
}

function clearChat() {
    chatBot.clearChat();
}

function closeJobModal() {
    document.getElementById('jobModal').style.display = 'none';
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('jobModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Initialize chatbot when page loads
let chatBot;
document.addEventListener('DOMContentLoaded', function() {
    chatBot = new ChatBot();
});

// Add typing indicator styles
const typingStyle = document.createElement('style');
typingStyle.textContent = `
    .typing-dots {
        display: flex;
        gap: 4px;
        align-items: center;
        padding: 8px 0;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        background: #6b7280;
        border-radius: 50%;
        animation: typingAnimation 1.4s infinite;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typingAnimation {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }
    
    .job-detail-header {
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 1rem;
    }
    
    .job-detail-header h2 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .job-company-large {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .job-detail-section {
        margin-bottom: 1.5rem;
    }
    
    .job-detail-section h4 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .job-detail-actions {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-color);
    }
    
    .btn-primary {
        background: var(--primary-color);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .btn-primary:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
    }
    
    .jobs-container {
        margin-top: 1rem;
        display: grid;
        gap: 1rem;
    }
`;

document.head.appendChild(typingStyle);