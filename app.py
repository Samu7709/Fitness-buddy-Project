"""
============================================================
  FITNESS BUDDY AI — Main Flask Application
  Powered by IBM Watsonx.ai + Granite Models
============================================================
  Author  : Fitness Buddy Team
  Version : 1.0.0

  How to run:
    1. Copy env.example → .env and fill in your IBM keys
    2. pip install -r requirements.txt
    3. python app.py
============================================================
"""

import os
import json
import datetime
from flask import (Flask, render_template, request, jsonify,
                   session, redirect, url_for)
from flask_cors import CORS
from dotenv import load_dotenv

# ── Import our agent instructions & fitness logic ─────────────────────────────
from agent_instructions import (
    build_system_prompt,
    get_daily_tip,
    get_workout_plan,
    get_meal_plan,
    calculate_bmi,
    calculate_calories,
    AGENT_NAME,
)

# ── Load environment variables ────────────────────────────────────────────────
# Tries .env first (production), then falls back to env.example (development)
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("env.example"):
    load_dotenv("env.example")
    print("[WARNING] .env not found - loaded credentials from env.example instead.")
    print("          Rename env.example to .env for best practice in production.\n")

# ── IBM Watsonx.ai client (lazy-initialised) ──────────────────────────────────
watsonx_client = None


# (client-level init not needed — ModelInference handles auth per-call)


def ask_granite(user_message: str, conversation_history: list = None) -> str:
    """
    Sends a message to IBM Granite model using the Chat API and returns the response.

    Uses /ml/v1/text/chat (messages format) which is the current recommended API.

    Args:
        user_message         : The user's latest message
        conversation_history : List of previous {role, content} dicts

    Returns:
        AI response string
    """
    if conversation_history is None:
        conversation_history = []

    api_key    = os.getenv("IBM_API_KEY", "").strip()
    project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
    wx_url     = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com").strip()
    model_id   = os.getenv("GRANITE_MODEL_ID", "ibm/granite-4-h-small").strip()

    # ── Guard: fall back to mock if credentials are missing ───────────────────
    if not api_key or not project_id:
        print("[WARNING] IBM credentials not set - using mock responses.")
        print(f"    IBM_API_KEY present : {bool(api_key)}")
        print(f"    WATSONX_PROJECT_ID  : {bool(project_id)}")
        return _mock_response(user_message)

    # ── Build messages list for the Chat API ──────────────────────────────────
    messages = [{"role": "system", "content": build_system_prompt()}]

    # Append previous conversation turns (last 6 for context window)
    for msg in conversation_history[-6:]:
        if msg.get("role") in ("user", "assistant"):
            messages.append({"role": msg["role"], "content": msg["content"]})

    # Append current user message
    messages.append({"role": "user", "content": user_message})

    # ── Call IBM Granite Chat API ──────────────────────────────────────────────
    try:
        from ibm_watsonx_ai.foundation_models import ModelInference
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

        model = ModelInference(
            model_id=model_id,
            credentials={"url": wx_url, "apikey": api_key},
            project_id=project_id,
        )

        print(f"[Granite] chat() -> model: {model_id}, messages: {len(messages)}")

        result = model.chat(
            messages=messages,
            params={
                GenParams.MAX_NEW_TOKENS: 512,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 0.9,
            },
        )

        # Parse the chat response — result is a dict with choices[0].message.content
        if isinstance(result, dict):
            content = (
                result.get("choices", [{}])[0]
                      .get("message", {})
                      .get("content", "")
            )
            if content.strip():
                print(f"[Granite] Response OK ({len(content)} chars)")
                return content.strip()

        print(f"[Granite] Unexpected response shape: {result!r}")
        return _mock_response(user_message)

    except Exception as e:
        print(f"[ERROR] Granite API error: {type(e).__name__}: {e}")
        return _mock_response(user_message)


