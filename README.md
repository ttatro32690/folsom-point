# AI-Enabled Agent Platform

This project is an AI-enabled agent platform developed with Python, FastAPI, PyTorch, Hugging Face Transformers, LangChain, Elasticsearch, and Next.js with TypeScript.

## Project Structure

ai-agent-platform/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── db/
│   │   └── init/
│   │       └── 01-init.sql
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx
│   ├── styles/
│   │   ├── globals.css
│   │   └── Home.module.css
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
└── README.md

## Setup Instructions

1. Clone the repository
2. Install backend dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```
4. Set up environment variables (copy `.env.example` to `.env` and fill in the values)
5. Run the development server:
   ```
   docker-compose up --build
   ```

## Database Initialization

The PostgreSQL database is automatically initialized with the necessary tables when the container starts up. The initialization script can be found in `backend/db/init/01-init.sql`. If you need to modify the database schema, update this file and rebuild the containers.

## Development

- Backend: The FastAPI application is located in the `backend/` directory.
- Frontend: The Next.js application with TypeScript is located in the `frontend/` directory.

## TypeScript

The frontend uses TypeScript for improved developer experience and type safety. The TypeScript configuration can be found in `frontend/tsconfig.json`.

## Testing

Run backend tests using pytest:

## Ollama


To pull the latest model from Ollama, run the following command:
```
docker exec -it ollama ./ollama pull llama3.2
```

All other commands can be run with docker following the (README.md)[https://github.com/ollama/ollama/blob/main/README.md]:
