from tools import create_project_issue
args = {
    "project_id": 82,
    "title": "Fix database connection",
    "description": "Connection times out after 30 seconds",
    "type_id": 16,  # 18 = Bug
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoQGdtYWlsLmNvbSIsImV4cCI6MTc2Mzc0MDI3NX0.nM3vl1_Ddx_OGuEVep9Xt1Bynvb9LnYOB49meE-1VVI", # Your actual JWT token here
    "story_points": 5,
    "priority": "high",
    "status": "open"
}

# 2. Call invoke
result = create_project_issue.invoke(args)

# 3. Print the result
print(result)