def _mock_response(message: str) -> str:
    """
    Fallback responses when Watsonx.ai is unavailable.
    Used for development/demo without IBM keys.
    """
    message_lower = message.lower()
    if any(w in message_lower for w in ["bmi", "weight", "height"]):
        return ("Great question! 💪 BMI (Body Mass Index) is calculated as weight(kg) ÷ height(m)². "
                "Use our **BMI Calculator** tab for a detailed analysis with personalised advice!")
    elif any(w in message_lower for w in ["workout", "exercise", "train"]):
        return ("Awesome that you want to work out! 🏋️ I recommend starting with our **Workout Planner** "
                "where I've built personalised home workout plans for beginners, intermediate, weight loss, "
                "and yoga. No gym needed — just your body and 20-35 minutes! 🔥")
    elif any(w in message_lower for w in ["eat", "diet", "food", "meal", "nutrition"]):
        return ("Nutrition is 70% of the fitness journey! 🥗 Check our **Meal Plans** section for "
                "Indian-specific healthy meal plans tailored to your goals. Dal, sabzi, curd — desi "
                "food is incredibly nutritious when balanced right!")
    elif any(w in message_lower for w in ["motivat", "inspire", "tired", "lazy"]):
        return ("Remember: 'Kal se nahi, aaj se!' 💫 Every small step counts. You don't need to be "
                "perfect — you just need to be consistent. Even a 10-minute walk today is better than "
                "the 'perfect workout' you keep postponing. You've got this! 🌟")
    elif any(w in message_lower for w in ["hello", "hi", "hey", "namaste"]):
        return (f"Namaste! 🙏 I'm {AGENT_NAME}, your personal AI fitness coach! "
                "I can help you with workout plans, healthy Indian meal suggestions, BMI calculation, "
                "daily motivation, and much more. What would you like to work on today? 💪")
    else:
        return (f"That's a great topic! 😊 As your AI fitness coach, I'm here to help with workouts, "
                "nutrition, BMI, habits, and motivation. Could you tell me a bit more about your "
                "fitness goal? (e.g., weight loss, muscle gain, flexibility, or general wellness?)")


# ── Flask App Setup ────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fitness-buddy-dev-key")
CORS(app)

# ── Default user profile stored in session ────────────────────────────────────
DEFAULT_PROFILE = {
    "name": "Fitness Enthusiast",
    "age": 25,
    "gender": "male",
    "weight": 70.0,
    "height": 170.0,
    "goal": "balanced",
    "activity_level": "moderate",
    "fitness_level": "beginner",
    "diet_preference": "vegetarian",
}

# ── Default habit tracker data ────────────────────────────────────────────────
DEFAULT_HABITS = {
    "water_glasses": 0,
    "workout_done": False,
    "fruits_eaten": False,
    "sleep_hours": 0,
    "steps_walked": 0,
    "last_updated": str(datetime.date.today()),
    "streak": 0,
}


# ==============================================================================
#  ROUTES
# ==============================================================================

@app.route("/")
def index():
    """Landing / home page."""
    tip = get_daily_tip()
    profile = session.get("profile", DEFAULT_PROFILE)
    return render_template("index.html",
                           agent_name=AGENT_NAME,
                           daily_tip=tip,
                           profile=profile)


@app.route("/dashboard")
def dashboard():
    """Main dashboard — overview of all features."""
    profile = session.get("profile", DEFAULT_PROFILE)
    habits = _get_habits()
    tip = get_daily_tip()

    # Quick BMI for dashboard widget
    bmi_data = calculate_bmi(profile["weight"], profile["height"])

    return render_template("dashboard.html",
                           agent_name=AGENT_NAME,
                           profile=profile,
                           habits=habits,
                           bmi_data=bmi_data,
                           daily_tip=tip)


@app.route("/chat")
def chat():
    """Chatbot page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    return render_template("chat.html",
                           agent_name=AGENT_NAME,
                           profile=profile)


@app.route("/bmi")
def bmi_page():
    """BMI calculator page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    return render_template("bmi.html",
                           agent_name=AGENT_NAME,
                           profile=profile)


@app.route("/workout")
def workout_page():
    """Workout planner page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    level = profile.get("fitness_level", "beginner")
    plan = get_workout_plan(level)
    return render_template("workout.html",
                           agent_name=AGENT_NAME,
                           profile=profile,
                           plan=plan,
                           all_plans={
                               "beginner": get_workout_plan("beginner"),
                               "intermediate": get_workout_plan("intermediate"),
                               "weight_loss": get_workout_plan("weight_loss"),
                               "yoga_flexibility": get_workout_plan("yoga_flexibility"),
                           })


@app.route("/meals")
def meals_page():
    """Healthy meal suggestions page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    goal = profile.get("goal", "balanced")
    meal_plan = get_meal_plan(goal)
    calorie_data = calculate_calories(
        profile["weight"], profile["height"], profile["age"],
        profile["gender"], profile["activity_level"], goal
    )
    return render_template("meals.html",
                           agent_name=AGENT_NAME,
                           profile=profile,
                           meal_plan=meal_plan,
                           calorie_data=calorie_data,
                           all_plans={
                               "weight_loss": get_meal_plan("weight_loss"),
                               "muscle_gain": get_meal_plan("muscle_gain"),
                               "balanced": get_meal_plan("balanced"),
                           })


