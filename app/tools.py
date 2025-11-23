import os
import requests
from langchain_core.tools import tool
from typing import Literal, Optional

# Method 1: Direct tool with environment variable (Simplest)
@tool
def create_project_issue(
    project_id: int,
    title: str,
    description: str,
    type_id: int,
    token:str,
    story_points: int = 0,
    priority: Literal["low", "medium", "high"] = "medium",
    status: str = "open"    
):
    """
    Creates a new issue (Story, Task, Bug, etc.) in the project management system.
    
    Args:
        project_id (int): The ID of the project to add the issue to.
        title (str): A concise summary of the issue.
        description (str): Detailed technical description or acceptance criteria.
        type_id (int): The numeric ID for the issue type:
                       24=Story, 23=Task, 21=Bug, 25=Epic, 22=Feature.
        story_points (int, optional): Fibonacci complexity estimate (1, 2, 3, 5, 8). Default 0.
        priority (str, optional): Importance level ("low", "medium", "high"). Default "medium".
        status (str, optional): Current state. Default "open".
        token (str) : token is needed for endpoint authentication. token is already provided
    
    Returns:
        dict: The API response containing the created issue details.
    """
    jwt_token = token
    
    if not jwt_token:
        return {
            "error": "Authentication failed",
            "details": "JWT_TOKEN not found in environment variables"
        }
    
    # Construct the payload
    payload = {
        "title": title,
        "description": description,
        "story_points": story_points,
        "status": status,
        "priority": priority,
        "project_id": project_id,
        "type_id": type_id
    }
    
    # Set up headers with JWT token
    print(token)
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    # API endpoint
    api_url = f"http://localhost:8000/api/projects/{project_id}/issues"
    
    try:
        # Send authenticated request
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (4xx, 5xx)
        print(e)
        return {
            "error": f"HTTP {response.status_code} error",
            "details": str(e),
            "response_body": response.text if response else None,
            "payload_attempted": payload
        }
    
    except requests.exceptions.RequestException as e:
        # Handle other request errors (connection, timeout, etc.)
        return {
            "error": "Failed to create issue",
            "details": str(e),
            "payload_attempted": payload
        }


tools = [create_project_issue]
tools_by_name={ tool.name:tool for tool in tools}
