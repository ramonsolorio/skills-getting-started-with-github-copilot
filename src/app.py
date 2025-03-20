"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

This API provides endpoints to:
1. View all available extracurricular activities
2. Sign up students for specific activities
3. Manage participant limits for each activity

The application uses in-memory storage for simplicity and serves
a static frontend for user interaction.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

# Initialize FastAPI application with metadata
app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
# Structure:
# {
#    "Activity Name": {
#        "description": "Text description of the activity",
#        "schedule": "Days and times the activity occurs",
#        "max_participants": Maximum number of students allowed (int),
#        "participants": List of student email addresses currently registered
#    }
# }
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "james@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and play basketball games",
        "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["luke@mergington.edu", "matthew@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create projects",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["sarah@mergington.edu", "grace@mergington.edu"]
    },
    "Drama Club": {
        "description": "Participate in plays and improve acting skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["chloe@mergington.edu", "zoe@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation skills and compete in debates",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    }
}


@app.get("/")
def root():
    """
    Redirect root endpoint to the static HTML frontend.
    
    Returns:
        RedirectResponse: Redirects user to the main HTML page
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """
    Retrieve all available activities with their details.
    
    Returns:
        dict: Complete activities dictionary with all activity details and current participants
    """
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """
    Sign up a student for a specific activity.
    
    Args:
        activity_name (str): Name of the activity to join
        email (str): Student's email address used for registration
    
    Returns:
        dict: Success message confirming registration
        
    Raises:
        HTTPException(404): If the requested activity doesn't exist
        HTTPException(400): If the student is already registered for the activity
        HTTPException(400): If the activity has reached maximum capacity
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail=f"{email} is already signed up for {activity_name}")

    # Check if activity has reached maximum capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail=f"Cannot sign up {email} for {activity_name}: maximum participants reached")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