@app.route("/habits")
def habits_page():
    """Habit tracker page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    habits = _get_habits()
    tip = get_daily_tip()
    return render_template("habits.html",
                           agent_name=AGENT_NAME,
                           profile=profile,
                           habits=habits,
                           daily_tip=tip)


@app.route("/profile")
def profile_page():
    """User profile management page."""
    profile = session.get("profile", DEFAULT_PROFILE)
    return render_template("profile.html",
                           agent_name=AGENT_NAME,
                           profile=profile)


# ==============================================================================
#  API ENDPOINTS (JSON)
# ==============================================================================

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    POST /api/chat
    Body: { "message": "...", "history": [...] }
    Returns: { "response": "..." }
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    response = ask_granite(user_message, history)
    return jsonify({
        "response": response,
        "agent": AGENT_NAME,
        "timestamp": datetime.datetime.now().strftime("%H:%M"),
    })


@app.route("/api/bmi", methods=["POST"])
def api_bmi():
    """
    POST /api/bmi
    Body: { "weight": 70, "height": 170 }
    Returns: BMI calculation result
    """
    data = request.get_json()
    try:
        weight = float(data.get("weight", 0))
        height = float(data.get("height", 0))
        result = calculate_bmi(weight, height)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calories", methods=["POST"])
def api_calories():
    """
    POST /api/calories
    Body: { weight, height, age, gender, activity_level, goal }
    """
    data = request.get_json()
    try:
        result = calculate_calories(
            float(data["weight"]),
            float(data["height"]),
            int(data["age"]),
            data["gender"],
            data["activity_level"],
            data["goal"],
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/workout", methods=["GET"])
def api_workout():
    """GET /api/workout?level=beginner"""
    level = request.args.get("level", "beginner")
    plan = get_workout_plan(level)
    return jsonify(plan)


@app.route("/api/meal", methods=["GET"])
def api_meal():
    """GET /api/meal?goal=weight_loss"""
    goal = request.args.get("goal", "balanced")
    plan = get_meal_plan(goal)
    return jsonify(plan)


@app.route("/api/profile", methods=["POST"])
def api_save_profile():
    """POST /api/profile — save user profile to session."""
    data = request.get_json()
    profile = session.get("profile", DEFAULT_PROFILE.copy())
    profile.update({k: v for k, v in data.items() if k in DEFAULT_PROFILE})
    session["profile"] = profile
    return jsonify({"success": True, "profile": profile})


@app.route("/api/habits", methods=["POST"])
def api_update_habits():
    """POST /api/habits — update habit tracker."""
    data = request.get_json()
    habits = _get_habits()
    habits.update({k: v for k, v in data.items() if k in DEFAULT_HABITS})
    habits["last_updated"] = str(datetime.date.today())

    # Update streak: if all key habits done, increment
    if (habits["water_glasses"] >= 8 and habits["workout_done"]
            and habits["fruits_eaten"] and habits["sleep_hours"] >= 7):
        habits["streak"] = habits.get("streak", 0) + 1

    session["habits"] = habits
    return jsonify({"success": True, "habits": habits})


@app.route("/api/tip", methods=["GET"])
def api_tip():
    """GET /api/tip — returns a random daily tip."""
    return jsonify({"tip": get_daily_tip()})


# ==============================================================================
#  HELPERS
# ==============================================================================

def _get_habits():
    """Returns today's habits from session, resetting if it's a new day."""
    habits = session.get("habits", DEFAULT_HABITS.copy())
    today = str(datetime.date.today())
    if habits.get("last_updated") != today:
        # New day — reset daily habits but keep streak
        old_streak = habits.get("streak", 0)
        habits = DEFAULT_HABITS.copy()
        habits["streak"] = old_streak
        habits["last_updated"] = today
        session["habits"] = habits
    return habits


# ==============================================================================
#  RUN
# ==============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    print(f"\n[FITNESS BUDDY AI] Running on http://localhost:{port}")
    print(f"[Agent] {AGENT_NAME} (IBM Granite)")
    print(f"[Debug] {debug}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
