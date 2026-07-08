# 🏋️ Fitness Buddy AI
### AI-Powered Fitness Coach — IBM Watsonx.ai + Granite Models

---

## 📋 Overview

**Fitness Buddy AI** is a full-stack web application built with **Python Flask** and **IBM Watsonx.ai (Granite models)**. It serves as a personalised AI fitness coach with a beautiful, responsive frontend.

### ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **AI Chat** | Conversational fitness coach powered by IBM Granite |
| 📊 **BMI Calculator** | Instant BMI with ideal weight range + calorie needs |
| 🏋️ **Workout Planner** | 4 home workout plans with rest timer & progress tracker |
| 🥗 **Indian Meal Plans** | 3 desi meal plans tailored to your fitness goal |
| ✅ **Habit Tracker** | Daily water, sleep, workout, steps tracking with streaks |
| 👤 **Profile Manager** | Personalise everything — goal, diet, fitness level |
| 🌙 **Dark Mode** | Full dark/light mode toggle |
| 📱 **Responsive** | Works beautifully on mobile, tablet, and desktop |

---

## 🗂️ Project Structure

```
fitness-buddy/
│
├── app.py                  # Main Flask app + all routes + API endpoints
├── agent_instructions.py   # 🔧 CUSTOMISE THE AI AGENT HERE
├── requirements.txt        # Python dependencies
├── env.example             # Copy to .env and fill in your keys
│
├── templates/
│   ├── base.html           # Base layout (navbar, footer, dark mode)
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Main dashboard
│   ├── chat.html           # AI chatbot interface
│   ├── bmi.html            # BMI + calorie calculator
│   ├── workout.html        # Workout planner with timer
│   ├── meals.html          # Indian meal plans
│   ├── habits.html         # Daily habit tracker
│   └── profile.html        # User profile management
│
├── static/
│   ├── css/
│   │   └── style.css       # All styles + dark mode + animations
│   └── js/
│       ├── main.js         # Dark mode, utils, toast notifications
│       └── chatbot.js      # Chat UI logic, message formatting
│
└── README.md
```

---

## 🚀 Quick Start

### Step 1 — Clone / Download
```bash
# If using git:
git clone <your-repo-url>
cd fitness-buddy

# Or just extract the ZIP and open the folder
```

### Step 2 — Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set Up Environment Variables
```bash
# Copy the example file
copy env.example .env       # Windows
cp env.example .env         # macOS/Linux

# Edit .env with your favourite editor:
notepad .env                # Windows
nano .env                   # macOS/Linux
```

Fill in your IBM credentials:
```env
IBM_API_KEY=your_ibm_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-3-8b-instruct
FLASK_SECRET_KEY=change-this-to-a-random-secret
```

### Step 5 — Run the App
```bash
python app.py
```

Open your browser: **http://localhost:5000** 🎉

---

## 🔑 Getting IBM Watsonx.ai Credentials

