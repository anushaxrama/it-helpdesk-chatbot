# 🚀 Quick Start Guide

This guide will help you get your IT Helpdesk Chatbot up and running in under 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.11+** installed ([Download here](https://www.python.org/downloads/))
- ✅ **Node.js 18+** and npm installed ([Download here](https://nodejs.org/))
- ✅ **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

---

## 🎯 Step 1: Set Up Backend

### 1.1 Navigate to Backend Directory

```bash
cd backend
```

### 1.2 Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- LangChain (AI orchestration)
- OpenAI (language model)
- ChromaDB (vector database)
- And other dependencies

### 1.4 Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
cp .env_example .env

# Edit .env and add your OpenAI API key
# Use nano, vim, or any text editor
nano .env
```

**Add your API key:**
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.7
MAX_TOKENS=500
```

> 💡 **Tip:** You can get a free OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)

### 1.5 Initialize Knowledge Base

The knowledge base will be automatically initialized when you start the server. It includes 50+ IT support scenarios covering:
- Networking (Wi-Fi, VPN)
- Password/Account issues
- Software installation
- Audio/Video troubleshooting
- Hardware problems
- And more!

### 1.6 Start Backend Server

```bash
python main.py
```

You should see:
```
✅ IT Helpdesk Chatbot API started successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

🎉 **Backend is ready!** Leave this terminal running.

---

## 🎨 Step 2: Set Up Frontend

Open a **new terminal window** and navigate to the frontend directory.

### 2.1 Navigate to Frontend Directory

```bash
cd frontend
```

### 2.2 Install Dependencies

```bash
npm install
```

This will install:
- React 18
- TypeScript
- Tailwind CSS
- Axios (API client)
- Lucide React (icons)

### 2.3 Set Up Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
# Copy the example file
cp .env.example .env
```

The default configuration should work:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2.4 Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.12  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

🎉 **Frontend is ready!**

---

## 🎊 Step 3: Use the Chatbot

1. **Open your browser** and go to: [http://localhost:5173](http://localhost:5173)

2. **Try asking questions** like:
   - "How do I connect to the company Wi-Fi?"
   - "My Zoom audio isn't working"
   - "I need to reset my password"
   - "The projector isn't detecting my laptop"

3. **Use Quick Actions** for common tasks (displayed on first load)

4. **Create tickets** if the bot suggests escalation

---

## 🧪 Verify Everything Works

### Test the Backend API

Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API documentation.

Try the `/health` endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {
    "api": "healthy",
    "chat_engine": "healthy",
    "knowledge_base": "healthy",
    "vector_store": "healthy"
  }
}
```

### Test the Frontend

The frontend should automatically connect to the backend. You'll see a green "Online" status in the header.

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError` or import errors
- **Solution:** Make sure your virtual environment is activated and dependencies are installed:
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

**Problem:** `OPENAI_API_KEY not set`
- **Solution:** Make sure you created `.env` file with your API key in the `backend` directory

**Problem:** Port 8000 already in use
- **Solution:** Stop other services using port 8000, or change the port in `.env`:
  ```env
  PORT=8001
  ```

**Problem:** `ChromaDB` errors
- **Solution:** Delete the `chroma_db` directory and restart:
  ```bash
  rm -rf chroma_db
  python main.py
  ```

### Frontend Issues

**Problem:** Cannot connect to backend
- **Solution:** Ensure backend is running on `http://localhost:8000`
- Check the `.env` file in frontend directory has correct `VITE_API_BASE_URL`

**Problem:** `npm install` fails
- **Solution:** Delete `node_modules` and `package-lock.json`, then reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

**Problem:** Port 5173 already in use
- **Solution:** The dev server will automatically use the next available port (5174, 5175, etc.)

### API Key Issues

**Problem:** OpenAI API errors
- **Solution:** 
  1. Verify your API key is valid at [platform.openai.com](https://platform.openai.com/api-keys)
  2. Check you have credits/billing set up
  3. Try using a different model (e.g., `gpt-3.5-turbo` instead of `gpt-4o-mini`)

---

## 📦 Alternative: Docker Deployment

If you prefer Docker:

### 1. Create `.env` file in project root

```env
OPENAI_API_KEY=your-api-key-here
```

### 2. Start with Docker Compose

```bash
docker-compose up --build
```

### 3. Access the application

- **Frontend:** [http://localhost:80](http://localhost:80)
- **Backend API:** [http://localhost:8000](http://localhost:8000)

---

## 🎓 Next Steps

Now that your chatbot is running:

1. **Customize the Knowledge Base**
   - Edit `backend/data/it_knowledge.csv` to add your own IT solutions
   - Restart the backend with `force_reload=True` in `knowledge_base.py`

2. **Customize the UI**
   - Modify `frontend/src/components/` to change the look and feel
   - Update colors in `frontend/tailwind.config.js`

3. **Add Features**
   - Integrate with real ticketing systems (ServiceNow, Jira)
   - Add user authentication
   - Implement analytics dashboard
   - Add file upload for screenshots

4. **Deploy to Production**
   - Backend: Deploy to Render, Railway, or AWS Lambda
   - Frontend: Deploy to Vercel, Netlify, or AWS S3
   - Database: Use Pinecone for managed vector storage

---

## 💡 Sample Queries to Try

Here are some example questions you can ask the chatbot:

### Networking
- "How do I connect to the company Wi-Fi?"
- "I need help setting up VPN"
- "My internet is very slow"

### Password & Access
- "How do I reset my password?"
- "My account is locked"
- "I can't access the shared drive"

### Audio/Video
- "My Zoom audio isn't working"
- "The camera is not detected"
- "How do I connect to the projector?"

### Software
- "How do I install Microsoft Teams?"
- "I need to activate Office"
- "How do I request new software?"

### Hardware
- "The printer is not found"
- "My laptop is overheating"
- "My keyboard isn't working"

### General
- "How do I contact IT support?"
- "My computer is running slow"
- "I'm working from home, what should I know?"

---

## 📞 Need Help?

If you run into issues:

1. Check the console logs (backend terminal and browser console)
2. Review the troubleshooting section above
3. Check the API docs at [http://localhost:8000/docs](http://localhost:8000/docs)
4. Review the main README.md for more details

---

**Congratulations! Your IT Helpdesk Chatbot is ready to help users! 🎉**

