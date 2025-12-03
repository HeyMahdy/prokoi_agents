from tools import create_project_issue
args = {
    "project_id": 1,
    "title": "Fix  connection",
    "description": "Connection times out after 30 seconds",
    "type_id": 1,  # 18 = Bug
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYWhkeUBnbWFpbC5jb20iLCJleHAiOjE3NjQ3ODA0NDF9.VX9M9XhbYDFHtiJpy7kcpd92bqEUhaaIvP_VxtuDgsQ", # Your actual JWT token here
    "story_points": 5,
    "priority": "high",
    "status": "open"
}

# 2. Call invoke
result = create_project_issue.invoke(args)

# 3. Print the result
print(result)