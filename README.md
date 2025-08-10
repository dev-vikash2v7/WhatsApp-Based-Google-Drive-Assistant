# WhatsApp-Driven Google Drive Assistant

A comprehensive n8n workflow that enables WhatsApp users to interact with Google Drive through simple text commands.

## Features

- **WhatsApp Integration**: Uses Twilio Sandbox for WhatsApp messaging
- **Google Drive Operations**: List, delete, move files and folders
- **AI Summarization**: Generate summaries of documents using OpenAI GPT-4
- **Command Parsing**: Simple text-based command interface

## Commands

- `LIST /ProjectX` - List files in /ProjectX folder
- `DELETE /ProjectX/report.pdf` - Delete specific file
- `MOVE /ProjectX/report.pdf /Archive` - Move file to different folder
- `SUMMARY /ProjectX` - Generate AI summaries of all documents in folder



## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   - Set up Google Drive API credentials
   - Configure Twilio WhatsApp credentials
   - Set OpenAI API key

3. **Import n8n Workflow**
   - Import the workflow JSON into your n8n instance
   - Configure the webhook endpoints

4. **Deploy Python Scripts**
   - Deploy Python scripts to your server
   - Update webhook URLs in n8n workflow

## Environment Variables

```bash
GOOGLE_DRIVE_CREDENTIALS_FILE=path/to/credentials.json
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
GEMINI_API_KEY=your_openai_key
```

## Usage

1. Send WhatsApp message to Twilio number
2. Use commands like: `LIST /ProjectX`
3. Receive response with file list or operation result
4. For summaries: `SUMMARY /ProjectX` returns AI-generated summaries

## Security

- All operations are performed within authenticated user's Google Drive
- OAuth2 authentication for Google Drive
- Secure API key management
- Input validation and sanitization
