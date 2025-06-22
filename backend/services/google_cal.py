# import other packages
import os
from dotenv import load_dotenv
import datetime
import pickle

# import google packages
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class GoogleCalendarAPI:
    def __init__(self):
        """
        initializes the scope and sets up the environment to access to the token and cred
        """
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None
        self.service = None


    def authenticate(self, credentials_path='credentials.json', token_path='calendar_token.pickle'):
        """authenticate users with google calendar api using OAuth 2.0"""
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                self.creds = pickle.load(token)
            
        # after extracting the tokens.pickle, is it valid
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                print("Refreshing expired calendar credentials...")
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
                
                print(f"Starting Calendar OAuth flow with scopes: {self.SCOPES}")
                # need to access the credentials 
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                # access this scope with the credential and see if its valid
                self.creds = flow.run_local_server(port=8080)
                print("Calendar OAuth authentication completed successfully!")
            # serializes the object self.creds into the token which is the path
            with open(token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        # service is available
        self.service = build('calendar', 'v3', credentials=self.creds)
        print(f"Calendar service initialized with scopes: {self.creds.scopes}")

    def create_event(self, summary: str = "Doctor Appointment",
                     description: str = "Appointment Description",
                     start_time: datetime = None,
                     end_time: datetime = None,
                     timezone: str = "America/New_York"):
        """
        schedules the apppointment onto the google calendar
        """
        if not self.service:
            raise ValueError("Please authenticate first using authenticate()")

        # we need to confirt the start time into the iso format
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # build the body that will be passed into the calendar as a service
        event = {
            'summary': summary,
            'description' : description,
            'start': {
                'dateTime': start_time_str,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time_str,
                'timeZone': timezone
            },
        }

        # make the calendar appointment service
        try:
            event = self.service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
            return event['id']
        except Exception as e:
            raise Exception(f"Failed to create event: {str(e)}")

class ScheduleAppointmentTool:
    def __init__(self):
        self.calendar_api = None  # Lazy initialization
    
    def _ensure_authenticated(self):
        """Ensure the calendar API is authenticated before use"""
        if self.calendar_api is None:
            self.calendar_api = GoogleCalendarAPI()
            try:
                self.calendar_api.authenticate()
            except Exception as e:
                print(f"Warning: Failed to initialize Google Calendar API: {str(e)}")
                raise
    
    def execute(self, summary: str, description: str, start_time: str, end_time: str, timezone: str = "America/New_York"):
        """Execute the appointment scheduling"""
        try:
            self._ensure_authenticated()
            
            # Parse datetime strings to datetime objects
            start_dt = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            # Create the event
            event_id = self.calendar_api.create_event(
                summary=summary,
                description=description,
                start_time=start_dt,
                end_time=end_dt,
                timezone=timezone
            )
            return f"Appointment scheduled successfully! Event ID: {event_id}"
        except Exception as e:
            return f"Failed to schedule appointment: {str(e)}"
    
    def to_openai_tool(self):
        """Convert to OpenAI tool format"""
        return {
            "type": "function",
            "function": {
                "name": "schedule_appointment",
                "description": "Schedule an appointment on Google Calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Title of the appointment"
                        },
                        "description": {
                            "type": "string", 
                            "description": "Description of the appointment"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time in ISO format (YYYY-MM-DDTHH:MM:SS)"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "End time in ISO format (YYYY-MM-DDTHH:MM:SS)"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone (default: America/New_York)"
                        }
                    },
                    "required": ["summary", "description", "start_time", "end_time"]
                }
            }
        }
        
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(script_dir)
    
    os.chdir(backend_dir)
    print(f"Changed to backend directory: {os.getcwd()}")
    
    google_cal = GoogleCalendarAPI()
    google_cal.authenticate()
    google_cal.create_event(summary="Test Event", description="Test Description", start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(hours=1))