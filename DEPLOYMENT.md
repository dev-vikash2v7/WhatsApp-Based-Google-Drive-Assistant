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

## Step 3: OpenAI API Setup

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

## Step 8: Testing

### 8.1 Test Basic Commands
Send these messages to your WhatsApp number:

```
HELP
LIST /
SUMMARY /ProjectX
```

### 8.2 Test File Operations
```
DELETE /ProjectX/test.pdf
MOVE /ProjectX/file.pdf /Archive
```

### 8.3 Monitor Logs
```bash
# Local installation
tail -f logs/app.log

# Docker installation
docker-compose logs -f whatsapp-drive-assistant
```

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

### Debug Mode
Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python api_server.py
```

### Health Check
Test the API server:
```bash
curl http://localhost:5000/
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **HTTPS**: Always use HTTPS in production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: All user inputs are validated
5. **File Access**: Only authenticated users can access their own files

## Monitoring

### Logs
- Application logs: `logs/app.log`
- Docker logs: `docker-compose logs`
- n8n logs: Check n8n interface

### Metrics
- API response times
- Error rates
- Command usage statistics

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify all credentials are correct
3. Test individual components
4. Review the troubleshooting section above

## License

This project is licensed under the MIT License.
