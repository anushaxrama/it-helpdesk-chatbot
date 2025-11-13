# 👋 Welcome to IT Helpdesk Chatbot!

## 🎯 You're 5 Minutes Away from Running This!

This is a **production-ready AI chatbot** for IT support. Here's everything you need to get started.

---

## ⚡ Super Quick Start (Copy & Paste)

### Option 1: Manual Setup (Recommended for Learning)

**Step 1: Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env_example .env
```

Now edit `backend/.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-proj-your-key-here
```

Then start the backend:
```bash
python main.py
```

**Step 2: Frontend** (new terminal)
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

**Step 3: Open Browser**
- Go to http://localhost:5173
- Start chatting!

---

### Option 2: Docker (Fastest)

```bash
# Create .env in project root
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env

# Start everything
docker-compose up --build

# Open http://localhost:80
```

---

## 📚 What to Read Next

### If you're trying to RUN this:
→ Read **SETUP.md** for detailed instructions

### If you're trying to UNDERSTAND this:
→ Read **README.md** for architecture and features

### If you're using this for a PORTFOLIO:
→ Read **PORTFOLIO.md** for resume content and talking points

### If you're trying to MODIFY this:
→ Read **CONTRIBUTING.md** for development guidelines

---

## 🆘 Quick Troubleshooting

**❌ "OPENAI_API_KEY not set"**
→ Create `backend/.env` file with your API key

**❌ "Cannot connect to backend"**
→ Make sure backend is running on http://localhost:8000

**❌ "Port already in use"**
→ Close other apps using port 8000 or 5173

**❌ "Module not found"**
→ Activate venv and run `pip install -r requirements.txt`

**❌ "npm install fails"**
→ Delete `node_modules` and try again

---

## 💡 Try These Queries First

Once it's running, try:
- "How do I connect to Wi-Fi?"
- "My Zoom audio isn't working"
- "I need to reset my password"
- Or click the Quick Action buttons!

---

## 🎓 Project Structure at a Glance

```
backend/          → Python FastAPI + LangChain
  ├── main.py              → API routes
  ├── chat_engine.py       → AI logic
  └── data/it_knowledge.csv → 50+ IT solutions

frontend/         → React + TypeScript + Tailwind
  └── src/
      ├── components/      → UI components
      └── api/chatApi.ts   → API client
```

---

## 🔑 Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up/login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)
5. Add to `backend/.env`

**Cost:** This uses `gpt-4o-mini` which costs ~$0.01 per 100 queries. Very cheap for development!

---

## 📱 Access Points

Once running:
- **Chat UI:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🎥 Demo Video Ideas

Want to record a demo? Show:
1. Asking a Wi-Fi question → Getting detailed steps
2. Clicking a Quick Action button → Instant response
3. Complex question → Escalation banner → Create ticket
4. Backend API docs at /docs

---

## 🚀 Next Steps

1. ✅ Get it running (5 minutes)
2. 📖 Read the docs (15 minutes)
3. 🧪 Try different queries (10 minutes)
4. 🎨 Customize the UI (optional)
5. 📸 Take screenshots for portfolio (5 minutes)
6. 📝 Update your resume (10 minutes)

**Total time investment: 1 hour to fully understand and document!**

---

## 📞 Need Help?

- Check **SETUP.md** for detailed troubleshooting
- Open a GitHub issue
- Review the console logs (backend terminal + browser console)

---

**🎉 You've got this! This project showcases real-world AI + full-stack skills.**

**Start with the Quick Start above, and you'll be chatting with AI in 5 minutes!**

