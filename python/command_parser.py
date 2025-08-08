import re
import logging
from typing import Dict, Optional, Tuple
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommandType(Enum):
    """Enumeration of supported commands"""
    LIST = "LIST"
    DELETE = "DELETE"
    MOVE = "MOVE"
    SUMMARY = "SUMMARY"
    HELP = "HELP"
    UNKNOWN = "UNKNOWN"

class CommandParser:
    """Parser for WhatsApp commands to Google Drive operations"""
    
    def __init__(self):
        """Initialize the command parser"""
        self.supported_commands = {
            "LIST": CommandType.LIST,
            "DELETE": CommandType.DELETE,
            "MOVE": CommandType.MOVE,
            "SUMMARY": CommandType.SUMMARY,
            "HELP": CommandType.HELP,
            "H": CommandType.HELP
        }
    
    def parse_message(self, message: str) -> Dict:
        """Parse WhatsApp message and extract command information"""
        try:
            # Clean and normalize the message
            message = message.strip().upper()
            
            if not message:
                return self._create_error_response("Empty message received")
            
            # Check for help command
            if message in ["HELP", "H", "?"]:
                return self._create_help_response()
            
            # Parse command and parameters
            parts = message.split()
            if len(parts) < 1:
                return self._create_error_response("No command found")
            
            command = parts[0]
            if command not in self.supported_commands:
                return self._create_error_response(f"Unknown command: {command}")
            
            command_type = self.supported_commands[command]
            
            # Parse based on command type
            if command_type == CommandType.LIST:
                return self._parse_list_command(parts)
            elif command_type == CommandType.DELETE:
                return self._parse_delete_command(parts)
            elif command_type == CommandType.MOVE:
                return self._parse_move_command(parts)
            elif command_type == CommandType.SUMMARY:
                return self._parse_summary_command(parts)
            else:
                return self._create_error_response(f"Unsupported command: {command}")
                
        except Exception as e:
            logger.error(f"Error parsing message: {e}")
            return self._create_error_response(f"Error parsing command: {str(e)}")
    
    def _parse_list_command(self, parts: list) -> Dict:
        """Parse LIST command"""
        print("parts" , parts)
        if len(parts) < 2:
            return self._create_error_response("LIST command requires a folder path")
        
        folder_path = parts[1]
        if not self._is_valid_path(folder_path):
            return self._create_error_response("Invalid folder path format")
        
        return {
            "command": "LIST",
            "folder_path": folder_path,
            "success": True
        }
    
    def _parse_delete_command(self, parts: list) -> Dict:
        """Parse DELETE command"""
        if len(parts) < 2:
            return self._create_error_response("DELETE command requires a file path")
        
        file_path = parts[1]
        if not self._is_valid_path(file_path):
            return self._create_error_response("Invalid file path format")
        
        return {
            "command": "DELETE",
            "file_path": file_path,
            "success": True
        }
    
    def _parse_move_command(self, parts: list) -> Dict:
        """Parse MOVE command"""
        if len(parts) < 3:
            return self._create_error_response("MOVE command requires source and destination paths")
        
        source_path = parts[1]
        destination_path = parts[2]
        
        if not self._is_valid_path(source_path):
            return self._create_error_response("Invalid source path format")
        
        if not self._is_valid_path(destination_path):
            return self._create_error_response("Invalid destination path format")
        
        return {
            "command": "MOVE",
            "source_path": source_path,
            "destination_path": destination_path,
            "success": True
        }
    
    def _parse_summary_command(self, parts: list) -> Dict:
        """Parse SUMMARY command"""
        if len(parts) < 2:
            return self._create_error_response("SUMMARY command requires a folder path")
        
        folder_path = parts[1]
        if not self._is_valid_path(folder_path):
            return self._create_error_response("Invalid folder path format")
        
        return {
            "command": "SUMMARY",
            "folder_path": folder_path,
            "success": True
        }
    
    def _is_valid_path(self, path: str) -> bool:
        """Validate path format"""
        if not path:
            return False
        
        # Path should start with /
        if not path.startswith('/'):
            return False
        
        # Path should not contain invalid characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            if char in path:
                return False
        
        # Path should not be too long
        if len(path) > 255:
            return False
        
        return True
    
    def _create_error_response(self, message: str) -> Dict:
        """Create error response"""
        return {
            "success": False,
            "error": message
        }
    
    def _create_help_response(self) -> Dict:
        """Create help response"""
        help_text = """
🤖 *WhatsApp Drive Assistant*

*Available Commands:*

📁 *LIST /FolderName*
   List all files in a folder
   Example: `LIST /ProjectX`

🗑️ *DELETE /FolderName/file.pdf*
   Delete a specific file
   Example: `DELETE /ProjectX/report.pdf`

📦 *MOVE /Source/file.pdf /Destination*
   Move file to different folder
   Example: `MOVE /ProjectX/report.pdf /Archive`

📋 *SUMMARY /FolderName*
   Generate AI summaries of all documents
   Example: `SUMMARY /ProjectX`

❓ *HELP* or *H*
   Show this help message

*Notes:*
• Use forward slashes (/) for paths
• Folder names are case-sensitive
• Supported documents: PDF, DOCX, Google Docs, TXT
        """
        
        return {
            "success": True,
            "command": "HELP",
            "help_text": help_text.strip()
        }
    
    def format_response(self, result: Dict) -> str:
        """Format the parsed command result into a response message"""
        if not result.get("success", False):
            return f"❌ {result.get('error', 'Unknown error')}"
        
        command = result.get("command")
        
        if command == "HELP":
            return result.get("help_text", "Help not available")
        
        # For other commands, return a confirmation message
        if command == "LIST":
            folder = result.get("folder_path", "")
            return f"📁 Listing files in: {folder}"
        
        elif command == "DELETE":
            file_path = result.get("file_path", "")
            return f"🗑️ Deleting file: {file_path}"
        
        elif command == "MOVE":
            source = result.get("source_path", "")
            dest = result.get("destination_path", "")
            return f"📦 Moving file from {source} to {dest}"
        
        elif command == "SUMMARY":
            folder = result.get("folder_path", "")
            return f"📋 Generating summaries for: {folder}"
        
        return "✅ Command parsed successfully"
