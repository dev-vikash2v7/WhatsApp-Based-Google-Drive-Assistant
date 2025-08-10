# WhatsApp-Driven Google Drive Assistant

A comprehensive n8n workflow that enables WhatsApp users to interact with Google Drive through simple text commands.

## Features

- **WhatsApp Integration**: Uses Twilio Sandbox for WhatsApp messaging
- **Google Drive Operations**: List, delete, move , copy files and summarize folders & file
- **AI Summarization**: Generate summaries of documents using OpenAI GPT-4
- **Command Parsing**: Simple text-based command interface

## Commands

- `LIST /ProjectX` - List files in /ProjectX folder
- `DELETE /ProjectX/report.pdf` - Delete specific file
- `MOVE /ProjectX/report.pdf /Archive` - Move file to different folder
- `Copy /ProjectX/report.pdf /Archive` - Copy file to different folder
- `FolderSummary /ProjectX` - Generate AI summaries of all documents in folder
- `FileSummary /ProjectX/report.pdf` - Generate AI summaries of specific document in folder


## Setup Instructions


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


### 1.3 Download credentials.json
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

#### 5.2 Start API Server
```bash
python api_server.py
```

## Step 6: n8n Setup

3. **Import n8n Workflow**
   - Import the workflow JSON into your n8n instance

   - Copy the webhook production url to <a href="https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1"> Twilio Sendbox settings </a>

4. **Deploy Python Scripts**
   - run ngrok ``` ngrok http 5000 ```
   - copy ngrokUrl + /api/execute to the 'HTTP Request' Node url in n8n
    - Eg : ``` https://e32f114262b4.ngrok-free.app/api/execute```



5. **Twilio Webhook Configuration**

   - Go to Twilio Console > Messaging > Settings > WhatsApp Sandbox Settings
   - Set the webhook URL to your n8n webhook endpoint
   - Format: `https://your-n8n-instance.com/webhook/whatsapp-drive-assistant`


6. **Save changes and activate n8n**

## Step 7 : Open Whatsapp 

1. Open Whatsapp <a href="https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1">twilio sendbox
</a>

2. Type **Help** and send to start the conversation






### Option B: Docker Deployment

#### 5.1 Build and Run with Docker Compose
```bash
docker-compose up -d
```

#### 5.2 Check Status
```bash
docker-compose ps
docker-compose logs whatsapp-drive-assistant
```

## Step 6: n8n Workflow Setup

### 6.1 Import Workflow
1. Open your n8n instance
2. Import the workflow from `n8n-workflows/whatsapp-drive-assistant.json`
3. Configure the webhook URL

### 6.2 Configure Credentials
1. Add Twilio credentials in n8n
2. Set up HTTP Basic Auth for Twilio API calls
3. Configure environment variables in n8n

### 6.3 Update Webhook URL
1. Update the API server URL in the workflow
2. Ensure the webhook is accessible from n8n

## Step 7: Twilio Webhook Configuration

### 7.1 Configure Webhook URL
1. Go to Twilio Console > Messaging > Settings > WhatsApp Sandbox Settings
2. Set the webhook URL to your n8n webhook endpoint
3. Format: `https://your-n8n-instance.com/webhook/whatsapp-drive-assistant`

### 7.2 Test Configuration
1. Send a message to your Twilio WhatsApp number
2. Check if the webhook receives the message
3. Verify the response is sent back


## Step 9: Production Deployment

### 9.1 SSL Certificate
For production, obtain SSL certificate:
```bash
# Using Let's Encrypt
certbot certonly --standalone -d your-domain.com
```

### 9.2 Nginx Configuration
Create `nginx.conf`:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream api_server {
        server whatsapp-drive-assistant:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        location / {
            proxy_pass http://api_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 9.3 Production Deployment
```bash
# Start with production profile
docker-compose --profile production up -d
```



## Troubleshooting

### Common Issues

#### 1. Google Drive Authentication
- Ensure `credentials.json` is in the correct location
- Check if the service account has proper permissions
- Verify the scopes are correctly configured

#### 2. Twilio Webhook Issues
- Check if the webhook URL is accessible
- Verify Twilio credentials are correct
- Ensure the WhatsApp number format is correct

#### 3. OpenAI API Errors
- Verify the API key is valid
- Check if you have sufficient credits
- Ensure the model name is correct

#### 4. n8n Workflow Issues
- Check if all nodes are properly connected
- Verify environment variables are set
- Test individual nodes for errors


### Logs
- Application logs: `logs/app.log`
- Docker logs: `docker-compose logs`
- n8n logs: Check n8n interface

