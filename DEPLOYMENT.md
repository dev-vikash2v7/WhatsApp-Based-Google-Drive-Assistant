# WhatsApp Drive Assistant - Deployment Guide


## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (optional)
- n8n instance (Workflow)
- Twilio account (For Whatsapp )
- Google Cloud Platform account (Google Drive)
- Gemini API key (Summarization)

## Step 1: Google Drive API Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Drive API

### 1.2 Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name it "WhatsApp Drive Assistant"
4. Grant "Editor" role
5. Create and download the JSON key file
6. Save as `credentials.json` in the project root

### 1.3 Configure OAuth2 (Alternative)
If you prefer OAuth2 authentication:
1. Go to "APIs & Services" > "Credentials"
2. Create OAuth 2.0 Client ID
3. Download the credentials file
4. Save as `credentials.json`

## Step 2: Twilio WhatsApp Setup

### 2.1 Create Twilio Account
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token

### 2.2 Setup WhatsApp Sandbox
1. Go to Twilio Console > Messaging > Try it out > Send a WhatsApp message
2. Follow instructions to join the sandbox
3. Note your WhatsApp number (format: whatsapp:+14155238886)

## Step 3: Gemini Setup

### 3.1 Get API Key
1. Go to [Gemini Platform](https://ai.google.dev/)
2. Create account and get API key
3. Note your API key for configuration

## Step 4: Environment Configuration

### 4.1 Copy Environment Template
```bash
cp env.example .env
```

### 4.2 Update Environment Variables
Edit `.env` file with your credentials:

```bash
# Google Drive API Configuration
GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json

# OpenAI API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# API Server Configuration
API_SERVER_URL=https://your-domain.com
FLASK_ENV=production
PORT=5000

```

## Step 5: Installation

### Option A: Local Installation

#### 5.1 Run Setup Script
```bash
python setup.py
```

#### 5.2 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5.3 Start API Server
```bash
python api_server.py
```




