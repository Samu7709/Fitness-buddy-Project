"""
Full project health check — run with: python healthcheck.py
"""
import os, json, sys, warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
if os.path.exists(".env"):
    load_dotenv(".env")
else:
    load_dotenv("env.example")

import app as flask_app

PASS = "PASS"
FAIL = "FAIL"

results = []

def check(label, ok, detail=""):
    status = PASS if ok else FAIL
    results.append(ok)
    icon = "✅" if ok else "❌"
    print(f"  {icon} {label:40s} {status}  {detail}")

print()
print("=" * 60)
print("  FITNESS BUDDY AI — Full Project Health Check")
print("=" * 60)

with flask_app.app.test_client() as c:

    # ── Page Routes ────────────────────────────────────────────
    print("\n📄 PAGE ROUTES")
    pages = [
        ("/",          "Home"),
        ("/dashboard", "Dashboard"),
        ("/chat",      "AI Chat"),
        ("/bmi",       "BMI Calculator"),
        ("/workout",   "Workout Planner"),
        ("/meals",     "Meal Plans"),
        ("/habits",    "Habit Tracker"),
        ("/profile",   "Profile"),
    ]
    for url, name in pages:
        r = c.get(url)
        check(f"GET {url} ({name})", r.status_code == 200, f"HTTP {r.status_code}")

    # ── BMI API ────────────────────────────────────────────────
    print("\n🔢 BMI & CALORIE API")
    r = c.post("/api/bmi",
               data=json.dumps({"weight": 70, "height": 170}),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/bmi — normal weight", d.get("bmi") == 24.2, f"BMI={d.get('bmi')} | {d.get('category')}")

    r = c.post("/api/bmi",
               data=json.dumps({"weight": 45, "height": 165}),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/bmi — underweight", d.get("category") == "Underweight", f"BMI={d.get('bmi')} | {d.get('category')}")

    r = c.post("/api/bmi",
               data=json.dumps({"weight": 95, "height": 170}),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/bmi — overweight", "Overweight" in str(d.get("category","")) or "Obese" in str(d.get("category","")),
          f"BMI={d.get('bmi')} | {d.get('category')}")

    r = c.post("/api/calories",
               data=json.dumps({"weight": 70, "height": 170, "age": 25,
                                "gender": "male", "activity_level": "moderate",
                                "goal": "weight_loss"}),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/calories", "target_calories" in d and "protein_g" in d,
          f"target={d.get('target_calories')} kcal | protein={d.get('protein_g')}g")

    # ── Workout API ────────────────────────────────────────────
    print("\n🏋️  WORKOUT API")
    for level in ["beginner", "intermediate", "weight_loss", "yoga_flexibility"]:
        r = c.get(f"/api/workout?level={level}")
        d = json.loads(r.data)
        ok = "exercises" in d and "warm_up" in d and "cool_down" in d
        check(f"GET /api/workout?level={level}", ok,
              f"exercises={len(d.get('exercises', []))}")

    # ── Meal API ───────────────────────────────────────────────
    print("\n🥗 MEAL PLAN API")
    for goal in ["weight_loss", "muscle_gain", "balanced"]:
        r = c.get(f"/api/meal?goal={goal}")
        d = json.loads(r.data)
        ok = "meals" in d and "tips" in d and "calories_target" in d
        check(f"GET /api/meal?goal={goal}", ok,
              f"meals={len(d.get('meals', {}))} | {d.get('calories_target','')}")

    # ── Profile API ────────────────────────────────────────────
    print("\n👤 PROFILE & HABITS API")
    profile_data = {
        "name": "Test User", "age": 28, "gender": "female",
        "weight": 65.0, "height": 163.0, "goal": "weight_loss",
        "activity_level": "light", "fitness_level": "beginner",
        "diet_preference": "vegetarian",
    }
    r = c.post("/api/profile",
               data=json.dumps(profile_data),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/profile — save profile", d.get("success") is True)

    r = c.post("/api/habits",
               data=json.dumps({"water_glasses": 6, "workout_done": True,
                                "fruits_eaten": True, "sleep_hours": 7.5,
                                "steps_walked": 7000}),
               content_type="application/json")
    d = json.loads(r.data)
    check("POST /api/habits — update habits", d.get("success") is True,
          f"streak={d.get('habits',{}).get('streak',0)}")

    r = c.get("/api/tip")
    d = json.loads(r.data)
    check("GET /api/tip — daily tip", "tip" in d and len(d["tip"]) > 10,
          d.get("tip","")[:50] + "...")

    # ── AI Chat (IBM Granite) ──────────────────────────────────
    print("\n🤖 IBM GRANITE AI CHAT")
    test_msgs = [
        ("Hello! What can you help me with?",     "greeting"),
        ("Give me a beginner home workout",        "workout"),
        ("Suggest a healthy Indian breakfast",     "meal"),
        ("My BMI is 27, what should I do?",       "bmi advice"),
        ("I feel lazy, motivate me!",              "motivation"),
    ]
    for msg, tag in test_msgs:
        r = c.post("/api/chat",
                   data=json.dumps({"message": msg, "history": []}),
                   content_type="application/json")
        d = json.loads(r.data)
        reply = d.get("response", "")
        ok = len(reply) > 30
        check(f"Chat: {tag}", ok, f"{len(reply)} chars — \"{reply[:55]}...\"")

# ── Summary ───────────────────────────────────────────────────
total = len(results)
passed = sum(results)
failed = total - passed

print()
print("=" * 60)
if failed == 0:
    print(f"  ✅ ALL {total}/{total} CHECKS PASSED — Project is complete & working!")
else:
    print(f"  ⚠️  {passed}/{total} passed | {failed} FAILED — see above")
print("=" * 60)
print()
