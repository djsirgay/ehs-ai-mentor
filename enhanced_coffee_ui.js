// Enhanced Coffee UI JavaScript
class CoffeeUI {
    constructor() {
        this.userId = 'u001'; // Default user
        this.chatHistory = [];
        // init() will be called from DOMContentLoaded
    }

    async init() {
        await this.loadChatHistory();
        if (this.chatHistory.length === 0) {
            this.sendInitialMessage();
        }
    }

    async loadChatHistory() {
        try {
            // Load from server first
            const response = await fetch(`/coffee/chat/history/${this.userId}`);
            const data = await response.json();
            
            if (data.success && data.history && data.history.length > 0) {
                this.chatHistory = [];
                data.history.forEach(item => {
                    this.chatHistory.push({ 
                        content: item.user_message, 
                        type: 'user', 
                        timestamp: item.timestamp 
                    });
                    this.chatHistory.push({ 
                        content: item.ai_response, 
                        type: 'bot', 
                        timestamp: item.timestamp 
                    });
                });
                this.renderChatHistory();
                return;
            }
        } catch (error) {
            console.log('Server history not available, checking localStorage');
        }
        
        // Fallback to localStorage if server fails
        const saved = localStorage.getItem(`coffeeChat_${this.userId}`);
        if (saved) {
            this.chatHistory = JSON.parse(saved);
            this.renderChatHistory();
        }
    }

    saveChatHistory() {
        localStorage.setItem(`coffeeChat_${this.userId}`, JSON.stringify(this.chatHistory));
    }

    renderChatHistory() {
        const container = document.getElementById('chatMessages');
        if (!container) return;
        
        container.innerHTML = '';
        
        this.chatHistory.forEach(msg => {
            const div = document.createElement('div');
            div.className = `message ${msg.type}`;
            div.innerHTML = msg.content;
            container.appendChild(div);
        });
        
        container.scrollTop = container.scrollHeight;
    }

    addMessage(content, type) {
        this.chatHistory.push({ 
            content, 
            type, 
            timestamp: Date.now() 
        });
        this.renderChatHistory();
        this.saveChatHistory();
    }

    async sendMessage(message) {
        if (!message) return;

        // Add user message
        this.addMessage(message, 'user');

        // Add loading message
        this.addMessage('🤖 Thinking...', 'bot');

        try {
            const formData = new FormData();
            formData.append('user_id', this.userId);
            formData.append('message', message);

            const response = await fetch('/coffee/chat', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            // Remove loading message
            this.chatHistory.pop();
            
            // Add bot response
            this.addMessage(data.response, 'bot');
            
        } catch (error) {
            // Remove loading message
            this.chatHistory.pop();
            this.addMessage('❌ Error: ' + error.message, 'bot');
        }
    }

    async sendInitialMessage() {
        this.addMessage('🤖 Connecting...', 'bot');
        
        try {
            const formData = new FormData();
            formData.append('user_id', this.userId);
            formData.append('message', 'hello');

            const response = await fetch('/coffee/chat', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            // Remove loading message
            this.chatHistory.pop();
            
            // Add bot response
            this.addMessage(data.response, 'bot');
            
        } catch (error) {
            // Remove loading message
            this.chatHistory.pop();
            this.addMessage('❌ Connection error. Please refresh the page.', 'bot');
        }
    }

    async createProfile(profileData) {
        try {
            const formData = new FormData();
            formData.append('user_id', this.userId);
            formData.append('interests', profileData.interests);
            formData.append('personality_traits', profileData.personality || '');
            formData.append('availability', JSON.stringify(profileData.availability || []));
            formData.append('meeting_preferences', JSON.stringify(profileData.meetingPreferences || {}));

            const response = await fetch('/enhanced-coffee/profile', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.success) {
                // Add success message to chat
                this.addMessage('✅ Smart Profile created! Now say "OK" or "Ready" to start finding friends!', 'bot');
                return true;
            } else {
                throw new Error('Profile creation failed');
            }
            
        } catch (error) {
            this.addMessage('❌ Error creating profile: ' + error.message, 'bot');
            return false;
        }
    }

    switchTab(tabName) {
        // Save chat history when switching away from chat
        if (document.querySelector('.tab-content.active').id === 'chat') {
            this.saveChatHistory();
        }

        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });

        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');

        // Load chat history when switching to chat
        if (tabName === 'chat') {
            setTimeout(() => this.loadChatHistory(), 100); // Small delay to ensure tab is active
        }
    }
}

// Global instance
let coffeeUI;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    coffeeUI = new CoffeeUI();
    await coffeeUI.init();
});

// Global functions for HTML compatibility
function switchTab(tabName) {
    if (coffeeUI) {
        coffeeUI.switchTab(tabName);
    }
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (message && coffeeUI) {
        coffeeUI.sendMessage(message);
        input.value = '';
    }
}

function createProfile() {
    const interests = document.getElementById('interests').value;
    const personality = document.getElementById('personality').value;
    const meetingStyle = document.getElementById('meetingStyle').value;
    const availability = document.getElementById('availability').value;

    if (!interests.trim()) {
        alert('Please enter your interests!');
        return;
    }

    const profileData = {
        interests: interests,
        personality: personality,
        availability: [{day: availability, time: 'flexible'}],
        meetingPreferences: {style: meetingStyle}
    };

    if (coffeeUI) {
        coffeeUI.createProfile(profileData).then(success => {
            if (success) {
                alert('✅ Profile created successfully! Switch to Chat tab and say "Ок" to start matching!');
                switchTab('chat');
            } else {
                alert('❌ Error creating profile. Please try again.');
            }
        });
    }
}