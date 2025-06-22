from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle
from email.mime.text import MIMEText
import base64

class GmailAPI:
    def __init__(self):
        """
        Initializes the scope and sets up the environment to access the token and credentials
        """
        # Use more comprehensive scopes for Gmail API
        self.SCOPES = [
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.compose',
            'https://www.googleapis.com/auth/gmail.modify'
        ]
        self.creds = None
        self.service = None

    def authenticate(self, credentials_path='credentials.json', token_path='token.pickle'):
        """Authenticate users with Gmail API using OAuth 2.0"""
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # Check if credentials are valid
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Refreshing expired credentials...")
                self.creds.refresh(Request())
            else:
                # Check if credentials.json exists
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(
                        "credentials.json not found. Please download it from Google Cloud Console:\n"
                        "1. Go to https://console.cloud.google.com/\n"
                        "2. Navigate to APIs & Services > Credentials\n"
                        "3. Download the OAuth 2.0 Client ID credentials\n"
                        "4. Save as 'credentials.json' in the backend directory"
                    )
                
                print(f"Starting OAuth flow with scopes: {self.SCOPES}")
                # Need to access the credentials
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                # Access this scope with the credential and see if it's valid
                self.creds = flow.run_local_server(port=8080)
                print("OAuth authentication completed successfully!")
            
            # Serialize the object self.creds into the token which is the path
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Service is available
        self.service = build('gmail', 'v1', credentials=self.creds)
        print(f"Gmail service initialized with scopes: {self.creds.scopes}")

    def send_email(self, to: str, subject: str, body: str, from_email: str = None):
        """
        Send an email using Gmail API
        """
        if not self.service:
            raise ValueError("Please authenticate first using authenticate()")

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        # Use 'me' as the sender (authenticated user's email)
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body_data = {'raw': raw}

        try:
            sent = self.service.users().messages().send(userId='me', body=body_data).execute()
            return sent['id']
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

class SendEmailTool:
    def __init__(self):
        self.gmail_api = GmailAPI()
        try:
            self.gmail_api.authenticate()
        except Exception as e:
            print(f"Warning: Failed to initialize Gmail API: {str(e)}")
    
    def execute(self, to: str, subject: str, body: str):
        """Execute the email sending"""
        try:
            # Send the email
            message_id = self.gmail_api.send_email(
                to=to,
                subject=subject,
                body=body
            )
            return f"Email sent successfully! Message ID: {message_id}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"
    
    def to_openai_tool(self):
        """Convert to OpenAI tool format"""
        return {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send an email using Gmail API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "string", 
                            "description": "Email subject line"
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body content"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            }
        }

# Legacy functions for backward compatibility
def authenticate_gmail():
    """Legacy function for backward compatibility"""
    gmail_api = GmailAPI()
    gmail_api.authenticate()
    return gmail_api.creds

def send_email(creds, to, subject, body):
    """Legacy function for backward compatibility"""
    gmail_api = GmailAPI()
    gmail_api.creds = creds
    gmail_api.service = build('gmail', 'v1', credentials=creds)
    message_id = gmail_api.send_email(to, subject, body)
    print(f"Message Id: {message_id}")
    return message_id

# Example usage
if __name__ == '__main__':
    # Test the new tool
    email_tool = SendEmailTool()
    result = email_tool.execute(
        to="test@example.com",
        subject="Test Email",
        body="This is a test email from the Gmail API tool."
    )
    print(result)
