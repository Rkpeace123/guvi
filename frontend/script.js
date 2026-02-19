// AURORA - Frontend JavaScript

class AuroraChat {
    constructor() {
        this.apiUrl = 'http://localhost:8000';
        this.apiKey = 'W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M';
        this.sessionId = this.generateSessionId();
        this.messageCount = 0;
        this.conversationHistory = [];
        
        this.initializeElements();
        this.attachEventListeners();
        this.checkSystemStatus();
    }
    
    initializeElements() {
        this.elements = {
            chatMessages: document.getElementById('chatMessages'),
            messageInput: document.getElementById('messageInput'),
            sendBtn: document.getElementById('sendBtn'),
            sessionId: document.getElementById('sessionId'),
            messageCount: document.getElementById('messageCount'),
            riskScore: document.getElementById('riskScore'),
            traaBar: document.getElementById('traaBar'),
            traaValue: document.getElementById('traaValue'),
            confidenceBar: document.getElementById('confidenceBar'),
            confidenceValue: document.getElementById('confidenceValue'),
            fsmState: document.getElementById('fsmState'),
            intelligenceCard: document.getElementById('intelligenceCard'),
            statusIndicator: document.getElementById('statusIndicator'),
            newSessionBtn: document.getElementById('newSessionBtn'),
            exportBtn: document.getElementById('exportBtn'),
            toastContainer: document.getElementById('toastContainer')
        };
        
        this.elements.sessionId.textContent = this.sessionId.substring(0, 12) + '...';
    }
    
    attachEventListeners() {
        // Send button
        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send
        this.elements.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Enable/disable send button
        this.elements.messageInput.addEventListener('input', () => {
            const hasText = this.elements.messageInput.value.trim().length > 0;
            this.elements.sendBtn.disabled = !hasText;
        });
        
        // Auto-resize textarea
        this.elements.messageInput.addEventListener('input', () => {
            this.elements.messageInput.style.height = 'auto';
            this.elements.messageInput.style.height = this.elements.messageInput.scrollHeight + 'px';
        });
        
        // Quick test buttons
        document.querySelectorAll('.quick-test-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const message = btn.getAttribute('data-message');
                this.elements.messageInput.value = message;
                this.elements.sendBtn.disabled = false;
                this.sendMessage();
            });
        });
        
        // New session button
        this.elements.newSessionBtn.addEventListener('click', () => this.newSession());
        
        // View final output button
        document.getElementById('viewFinalOutputBtn').addEventListener('click', () => this.checkAndShowFinalOutput());
        
        // Export button
        this.elements.exportBtn.addEventListener('click', () => this.exportData());
    }
    
    generateSessionId() {
        return `aurora-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                this.updateStatus('online', 'System Online');
            } else {
                this.updateStatus('offline', 'System Offline');
            }
        } catch (error) {
            this.updateStatus('offline', 'Connection Failed');
            this.showToast('Cannot connect to AURORA backend. Make sure the server is running.', 'error');
        }
    }
    
    updateStatus(status, text) {
        this.elements.statusIndicator.className = `status-indicator ${status}`;
        this.elements.statusIndicator.querySelector('.status-text').textContent = text;
    }
    
    async sendMessage() {
        const messageText = this.elements.messageInput.value.trim();
        if (!messageText) return;
        
        // Clear input
        this.elements.messageInput.value = '';
        this.elements.messageInput.style.height = 'auto';
        this.elements.sendBtn.disabled = true;
        
        // Remove welcome message if present
        const welcomeMsg = document.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        // Add user message to chat
        this.addMessage('scammer', messageText);
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            // Send to API
            const response = await fetch(`${this.apiUrl}/api/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': this.apiKey
                },
                body: JSON.stringify({
                    sessionId: this.sessionId,
                    message: {
                        sender: 'scammer',
                        text: messageText,
                        timestamp: new Date().toISOString()
                    },
                    conversationHistory: this.conversationHistory,
                    metadata: {
                        channel: 'Web',
                        language: 'English',
                        locale: 'IN'
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            // Add system response
            this.addMessage('system', data.reply, data.advanced_metrics);
            
            // Update metrics
            if (data.advanced_metrics) {
                this.updateMetrics(data.advanced_metrics);
            }
            
            // Update conversation history
            this.conversationHistory.push({
                sender: 'scammer',
                text: messageText,
                timestamp: new Date().toISOString()
            });
            this.conversationHistory.push({
                sender: 'user',
                text: data.reply,
                timestamp: new Date().toISOString()
            });
            
            this.messageCount++;
            this.elements.messageCount.textContent = this.messageCount;
            
            // Check if session should be finalized (after 10 scammer messages)
            if (this.messageCount >= 10) {
                setTimeout(() => this.checkAndShowFinalOutput(), 2000);
            }
            
        } catch (error) {
            this.removeTypingIndicator(typingId);
            this.showToast(`Error: ${error.message}`, 'error');
            console.error('Send message error:', error);
        }
    }
    
    addMessage(sender, text, metrics = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const avatar = sender === 'scammer' ? '🎭' : '🛡️';
        const senderName = sender === 'scammer' ? 'Scammer' : 'AURORA';
        
        let metricsHTML = '';
        if (metrics) {
            const traa = metrics.traa || {};
            const fsm = metrics.fsm || {};
            metricsHTML = `
                <div class="message-metrics">
                    <div class="metric-badge risk">
                        Risk: ${(traa.risk_score || 0).toFixed(2)}
                    </div>
                    <div class="metric-badge confidence">
                        Confidence: ${(traa.confidence || 0).toFixed(2)}
                    </div>
                    <div class="metric-badge">
                        State: ${fsm.state || 'unknown'}
                    </div>
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-bubble">${this.escapeHtml(text)}</div>
                <div class="message-meta">
                    <span>${senderName}</span>
                    <span>•</span>
                    <span>${new Date().toLocaleTimeString()}</span>
                </div>
                ${metricsHTML}
            </div>
        `;
        
        this.elements.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message system';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">🛡️</div>
            <div class="message-content">
                <div class="message-bubble">
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        this.elements.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        return 'typing-indicator';
    }
    
    removeTypingIndicator(id) {
        const indicator = document.getElementById(id);
        if (indicator) {
            indicator.remove();
        }
    }
    
    updateMetrics(metrics) {
        const traa = metrics.traa || {};
        const fsm = metrics.fsm || {};
        const entities = metrics.entities || {};
        const scamClass = metrics.scam_classification || {};
        
        // Update risk score
        const riskScore = traa.risk_score || 0;
        this.elements.riskScore.textContent = riskScore.toFixed(2);
        this.elements.riskScore.className = 'info-value risk-score';
        if (riskScore >= 0.65) {
            this.elements.riskScore.classList.add('high');
        } else if (riskScore >= 0.4) {
            this.elements.riskScore.classList.add('medium');
        }
        
        // Update TRAA bar
        const traaPercent = Math.min(riskScore * 100, 100);
        this.elements.traaBar.style.width = `${traaPercent}%`;
        this.elements.traaValue.textContent = riskScore.toFixed(2);
        
        // Update confidence bar
        const confidence = traa.confidence || 0;
        const confidencePercent = Math.min(confidence * 100, 100);
        this.elements.confidenceBar.style.width = `${confidencePercent}%`;
        this.elements.confidenceValue.textContent = confidence.toFixed(2);
        
        // Update FSM state
        this.elements.fsmState.textContent = fsm.state || '-';
        
        // Update scam classification
        if (scamClass.name) {
            const scamTypeName = document.getElementById('scamTypeName');
            const scamConfidenceBar = document.getElementById('scamConfidenceBar');
            const scamUrgency = document.getElementById('scamUrgency');
            
            if (scamTypeName) {
                scamTypeName.textContent = scamClass.name;
            }
            
            if (scamConfidenceBar) {
                const scamConfPercent = Math.min((scamClass.confidence || 0) * 100, 100);
                scamConfidenceBar.style.width = `${scamConfPercent}%`;
            }
            
            if (scamUrgency) {
                scamUrgency.textContent = `Urgency: ${scamClass.urgency || 'unknown'}`;
                scamUrgency.className = `scam-urgency ${scamClass.urgency || ''}`;
            }
        }
        
        // Update intelligence
        if (entities.total > 0) {
            this.updateIntelligence(metrics);
        }
    }
    
    async updateIntelligence(metrics) {
        try {
            const response = await fetch(`${this.apiUrl}/api/session/${this.sessionId}`, {
                headers: {
                    'X-API-Key': this.apiKey
                }
            });
            
            if (response.ok) {
                const sessionData = await response.json();
                const intelligence = sessionData.session?.intelligence || {};
                const finalOutput = sessionData.finalOutput;
                
                let html = '';
                let hasIntel = false;
                
                if (intelligence.phoneNumbers && intelligence.phoneNumbers.length > 0) {
                    hasIntel = true;
                    html += `<div class="intel-item">
                        <span class="intel-type">📞 Phone Numbers</span>
                        ${intelligence.phoneNumbers.map(p => `<div class="intel-value">${p}</div>`).join('')}
                    </div>`;
                }
                
                if (intelligence.upiIds && intelligence.upiIds.length > 0) {
                    hasIntel = true;
                    html += `<div class="intel-item">
                        <span class="intel-type">💳 UPI IDs</span>
                        ${intelligence.upiIds.map(u => `<div class="intel-value">${u}</div>`).join('')}
                    </div>`;
                }
                
                if (intelligence.bankAccounts && intelligence.bankAccounts.length > 0) {
                    hasIntel = true;
                    html += `<div class="intel-item">
                        <span class="intel-type">🏦 Bank Accounts</span>
                        ${intelligence.bankAccounts.map(b => `<div class="intel-value">${b}</div>`).join('')}
                    </div>`;
                }
                
                if (intelligence.phishingLinks && intelligence.phishingLinks.length > 0) {
                    hasIntel = true;
                    html += `<div class="intel-item">
                        <span class="intel-type">🔗 Phishing Links</span>
                        ${intelligence.phishingLinks.map(l => `<div class="intel-value">${l}</div>`).join('')}
                    </div>`;
                }
                
                if (intelligence.emailAddresses && intelligence.emailAddresses.length > 0) {
                    hasIntel = true;
                    html += `<div class="intel-item">
                        <span class="intel-type">📧 Email Addresses</span>
                        ${intelligence.emailAddresses.map(e => `<div class="intel-value">${e}</div>`).join('')}
                    </div>`;
                }
                
                if (hasIntel) {
                    this.elements.intelligenceCard.innerHTML = html;
                } else {
                    this.elements.intelligenceCard.innerHTML = '<p class="empty-state">No intelligence extracted yet</p>';
                }
                
                // Check if session is finalized and show final output
                if (sessionData.session?.finalized && finalOutput) {
                    this.showFinalOutput(finalOutput);
                }
            }
        } catch (error) {
            console.error('Failed to fetch intelligence:', error);
        }
    }
    
    async checkAndShowFinalOutput() {
        try {
            const response = await fetch(`${this.apiUrl}/api/session/${this.sessionId}`, {
                headers: {
                    'X-API-Key': this.apiKey
                }
            });
            
            if (response.ok) {
                const sessionData = await response.json();
                const finalOutput = sessionData.finalOutput;
                
                if (finalOutput) {
                    this.showFinalOutput(finalOutput);
                }
            }
        } catch (error) {
            console.error('Failed to check final output:', error);
        }
    }
    
    showFinalOutput(finalOutput) {
        // Check if final output already displayed
        if (document.getElementById('finalOutputSection')) {
            return;
        }
        
        // Create final output display
        const finalOutputDiv = document.createElement('div');
        finalOutputDiv.id = 'finalOutputSection';
        finalOutputDiv.className = 'final-output-section';
        
        const intel = finalOutput.extractedIntelligence || {};
        const metrics = finalOutput.engagementMetrics || {};
        
        finalOutputDiv.innerHTML = `
            <div class="final-output-header">
                <div class="final-output-icon">🏁</div>
                <div>
                    <h3>Session Finalized - Final Output</h3>
                    <p>This data has been sent to GUVI for evaluation</p>
                </div>
            </div>
            
            <div class="final-output-content">
                <div class="final-output-row">
                    <div class="final-output-label">Session ID:</div>
                    <div class="final-output-value">${finalOutput.sessionId}</div>
                </div>
                
                <div class="final-output-row">
                    <div class="final-output-label">Scam Detected:</div>
                    <div class="final-output-value">
                        <span class="badge ${finalOutput.scamDetected ? 'badge-danger' : 'badge-success'}">
                            ${finalOutput.scamDetected ? '✓ YES' : '✗ NO'}
                        </span>
                    </div>
                </div>
                
                <div class="final-output-row">
                    <div class="final-output-label">Total Messages:</div>
                    <div class="final-output-value">${finalOutput.totalMessagesExchanged}</div>
                </div>
                
                <div class="final-output-section-title">📊 Engagement Metrics</div>
                <div class="final-output-row">
                    <div class="final-output-label">Duration:</div>
                    <div class="final-output-value">${metrics.engagementDurationSeconds || 0} seconds</div>
                </div>
                
                <div class="final-output-section-title">🔍 Extracted Intelligence</div>
                ${intel.phoneNumbers && intel.phoneNumbers.length > 0 ? `
                    <div class="final-output-row">
                        <div class="final-output-label">📞 Phone Numbers:</div>
                        <div class="final-output-value">${intel.phoneNumbers.join(', ')}</div>
                    </div>
                ` : ''}
                ${intel.upiIds && intel.upiIds.length > 0 ? `
                    <div class="final-output-row">
                        <div class="final-output-label">💳 UPI IDs:</div>
                        <div class="final-output-value">${intel.upiIds.join(', ')}</div>
                    </div>
                ` : ''}
                ${intel.bankAccounts && intel.bankAccounts.length > 0 ? `
                    <div class="final-output-row">
                        <div class="final-output-label">🏦 Bank Accounts:</div>
                        <div class="final-output-value">${intel.bankAccounts.join(', ')}</div>
                    </div>
                ` : ''}
                ${intel.phishingLinks && intel.phishingLinks.length > 0 ? `
                    <div class="final-output-row">
                        <div class="final-output-label">🔗 Phishing Links:</div>
                        <div class="final-output-value">${intel.phishingLinks.join(', ')}</div>
                    </div>
                ` : ''}
                ${intel.emailAddresses && intel.emailAddresses.length > 0 ? `
                    <div class="final-output-row">
                        <div class="final-output-label">📧 Email Addresses:</div>
                        <div class="final-output-value">${intel.emailAddresses.join(', ')}</div>
                    </div>
                ` : ''}
                
                <div class="final-output-section-title">📝 Agent Notes</div>
                <div class="final-output-notes">${finalOutput.agentNotes}</div>
                
                <div class="final-output-json">
                    <div class="final-output-json-header">
                        <span>Raw JSON Output</span>
                        <button class="copy-json-btn" onclick="window.auroraChat.copyFinalOutput()">
                            📋 Copy
                        </button>
                    </div>
                    <pre><code>${JSON.stringify(finalOutput, null, 2)}</code></pre>
                </div>
            </div>
        `;
        
        this.elements.chatMessages.appendChild(finalOutputDiv);
        this.scrollToBottom();
        this.showToast('Session finalized! Final output sent to GUVI', 'success');
        
        // Store final output for copying
        this.finalOutputData = finalOutput;
    }
    
    copyFinalOutput() {
        if (this.finalOutputData) {
            navigator.clipboard.writeText(JSON.stringify(this.finalOutputData, null, 2));
            this.showToast('Final output copied to clipboard', 'success');
        }
    }
    
    newSession() {
        if (confirm('Start a new session? Current conversation will be cleared.')) {
            this.sessionId = this.generateSessionId();
            this.messageCount = 0;
            this.conversationHistory = [];
            
            this.elements.sessionId.textContent = this.sessionId.substring(0, 12) + '...';
            this.elements.messageCount.textContent = '0';
            this.elements.riskScore.textContent = '0.00';
            this.elements.riskScore.className = 'info-value risk-score';
            this.elements.traaBar.style.width = '0%';
            this.elements.traaValue.textContent = '0.00';
            this.elements.confidenceBar.style.width = '0%';
            this.elements.confidenceValue.textContent = '0.00';
            this.elements.fsmState.textContent = '-';
            this.elements.intelligenceCard.innerHTML = '<p class="empty-state">No intelligence extracted yet</p>';
            
            this.elements.chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="welcome-icon">🛡️</div>
                    <h3>Welcome to AURORA Testing Interface</h3>
                    <p>Start a conversation to test the advanced honeypot system</p>
                    <div class="quick-tests">
                        <button class="quick-test-btn" data-message="Your account has been blocked! Verify immediately by calling 9876543210">
                            🚨 Urgent Scam
                        </button>
                        <button class="quick-test-btn" data-message="Congratulations! You won 1 crore rupees. Pay processing fee to winner@upi">
                            🎉 Prize Scam
                        </button>
                        <button class="quick-test-btn" data-message="Hello, how are you today?">
                            👋 Normal Message
                        </button>
                    </div>
                </div>
            `;
            
            // Re-attach quick test listeners
            document.querySelectorAll('.quick-test-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const message = btn.getAttribute('data-message');
                    this.elements.messageInput.value = message;
                    this.elements.sendBtn.disabled = false;
                    this.sendMessage();
                });
            });
            
            this.showToast('New session started', 'success');
        }
    }
    
    async exportData() {
        try {
            const response = await fetch(`${this.apiUrl}/api/session/${this.sessionId}`, {
                headers: {
                    'X-API-Key': this.apiKey
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `aurora-session-${this.sessionId}.json`;
                a.click();
                URL.revokeObjectURL(url);
                this.showToast('Session data exported', 'success');
            } else {
                throw new Error('Failed to fetch session data');
            }
        } catch (error) {
            this.showToast(`Export failed: ${error.message}`, 'error');
        }
    }
    
    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.elements.toastContainer.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideInRight 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    scrollToBottom() {
        this.elements.chatMessages.scrollTop = this.elements.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.auroraChat = new AuroraChat();
});