### 1. IBM API Key
1. Log in to [IBM Cloud](https://cloud.ibm.com)
2. Go to **Manage → Access (IAM) → API keys**
3. Click **Create an IBM Cloud API key**
4. Copy the key and paste it into `.env` as `IBM_API_KEY`

### 2. Watsonx.ai Project ID
1. Go to [IBM Watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Click **Projects** → Open or create a project
3. Go to project **Settings** tab
4. Copy the **Project ID** → paste into `.env` as `WATSONX_PROJECT_ID`

### 3. Watsonx.ai Service
- Make sure you have a **Watson Machine Learning** service instance provisioned and associated with your project

> 💡 **No IBM account yet?** The app works in **demo mode** with built-in mock responses, so you can explore all features without API keys.

---

## 🔧 Customising the AI Agent

All AI behaviour is controlled in **`agent_instructions.py`**. No deep Python knowledge needed!

```python
# Change the agent's name
AGENT_NAME = "FitBuddy"

# Change tone: "friendly", "motivational", "strict", "professional"
AGENT_TONE = "friendly and motivational"

# Add your own daily tips
DAILY_TIPS = [
    "Your custom tip here! 💪",
    ...
]

# Customise nutrition preferences
AGENT_NUTRITION_STYLE = """
- Your dietary guidelines here
"""

# Modify safety rules
AGENT_SAFETY_RULES = """
- Your safety guidelines here
"""
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Chat with IBM Granite AI |
| POST | `/api/bmi` | Calculate BMI |
| POST | `/api/calories` | Calculate daily calorie needs |
| GET | `/api/workout?level=beginner` | Get workout plan |
| GET | `/api/meal?goal=weight_loss` | Get meal plan |
| POST | `/api/profile` | Save user profile |
| POST | `/api/habits` | Update habit tracker |
| GET | `/api/tip` | Get random daily tip |

### Example Chat Request
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Give me a beginner workout plan", "history": []}'
```

---

## ☁️ Deployment

### Option 1 — IBM Cloud Code Engine (Recommended)
```bash
# 1. Install IBM Cloud CLI
# 2. Login and target your resource group
ibmcloud login
ibmcloud target -g Default

# 3. Deploy as container
ibmcloud ce application create \
  --name fitness-buddy \
  --image your-image:latest \
  --env-from-secret fitness-buddy-secrets \
  --port 5000
```

### Option 2 — Heroku
```bash
# Create Procfile (already configured for gunicorn)
echo "web: gunicorn app:app" > Procfile

heroku create your-fitness-buddy
heroku config:set IBM_API_KEY=xxx WATSONX_PROJECT_ID=xxx
git push heroku main
```

### Option 3 — Railway / Render / Fly.io
All three support Python Flask directly. Set your environment variables in the dashboard and deploy.

### Option 4 — Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```
```bash
docker build -t fitness-buddy .
docker run -p 5000:5000 --env-file .env fitness-buddy
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.0 |
| AI Model | IBM Watsonx.ai — Granite 3 8B Instruct |
| Auth | IBM Cloud IAM API Key |
| Frontend | HTML5, Bootstrap 5.3, Vanilla JS |
| Styling | Custom CSS (dark mode, animations) |
| Icons | Bootstrap Icons |
| Fonts | Inter + Poppins (Google Fonts) |
| Deployment | Gunicorn (production WSGI) |

---

## 🔒 Security Notes

- ✅ API keys stored in `.env` — never commit `.env` to version control
- ✅ `.env` added to `.gitignore` automatically
- ✅ Flask secret key should be changed in production
- ✅ CORS enabled for API flexibility
- ✅ No user data stored permanently (session-based)

---

## 📝 Customisation Guide

### Change the Granite Model
In `.env`:
```env
# Faster, lighter:
GRANITE_MODEL_ID=ibm/granite-3-2b-instruct

# More capable:
GRANITE_MODEL_ID=ibm/granite-3-8b-instruct
```

### Add a New Workout Plan
In `agent_instructions.py`, add to `WORKOUT_TEMPLATES`:
```python
"my_custom_plan": {
    "name": "My Custom Workout",
    "warm_up": ["Jumping jacks — 1 min"],
    "exercises": [
        {"name": "Push-ups", "sets": 3, "reps": "10", "rest": "30 sec"},
    ],
    "cool_down": ["Stretch — 2 min"],
}
```

### Add a New Meal Plan
In `agent_instructions.py`, add to `MEAL_PLANS`:
```python
"keto": {
    "name": "Indian Keto Plan",
    "calories_target": "1600-1800 kcal",
    "meals": { "breakfast": "Paneer bhurji + bulletproof chai" },
    "tips": ["Keep carbs under 50g/day"]
}
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `IBM API key invalid` | Double-check key in `.env`; make sure it's active in IAM |
| `Project not found` | Verify `WATSONX_PROJECT_ID` — copy from project Settings page |
| `Module not found` | Run `pip install -r requirements.txt` again |
| `Port in use` | Change port: `PORT=5001 python app.py` |
| AI returns mock responses | Normal — means Watsonx.ai is not connected; check your `.env` |
| Templates not found | Make sure you run `python app.py` from the project root folder |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- **IBM Watsonx.ai** — Granite foundation models
- **Bootstrap** — UI framework
- **Bootstrap Icons** — Icon library
- **Google Fonts** — Inter & Poppins typography

---

> 💪 *"Kal se nahi — aaj se! Start your fitness journey today."*
>
> Built with ❤️ using IBM Watsonx.ai + Granite
