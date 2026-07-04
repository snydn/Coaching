import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import requests
import json
from datetime import datetime

# YOUR GOOGLE SCRIPT URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzw53dmy6mYj_SFtVF2HyRas5XQUEywm7CBe7VetAHlGfKsiqa3QtUMuzoMJ4UjaC_nzQ/exec"

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        try:
            return SimpleHTTPRequestHandler.do_GET(self)
        except:
            self.send_error(404, 'File not found')
    
    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                response = requests.post(GOOGLE_SCRIPT_URL, json=data, timeout=30)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                if response.status_code == 200:
                    result = {"success": True, "message": "Client saved successfully!"}
                else:
                    result = {"success": False, "message": f"Error: {response.status_code}"}
                
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": str(e)}).encode())
    
    def log_message(self, format, *args):
        pass

def create_index_html():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS2 Coaching App</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f0f1a;
            color: #e8eaed;
            padding: 24px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }
        
        .container {
            max-width: 820px;
            width: 100%;
            margin: 0 auto;
            background: #1a1a2e;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid #2a2a4a;
        }
        
        .header {
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid #2a2a4a;
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #ff4b4b, #ff6b6b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        .header p {
            color: #8892b0;
            font-size: 14px;
            margin-top: 4px;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 600;
            color: #ccd6f6;
            margin-top: 24px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .section-title .icon {
            font-size: 18px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        
        @media (max-width: 600px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            .container {
                padding: 20px;
            }
        }
        
        label {
            display: block;
            font-size: 13px;
            font-weight: 500;
            color: #8892b0;
            margin-bottom: 5px;
        }
        
        label .required {
            color: #ff4b4b;
        }
        
        input, textarea {
            width: 100%;
            padding: 11px 14px;
            border: 1px solid #2a2a4a;
            border-radius: 10px;
            background: #14142a;
            color: #e8eaed;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
            outline: none;
        }
        
        input:focus, textarea:focus {
            border-color: #ff4b4b;
            box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.15);
            background: #1a1a3a;
        }
        
        input::placeholder, textarea::placeholder {
            color: #4a4a6a;
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        /* Tag Input Styles */
        .tag-input-container {
            background: #14142a;
            border: 1px solid #2a2a4a;
            border-radius: 10px;
            padding: 8px;
            transition: all 0.2s ease;
            min-height: 50px;
        }
        
        .tag-input-container:focus-within {
            border-color: #ff4b4b;
            box-shadow: 0 0 0 3px rgba(255, 75, 75, 0.15);
        }
        
        .tag-input-container .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 4px;
        }
        
        .tag-input-container .tag {
            background: #2a2a5a;
            color: #e8eaed;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            animation: tagIn 0.2s ease;
        }
        
        .tag-input-container .tag .remove-tag {
            cursor: pointer;
            color: #8892b0;
            font-size: 14px;
            line-height: 1;
            transition: color 0.2s;
        }
        
        .tag-input-container .tag .remove-tag:hover {
            color: #ff4b4b;
        }
        
        .tag-input-container .tag-input-wrapper {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .tag-input-container .tag-input-wrapper input {
            flex: 1;
            min-width: 120px;
            background: transparent;
            border: none;
            padding: 4px 8px;
            color: #e8eaed;
            font-size: 14px;
            outline: none;
        }
        
        .tag-input-container .tag-input-wrapper input::placeholder {
            color: #4a4a6a;
        }
        
        .tag-input-container .tag-input-wrapper .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        
        .tag-input-container .tag-input-wrapper .suggestions .suggestion {
            background: #1a1a3a;
            color: #8892b0;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid transparent;
        }
        
        .tag-input-container .tag-input-wrapper .suggestions .suggestion:hover {
            background: #2a2a5a;
            color: #e8eaed;
            border-color: #ff4b4b;
        }
        
        @keyframes tagIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        .quick-add-btns {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 6px;
        }
        
        .quick-add-btns .quick-btn {
            background: #1a1a3a;
            color: #8892b0;
            padding: 3px 12px;
            border-radius: 12px;
            font-size: 11px;
            cursor: pointer;
            border: 1px solid #2a2a4a;
            transition: all 0.2s;
        }
        
        .quick-add-btns .quick-btn:hover {
            background: #2a2a5a;
            color: #e8eaed;
            border-color: #ff4b4b;
        }
        
        .helper-text {
            font-size: 12px;
            color: #4a4a6a;
            margin-top: 4px;
        }
        
        .submit-btn {
            width: 100%;
            padding: 14px;
            margin-top: 24px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #ff4b4b, #e63946);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .submit-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 75, 75, 0.3);
        }
        
        .submit-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        #message {
            margin-bottom: 16px;
        }
        
        .success {
            padding: 12px 16px;
            background: #1a3a1e;
            border-left: 4px solid #4CAF50;
            border-radius: 8px;
            color: #81c784;
            font-size: 14px;
        }
        
        .error {
            padding: 12px 16px;
            background: #3a1e1e;
            border-left: 4px solid #ff6b6b;
            border-radius: 8px;
            color: #ff6b6b;
            font-size: 14px;
        }
        
        .loading {
            padding: 12px 16px;
            background: #3a3a1e;
            border-left: 4px solid #ffd93d;
            border-radius: 8px;
            color: #ffd93d;
            font-size: 14px;
        }
        
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #0f0f1a;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a2a4a;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3a3a5a;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 CS2 Coaching Management</h1>
            <p>Client registration &amp; tracking system</p>
        </div>
        
        <div id="message"></div>
        
        <form id="coachingForm" autocomplete="off">
            
            <!-- Client Information -->
            <div class="section-title">
                <span class="icon">👤</span> Client Information
            </div>
            <div class="form-group">
                <label>Name/Nickname <span class="required">*</span></label>
                <input type="text" id="name" placeholder="Enter client's name or nickname" required>
            </div>
            
            <!-- Contact Information -->
            <div class="section-title">
                <span class="icon">📱</span> Contact Information <span style="color:#4a4a6a;font-weight:400;font-size:12px;">(at least one required)</span>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="email" placeholder="client@email.com">
                </div>
                <div class="form-group">
                    <label>Telegram</label>
                    <input type="text" id="telegram" placeholder="@username">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Steam</label>
                    <input type="text" id="steam" placeholder="Steam ID or profile URL">
                </div>
                <div class="form-group">
                    <label>Discord</label>
                    <input type="text" id="discord" placeholder="username#1234">
                </div>
            </div>
            <div class="form-group">
                <label>WhatsApp</label>
                <input type="text" id="whatsapp" placeholder="+1234567890">
            </div>
            
            <!-- Faceit Profile -->
            <div class="section-title">
                <span class="icon">🎮</span> Faceit Profile
            </div>
            <div class="form-group">
                <label>Faceit Profile URL</label>
                <input type="text" id="faceit" placeholder="https://www.faceit.com/en/players/username" value="-">
                <div class="helper-text">Enter "-" if you don't have a Faceit profile</div>
            </div>
            
            <!-- ELO Information -->
            <div class="section-title">
                <span class="icon">📊</span> ELO Information
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Current ELO</label>
                    <input type="number" id="current_elo" value="1000" min="0" max="10000">
                </div>
                <div class="form-group">
                    <label>MAX ELO</label>
                    <input type="number" id="max_elo" value="1000" min="0" max="10000">
                </div>
            </div>
            
            <!-- Preferred Maps - Tag Input -->
            <div class="section-title">
                <span class="icon">🗺️</span> Preferred Maps
            </div>
            <div class="form-group">
                <label>Select maps (click to add, click X to remove)</label>
                <div class="tag-input-container" id="mapsContainer">
                    <div class="tags" id="mapsTags"></div>
                    <div class="tag-input-wrapper">
                        <input type="text" id="mapsInput" placeholder="Type map name and press Enter..." autocomplete="off">
                        <div class="suggestions" id="mapsSuggestions"></div>
                    </div>
                </div>
                <div class="quick-add-btns" id="mapsQuickAdd">
                    <span class="quick-btn" data-value="Dust II">Dust II</span>
                    <span class="quick-btn" data-value="Mirage">Mirage</span>
                    <span class="quick-btn" data-value="Inferno">Inferno</span>
                    <span class="quick-btn" data-value="Nuke">Nuke</span>
                    <span class="quick-btn" data-value="Overpass">Overpass</span>
                    <span class="quick-btn" data-value="Vertigo">Vertigo</span>
                    <span class="quick-btn" data-value="Ancient">Ancient</span>
                    <span class="quick-btn" data-value="Anubis">Anubis</span>
                    <span class="quick-btn" data-value="All Maps">All Maps</span>
                </div>
                <div class="helper-text">Click a button above or type custom and press Enter</div>
            </div>
            
            <!-- Problems to Fix - Tag Input -->
            <div class="section-title">
                <span class="icon">🎯</span> Problems to Fix
            </div>
            <div class="form-group">
                <label>Select problems (click to add, click X to remove)</label>
                <div class="tag-input-container" id="problemsContainer">
                    <div class="tags" id="problemsTags"></div>
                    <div class="tag-input-wrapper">
                        <input type="text" id="problemsInput" placeholder="Type problem and press Enter..." autocomplete="off">
                        <div class="suggestions" id="problemsSuggestions"></div>
                    </div>
                </div>
                <div class="quick-add-btns" id="problemsQuickAdd">
                    <span class="quick-btn" data-value="Aim">Aim</span>
                    <span class="quick-btn" data-value="Movement">Movement</span>
                    <span class="quick-btn" data-value="Positioning">Positioning</span>
                    <span class="quick-btn" data-value="Disadvantage">Disadvantage</span>
                    <span class="quick-btn" data-value="Entry frager (Opening)">Entry frager</span>
                    <span class="quick-btn" data-value="Defending">Defending</span>
                    <span class="quick-btn" data-value="Lurking/flanking">Lurking/flanking</span>
                    <span class="quick-btn" data-value="Support (Utility knowledge)">Utility knowledge</span>
                    <span class="quick-btn" data-value="Game maker">Game maker</span>
                    <span class="quick-btn" data-value="Active Player">Active Player</span>
                    <span class="quick-btn" data-value="Pressure">Pressure</span>
                    <span class="quick-btn" data-value="Element of surprise">Element of surprise</span>
                </div>
                <div class="helper-text">Click a button above or type custom and press Enter</div>
            </div>
            
            <!-- Availability - Tag Input -->
            <div class="section-title">
                <span class="icon">📅</span> Availability
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Hours per Session</label>
                    <input type="number" id="hours" value="1.5" min="0.5" max="6" step="0.5">
                </div>
                <div class="form-group">
                    <label>Available Days</label>
                    <div class="tag-input-container" id="daysContainer">
                        <div class="tags" id="daysTags"></div>
                        <div class="tag-input-wrapper">
                            <input type="text" id="daysInput" placeholder="Type day and press Enter..." autocomplete="off">
                            <div class="suggestions" id="daysSuggestions"></div>
                        </div>
                    </div>
                    <div class="quick-add-btns" id="daysQuickAdd">
                        <span class="quick-btn" data-value="Monday">Monday</span>
                        <span class="quick-btn" data-value="Tuesday">Tuesday</span>
                        <span class="quick-btn" data-value="Wednesday">Wednesday</span>
                        <span class="quick-btn" data-value="Thursday">Thursday</span>
                        <span class="quick-btn" data-value="Friday">Friday</span>
                        <span class="quick-btn" data-value="Saturday">Saturday</span>
                        <span class="quick-btn" data-value="Sunday">Sunday</span>
                    </div>
                    <div class="helper-text">Click a button above or type custom and press Enter</div>
                </div>
            </div>
            
            <!-- Additional Notes -->
            <div class="section-title">
                <span class="icon">📝</span> Additional Notes
            </div>
            <div class="form-group">
                <textarea id="notes" placeholder="Any additional information or special requirements..."></textarea>
            </div>
            
            <button type="submit" class="submit-btn" id="submitBtn">📤 Submit Client Profile</button>
        </form>
    </div>
    
    <script>
        // ==================== TAG INPUT SYSTEM ====================
        function createTagInput(containerId, inputId, tagsId, suggestionsId, suggestionsList, placeholder) {
            const container = document.getElementById(containerId);
            const input = document.getElementById(inputId);
            const tagsContainer = document.getElementById(tagsId);
            const suggestionsContainer = document.getElementById(suggestionsId);
            
            let tags = [];
            
            // Set placeholder
            input.placeholder = placeholder || 'Type and press Enter...';
            
            // Add suggestion click handlers
            function updateSuggestions(value) {
                suggestionsContainer.innerHTML = '';
                if (!value.trim()) return;
                
                const matches = suggestionsList.filter(s => 
                    s.toLowerCase().includes(value.toLowerCase()) && 
                    !tags.includes(s)
                );
                
                matches.slice(0, 6).forEach(suggestion => {
                    const el = document.createElement('span');
                    el.className = 'suggestion';
                    el.textContent = suggestion;
                    el.addEventListener('click', () => {
                        addTag(suggestion);
                        input.value = '';
                        suggestionsContainer.innerHTML = '';
                    });
                    suggestionsContainer.appendChild(el);
                });
            }
            
            function addTag(value) {
                value = value.trim();
                if (!value) return;
                if (tags.includes(value)) {
                    input.value = '';
                    suggestionsContainer.innerHTML = '';
                    return;
                }
                tags.push(value);
                renderTags();
                input.value = '';
                suggestionsContainer.innerHTML = '';
                input.focus();
            }
            
            function removeTag(value) {
                tags = tags.filter(t => t !== value);
                renderTags();
            }
            
            function renderTags() {
                tagsContainer.innerHTML = '';
                tags.forEach(tag => {
                    const tagEl = document.createElement('span');
                    tagEl.className = 'tag';
                    tagEl.innerHTML = `${tag} <span class="remove-tag" data-value="${tag}">×</span>`;
                    tagEl.querySelector('.remove-tag').addEventListener('click', (e) => {
                        removeTag(e.target.dataset.value);
                    });
                    tagsContainer.appendChild(tagEl);
                });
            }
            
            // Quick add buttons
            const containerEl = document.getElementById(containerId);
            const quickAddContainer = containerEl.parentElement.querySelector('.quick-add-btns');
            if (quickAddContainer) {
                quickAddContainer.querySelectorAll('.quick-btn').forEach(btn => {
                    btn.addEventListener('click', () => {
                        addTag(btn.dataset.value);
                    });
                });
            }
            
            // Input events
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    addTag(input.value);
                }
                if (e.key === 'Backspace' && !input.value && tags.length > 0) {
                    removeTag(tags[tags.length - 1]);
                }
            });
            
            input.addEventListener('input', () => {
                updateSuggestions(input.value);
            });
            
            input.addEventListener('blur', () => {
                setTimeout(() => {
                    suggestionsContainer.innerHTML = '';
                }, 200);
            });
            
            // Public methods
            return {
                getTags: () => tags,
                setTags: (newTags) => { tags = newTags; renderTags(); },
                clear: () => { tags = []; renderTags(); },
                addTag: addTag
            };
        }
        
        // ==================== SUGGESTIONS ====================
        const mapSuggestions = ['Dust II', 'Mirage', 'Inferno', 'Nuke', 'Overpass', 'Vertigo', 'Ancient', 'Anubis', 'All Maps'];
        const problemSuggestions = ['Aim', 'Movement', 'Positioning', 'Disadvantage', 'Entry frager (Opening)', 'Defending', 'Lurking/flanking', 'Support (Utility knowledge)', 'Game maker', 'Active Player', 'Pressure', 'Element of surprise'];
        const daySuggestions = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        
        // ==================== INITIALIZE TAG INPUTS WITH DEFAULT VALUES ====================
        const mapsTagInput = createTagInput('mapsContainer', 'mapsInput', 'mapsTags', 'mapsSuggestions', mapSuggestions, 'Type map name and press Enter...');
        const problemsTagInput = createTagInput('problemsContainer', 'problemsInput', 'problemsTags', 'problemsSuggestions', problemSuggestions, 'Type problem and press Enter...');
        const daysTagInput = createTagInput('daysContainer', 'daysInput', 'daysTags', 'daysSuggestions', daySuggestions, 'Type day and press Enter...');
        
        // ==================== FORM SUBMISSION ====================
        const form = document.getElementById('coachingForm');
        const submitBtn = document.getElementById('submitBtn');
        const messageDiv = document.getElementById('message');
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = {
                name: document.getElementById('name').value.trim(),
                email: document.getElementById('email').value.trim(),
                telegram: document.getElementById('telegram').value.trim(),
                steam: document.getElementById('steam').value.trim(),
                discord: document.getElementById('discord').value.trim(),
                whatsapp: document.getElementById('whatsapp').value.trim(),
                faceit: document.getElementById('faceit').value.trim() || '-',
                current_elo: parseInt(document.getElementById('current_elo').value) || 0,
                max_elo: parseInt(document.getElementById('max_elo').value) || 0,
                maps: mapsTagInput.getTags().join(', '),
                problems: problemsTagInput.getTags().join(', '),
                hours_per_session: parseFloat(document.getElementById('hours').value) || 0,
                days: daysTagInput.getTags().join(', '),
                additional_notes: document.getElementById('notes').value.trim()
            };
            
            // Validation
            if (!data.name) {
                messageDiv.innerHTML = '<div class="error">❌ Name is required!</div>';
                return;
            }
            
            const contacts = [data.email, data.telegram, data.steam, data.discord, data.whatsapp];
            if (!contacts.some(c => c)) {
                messageDiv.innerHTML = '<div class="error">❌ At least one contact method is required!</div>';
                return;
            }
            
            if (mapsTagInput.getTags().length === 0) {
                messageDiv.innerHTML = '<div class="error">❌ Please add at least one map!</div>';
                return;
            }
            
            if (problemsTagInput.getTags().length === 0) {
                messageDiv.innerHTML = '<div class="error">❌ Please add at least one problem!</div>';
                return;
            }
            
            if (daysTagInput.getTags().length === 0) {
                messageDiv.innerHTML = '<div class="error">❌ Please add at least one available day!</div>';
                return;
            }
            
            // Submit
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Submitting...';
            messageDiv.innerHTML = '<div class="loading">⏳ Sending data to Google Sheets...</div>';
            
            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    messageDiv.innerHTML = '<div class="success">✅ ' + result.message + '</div>';
                    form.reset();
                    document.getElementById('faceit').value = '-';
                    document.getElementById('current_elo').value = '1000';
                    document.getElementById('max_elo').value = '1000';
                    document.getElementById('hours').value = '1.5';
                    mapsTagInput.clear();
                    problemsTagInput.clear();
                    daysTagInput.clear();
                } else {
                    messageDiv.innerHTML = '<div class="error">❌ ' + result.message + '</div>';
                }
            } catch (error) {
                messageDiv.innerHTML = '<div class="error">❌ Connection error: ' + error + '</div>';
            }
            
            submitBtn.disabled = false;
            submitBtn.textContent = '📤 Submit Client Profile';
        });
    </script>
</body>
</html>'''
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:8501')

def run_server():
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    create_index_html()
    
    port = 8501
    server = HTTPServer(('localhost', port), MyHandler)
    print(f"✅ Server running at http://localhost:{port}")
    print("   Press Ctrl+C to stop")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    run_server()