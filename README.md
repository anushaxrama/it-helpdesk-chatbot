# AI Helpdesk Chatbot

An intelligent IT support chatbot powered by LangChain, OpenAI, and modern web technologies. This application provides automated assistance for common IT issues like Wi-Fi setup, password resets, software installation, and A/V troubleshooting.

## Features

- **Intelligent Chat Interface**: Natural language processing for IT queries
- **Knowledge Base Integration**: RAG-powered retrieval from structured IT documentation
- **Contextual Memory**: Remembers conversation context for better assistance
- **Quick Actions**: Pre-defined buttons for common IT tasks
- **A/V Troubleshooting**: Specialized logic for audio/video device issues
- **Escalation System**: Automatic ticket generation for unresolved issues
- **Analytics Dashboard**: Track query patterns and resolution rates
- **Beautiful UI**: Modern, responsive design with Tailwind CSS

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   React +   │ HTTP │   FastAPI    │      │   LangChain +   │
│  TypeScript │─────▶│   Backend    │─────▶│   OpenAI API    │
│   + Tailwind│      │              │      │                 │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   ChromaDB   │
                     │ (Vector Store)│
                     └──────────────┘
```

## Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - High-performance async API framework
- **LangChain** - AI orchestration framework
- **OpenAI API** - Large language model
- **ChromaDB** - Vector database for embeddings
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool
- **Axios** - HTTP client

### Database & Storage
- **ChromaDB** - Vector embeddings storage
- **JSON** - Knowledge base documents

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm
- OpenAI API key (or Gemini API key)

### Installation

#### 1. Clone and Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

#### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
```

#### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

Visit `http://localhost:5173` to use the chatbot!

## Project Structure

```
langchain/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── chat_engine.py          # LangChain RAG pipeline
│   ├── knowledge_base.py       # Knowledge base loader
│   ├── models.py               # Pydantic models
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── data/
│       └── it_knowledge.csv    # IT support knowledge base
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── QuickActions.tsx
│   │   ├── api/
│   │   │   └── chatApi.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── vite.config.ts
├── docker-compose.yml          # Docker orchestration
├── Dockerfile.backend          # Backend container
├── Dockerfile.frontend         # Frontend container
└── README.md
```

## Example Queries

Try asking the chatbot:
- "How do I connect to the company Wi-Fi?"
- "My Zoom audio isn't working"
- "I need to reset my password"
- "The projector isn't detecting my laptop"
- "How do I install Microsoft Teams?"

## UI Features

- **Clean Chat Interface**: Messages with sender avatars and timestamps
- **Quick Action Buttons**: One-click access to common IT tasks
- **Typing Indicators**: Real-time feedback during bot responses
- **Conversation History**: Scrollable message history
- **Responsive Design**: Works on desktop and mobile
- **Dark Mode Support**: Easy on the eyes (optional)

## 🔧 Configuration

### Backend Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.7
MAX_TOKENS=500
CORS_ORIGINS=http://localhost:5173
```

### Frontend Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Knowledge Base Format

The IT knowledge base is stored in `backend/data/it_knowledge.csv`:

```csv
category,issue,solution,keywords
networking,wifi_connection,"1. Click Wi-Fi icon 2. Select 'CompanyWiFi' 3. Enter password...",wifi,network,connection
password,reset_password,"Visit https://portal.company.com/reset...",password,reset,forgot
...
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access application at http://localhost:80
```

### Production Deployment Options

- **Backend**: Render, Railway, AWS Lambda, Google Cloud Run
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: Pinecone (managed vector DB) or self-hosted ChromaDB

## How It Works

1. **User Query**: User types a question in the chat interface
2. **API Request**: Frontend sends query to FastAPI backend
3. **Embedding**: Query is converted to vector embedding
4. **Retrieval**: ChromaDB finds most relevant knowledge base entries
5. **Generation**: LangChain + OpenAI generate contextual response
6. **Memory**: Conversation context is maintained for follow-ups
7. **Response**: Answer is streamed back to the user

## Resume Description

**Helpdesk Chatbot for IT Support (AI | UX | Automation)**
*LangChain | Python | React | FastAPI | ChromaDB | Tailwind CSS*

• Built an AI-driven IT helpdesk chatbot that resolves technical queries using natural language interface
• Integrated LangChain RAG pipeline to connect user queries with structured troubleshooting knowledge base
• Designed responsive chat UI in React + TypeScript with Tailwind CSS for white-glove IT support experience
• Implemented contextual memory and fallback escalation to support ticket generation
• Deployed production-ready application with Docker, handling 50+ IT issue categories

## Contributing

This is a portfolio project, but suggestions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation

## Acknowledgments

- Built for demonstrating AI-powered IT support automation
- Designed to showcase full-stack development skills 
- Inspired by modern IT helpdesk systems and conversational AI

---

**Created by**: Anusha Ramachandran
**Purpose**: Portfolio Project for IT Support & AI Skills Demonstration
**Contact**: arama@ucdavis.edu

