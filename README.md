# Prokoi Agents - AI-Powered Project Management Assistant

An intelligent project management system that uses AI agents to break down high-level project descriptions into granular, actionable development tasks. Built with FastAPI, LangGraph, and Celery for asynchronous task processing.

## Features

- **AI-Driven Task Breakdown**: Convert project descriptions into structured development issues
- **Asynchronous Processing**: Uses Celery with Redis for background task execution
- **RESTful API**: FastAPI-based endpoints for project interaction
- **LangGraph Integration**: Orchestrates AI agents using graph-based workflows
- **Docker Support**: Containerized deployment with docker-compose

## Architecture

- **FastAPI Server** (`main.py`): HTTP API endpoints
- **LangGraph Workflow** (`app/graph.py`): AI agent orchestration
- **Celery Tasks** (`app/tasks.py`): Background job processing
- **State Management** (`app/state.py`): Data structures for agent state
- **Custom Tools** (`app/tools.py`): Project management tools and integrations

## Prerequisites

- Docker and Docker Compose
- Redis Cloud account (or local Redis instance)
- OpenAI API key

## Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HeyMahdy/prokoi_agents.git
   cd prokoi_agents
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Configure your `.env` file**:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   REDIS_URL=redis://username:password@your-redis-cloud-endpoint:port/0
   ```

## Running with Docker

### Using Docker Compose (Recommended)

1. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Run in detached mode**:
   ```bash
   docker-compose up -d --build
   ```

3. **View logs**:
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f api
   docker-compose logs -f worker
   ```

4. **Stop services**:
   ```bash
   docker-compose down
   ```

### Manual Docker Build

1. **Build the image**:
   ```bash
   docker build -t prokoi-agents .
   ```

2. **Run the API server**:
   ```bash
   docker run -p 8000:8000 --env-file .env prokoi-agents uvicorn main:app --host 0.0.0.0 --port 8000
   ```

3. **Run the Celery worker**:
   ```bash
   docker run --env-file .env prokoi-agents celery -A app.tasks worker --loglevel=info --queue=agent_queue
   ```

## API Usage

### Create Project Issues

**Endpoint**: `POST /chat`

**Parameters**:
- `project_id`: Integer (query parameter)
- `input`: String (request body) - Project description

**Example**:
```bash
curl -X POST "http://localhost:8000/chat?project_id=1" \
  -H "Content-Type: application/json" \
  -d '{"input": "Create a user authentication system with login, signup, and password reset functionality"}'
```

**Response**:
```json
{
  "task_id": "ab3172fe-f3dd-4528-a547-15457c3b4002"
}
```

### Check Task Status

**Endpoint**: `GET /task/{task_id}`

**Example**:
```bash
curl http://localhost:8000/task/ab3172fe-f3dd-4528-a547-15457c3b4002
```

**Response**:
```json
{
  "status": "completed",
  "response": "Created 5 issues for user authentication system..."
}
```

## Development

### Local Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis** (if using local Redis):
   ```bash
   redis-server
   ```

3. **Start Celery worker**:
   ```bash
   celery -A app.tasks worker --loglevel=info --queue=agent_queue
   ```

4. **Run the API server**:
   ```bash
   uvicorn main:app --reload
   ```

### Project Structure

```
prokoi_agents/
├── app/
│   ├── __init__.py
│   ├── state.py          # Agent state definitions
│   ├── tools.py          # Custom project management tools
│   ├── nodes.py          # LangGraph node implementations
│   ├── graph.py          # Agent workflow graph
│   ├── tasks.py          # Celery task definitions
│   ├── worker.py         # Celery worker configuration
│   ├── middleware.py     # FastAPI middleware
│   └── prompts.py        # AI prompt templates
├── main.py               # FastAPI application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI models | Yes |
| `REDIS_URL` | Redis connection URL | Yes |

### Docker Configuration

- **Base Image**: Python 3.13-slim
- **Package Manager**: uv (faster than pip)
- **Exposed Port**: 8000
- **Working Directory**: `/code`

## Troubleshooting

### Common Issues

1. **Celery task not found**:
   - Ensure task names match between registration and calling
   - Check that worker is discovering tasks properly

2. **Redis connection failed**:
   - Verify Redis Cloud credentials in `.env`
   - Check network connectivity

3. **OpenAI API errors**:
   - Verify API key is valid
   - Check rate limits and quotas

### Debugging

1. **View container logs**:
   ```bash
   docker-compose logs -f worker
   ```

2. **Connect to running container**:
   ```bash
   docker-compose exec api bash
   ```

3. **Monitor Redis queues**:
   - Use Redis CLI or cloud dashboard
   - Check for failed/pending tasks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
