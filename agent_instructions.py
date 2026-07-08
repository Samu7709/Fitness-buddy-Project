# ============================================================
# ============================================================
#        FITNESS BUDDY AI — AGENT INSTRUCTIONS MODULE
#        IBM Watsonx.ai + Granite Model Integration
# ============================================================
# ============================================================
#
# HOW TO CUSTOMIZE THE AGENT:
#   Edit the constants in the AGENT_INSTRUCTIONS section below.
#   Each section is clearly labeled — no deep Python knowledge needed.
#
# ============================================================

# ============================================================
#  AGENT INSTRUCTIONS — CUSTOMIZE EVERYTHING HERE
# ============================================================

AGENT_NAME = "FitBuddy"

# --------------------------------------------------------------
# 1. PERSONALITY & TONE
#    Options: "friendly", "motivational", "professional", "strict", "fun"
# --------------------------------------------------------------
AGENT_TONE = "friendly and motivational"
AGENT_PERSONALITY = """
You are FitBuddy, a warm, encouraging, and knowledgeable AI fitness coach.
You speak like a supportive friend who happens to be a certified fitness expert.
You celebrate small wins, never shame the user, and always keep things positive.
You use simple language that anyone can understand — no jargon overload.
"""

# --------------------------------------------------------------
# 2. FITNESS SPECIALIZATION
#    What this agent focuses on
# --------------------------------------------------------------
AGENT_FITNESS_FOCUS = """
- Home workouts (no gym equipment required unless specified)
- Bodyweight exercises: push-ups, squats, lunges, planks, yoga
- Cardio: walking, jogging, jumping jacks, skipping
- Flexibility & stretching: yoga-inspired routines
- Beginner to intermediate fitness levels
- Weight management: fat loss and healthy muscle tone
- Postural improvement and back pain relief exercises
"""

# --------------------------------------------------------------
# 3. NUTRITIONAL PREFERENCES — INDIAN LIFESTYLE
#    Customize meal suggestions based on regional preferences
# --------------------------------------------------------------
AGENT_NUTRITION_STYLE = """
- Prioritize traditional Indian foods: dal, sabzi, roti, rice, curd, idli, dosa, poha, upma
- Suggest protein-rich Indian options: paneer, soya chunks, moong dal, chana, rajma, eggs, chicken
- Include low-calorie Indian snacks: roasted chana, makhana, sprouts, fruits
- Respect vegetarian and vegan preferences when mentioned
- Recommend seasonal Indian fruits and vegetables
- Suggest hydration: nimbu pani, coconut water, buttermilk (chaas), green tea
- Avoid overly processed or Western fast foods unless asked
- Respect regional diversity: South Indian, North Indian, Maharashtrian, Bengali etc.
- Consider festival seasons and traditional practices
"""

# --------------------------------------------------------------
# 4. MOTIVATIONAL STYLE
# --------------------------------------------------------------
AGENT_MOTIVATIONAL_STYLE = """
- Use short, punchy motivational quotes (Hindi or English)
- Reference Indian icons when relevant (Milkha Singh, Mary Kom, PV Sindhu, Virat Kohli)
- Celebrate consistency over perfection: "Even 10 minutes counts!"
- Use relatable Indian analogies: "Strong like a banyan tree 🌳"
- Encourage "kal se nahi, aaj se!" (Not from tomorrow, from today!)
- Send daily habit-building nudges
- Acknowledge struggles: busy schedule, Indian family diet, desk jobs, summer heat
"""

# --------------------------------------------------------------
# 5. SAFETY GUIDELINES — VERY IMPORTANT
# --------------------------------------------------------------
AGENT_SAFETY_RULES = """
- Always recommend consulting a doctor before starting a new fitness program
- Never prescribe medical treatments or diagnose diseases
- For injuries, always say "Please see a physiotherapist or doctor"
- BMI is a general indicator — always mention it has limitations
- Do NOT recommend extreme calorie restriction (below 1200 kcal)
- Do NOT recommend supplements without noting "consult a nutritionist first"
- For pregnant women: always advise "consult your OB-GYN first"
- For children under 15: recommend age-appropriate activities only
- Avoid recommending exercises for specific medical conditions without physician approval
"""

# --------------------------------------------------------------
# 6. RESPONSE FORMAT PREFERENCES
# --------------------------------------------------------------
AGENT_RESPONSE_FORMAT = """
- Keep responses concise: 3-5 sentences for simple questions
- Use bullet points for workout plans and meal plans
- For workout plans: include sets, reps, and rest time
- For meal plans: include rough calorie estimates
- Use emojis sparingly but warmly (💪 🥗 🏃 ✅)
- End motivational messages with a short call-to-action
- Always be culturally sensitive and inclusive
"""

# --------------------------------------------------------------
# 7. DAILY TIPS POOL — Add your own tips here!
# --------------------------------------------------------------
DAILY_TIPS = [
    "💧 Start your morning with a glass of warm water with lemon. It kickstarts your metabolism!",
    "🧘 Even 5 minutes of deep breathing can reduce stress hormones significantly.",
    "🚶 Take a 10-minute walk after every meal. It helps digestion and burns extra calories!",
    "💤 Sleep 7-8 hours. Muscles repair and grow during sleep, not just during workouts.",
    "🥗 Fill half your thali with vegetables. Color = nutrients!",
    "⏰ Eat at consistent times. Your body loves routine — just like your fitness schedule.",
    "🏋️ Progressive overload: Add one more rep or 30 more seconds each week to keep improving.",
    "🍌 Have a banana or handful of dry fruits 30 min before workout for natural energy.",
    "📵 No screen time 30 min before bed. Better sleep = better recovery.",
    "🤸 Stretch for 5 minutes after every workout to reduce soreness and improve flexibility.",
    "🥛 Include curd/yogurt daily — probiotics aid digestion and boost immunity.",
    "🌞 Morning sunlight for 15 minutes boosts Vitamin D and improves mood naturally.",
    "💪 You don't need a gym to be fit. Your body weight is your best equipment!",
    "🍵 Swap one chai with green tea today. Small changes, big results over time.",
    "🎯 Set one small fitness goal today. Not monthly — just TODAY. Then crush it!",
]

# --------------------------------------------------------------
# 8. WORKOUT TEMPLATES — Indian Home Workout Plans
# --------------------------------------------------------------
WORKOUT_TEMPLATES = {
    "beginner": {
        "name": "Starter Spark — 20 Min Home Workout",
        "warm_up": [
            "Neck rotations — 30 sec",
            "Shoulder rolls — 30 sec",
            "Arm circles — 30 sec each direction",
            "Hip circles — 30 sec",
            "Marching in place — 1 min",
        ],
        "exercises": [
            {"name": "Wall push-ups", "sets": 3, "reps": "10", "rest": "30 sec"},
            {"name": "Chair squats", "sets": 3, "reps": "12", "rest": "30 sec"},
            {"name": "Standing calf raises", "sets": 3, "reps": "15", "rest": "20 sec"},
            {"name": "Plank hold", "sets": 3, "reps": "20 sec", "rest": "30 sec"},
            {"name": "Lying leg raises", "sets": 3, "reps": "10", "rest": "30 sec"},
        ],
        "cool_down": [
            "Child's pose (Balasana) — 1 min",
            "Seated forward fold — 1 min",
            "Supine twist — 30 sec each side",
        ],
    },
    "intermediate": {
        "name": "Power Builder — 35 Min Home Workout",
        "warm_up": [
            "Jumping jacks — 1 min",
            "High knees — 1 min",
            "Arm swings — 30 sec",
            "Hip flexor stretch — 30 sec each",
        ],
        "exercises": [
            {"name": "Push-ups", "sets": 4, "reps": "15", "rest": "45 sec"},
            {"name": "Jump squats", "sets": 3, "reps": "12", "rest": "45 sec"},
            {"name": "Reverse lunges", "sets": 3, "reps": "10 each leg", "rest": "30 sec"},
            {"name": "Mountain climbers", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
            {"name": "Plank to downward dog", "sets": 3, "reps": "10", "rest": "30 sec"},
            {"name": "Glute bridges", "sets": 3, "reps": "15", "rest": "30 sec"},
            {"name": "Tricep dips (chair)", "sets": 3, "reps": "12", "rest": "30 sec"},
        ],
        "cool_down": [
            "Pigeon pose — 1 min each side",
            "Chest opener stretch — 1 min",
            "Supine spinal twist — 1 min each side",
            "Savasana — 2 min",
        ],
    },
    "weight_loss": {
        "name": "Fat Burner Express — 30 Min HIIT",
        "warm_up": [
            "Brisk walk in place — 2 min",
            "Dynamic leg swings — 30 sec each",
            "Torso twists — 1 min",
        ],
        "exercises": [
            {"name": "Burpees", "sets": 4, "reps": "8", "rest": "20 sec"},
            {"name": "Jumping jacks", "sets": 4, "reps": "30 sec", "rest": "15 sec"},
            {"name": "Skater hops", "sets": 3, "reps": "12 each side", "rest": "20 sec"},
            {"name": "High knees", "sets": 4, "reps": "30 sec", "rest": "15 sec"},
            {"name": "Squat pulses", "sets": 3, "reps": "20", "rest": "20 sec"},
            {"name": "Plank jacks", "sets": 3, "reps": "20 sec", "rest": "20 sec"},
        ],
        "cool_down": [
            "Standing quad stretch — 30 sec each",
            "Hamstring stretch — 1 min each",
            "Seated butterfly stretch — 1 min",
        ],
    },
    "yoga_flexibility": {
        "name": "Yoga Flow — 25 Min Flexibility & Calm",
        "warm_up": [
            "Pranayama breathing — 3 min",
            "Seated neck stretches — 1 min",
        ],
        "exercises": [
            {"name": "Surya Namaskar (Sun Salutation)", "sets": 3, "reps": "full round", "rest": "1 min"},
            {"name": "Warrior I (Virabhadrasana I)", "sets": 1, "reps": "45 sec each side", "rest": "30 sec"},
            {"name": "Warrior II", "sets": 1, "reps": "45 sec each side", "rest": "30 sec"},
            {"name": "Tree pose (Vrikshasana)", "sets": 1, "reps": "45 sec each side", "rest": "20 sec"},
            {"name": "Bridge pose (Setu Bandha)", "sets": 3, "reps": "30 sec", "rest": "30 sec"},
            {"name": "Cat-Cow flow", "sets": 1, "reps": "2 min continuous", "rest": "—"},
        ],
        "cool_down": [
            "Seated forward fold — 2 min",
            "Legs up the wall — 3 min",
            "Savasana — 5 min",
        ],
    },
}

# --------------------------------------------------------------
# 9. INDIAN MEAL PLANS — Healthy & Delicious
# --------------------------------------------------------------
MEAL_PLANS = {
    "weight_loss": {
        "name": "Slim & Strong Meal Plan (Indian)",
        "calories_target": "1400-1600 kcal",
        "meals": {
            "early_morning": "Warm water + lemon + 5 soaked almonds (~30 kcal)",
            "breakfast": "2 moong dal chilla with mint chutney OR 2 idli + sambar (~300 kcal)",
            "mid_morning": "1 seasonal fruit (apple/guava/papaya) OR 1 cup green tea (~80 kcal)",
            "lunch": "2 roti + 1 cup dal + 1 cup sabzi + salad + curd (~500 kcal)",
            "evening_snack": "Roasted chana OR makhana (fox nuts) + 1 cup masala chai (~150 kcal)",
            "dinner": "1 cup vegetable khichdi OR 1-2 roti + sabzi + soup (~400 kcal)",
            "post_dinner": "1 glass warm turmeric milk (haldi doodh) (~100 kcal)",
        },
        "tips": [
            "Avoid deep-fried snacks (samosa, pakoda) — opt for baked/roasted",
            "Use less oil — switch to mustard or coconut oil in small quantities",
            "Eat dinner by 8 PM for better digestion",
            "Drink 8-10 glasses of water daily",
        ],
    },
    "muscle_gain": {
        "name": "Power & Protein Meal Plan (Indian)",
        "calories_target": "2200-2500 kcal",
        "meals": {
            "early_morning": "Warm water + 10 soaked almonds + 5 walnuts (~100 kcal)",
            "breakfast": "4 egg whites OR 1 cup soya milk + 2 multigrain rotis + peanut butter (~550 kcal)",
            "mid_morning": "Paneer (100g) + cucumber salad OR protein-rich smoothie (~250 kcal)",
            "lunch": "3 rotis + 1 cup rajma/chana + 1 cup sabzi + 1 cup curd + salad (~700 kcal)",
            "pre_workout": "Banana + 1 tbsp peanut butter OR 1 cup dry fruits (~200 kcal)",
            "post_workout": "200ml milk + 1 banana OR 2 boiled eggs + 1 roti (~300 kcal)",
            "dinner": "2 rotis + 200g grilled paneer/chicken + sabzi + dal (~600 kcal)",
        },
        "tips": [
            "Eat every 3-4 hours to keep protein synthesis active",
            "Include desi ghee in moderation — it's a quality fat source",
            "Soya chunks are an excellent vegetarian protein source (52g protein/100g)",
            "Sleep 8 hours — muscle grows during rest, not just workouts",
        ],
    },
    "balanced": {
        "name": "Balanced Wellness Meal Plan (Indian)",
        "calories_target": "1800-2000 kcal",
        "meals": {
            "early_morning": "1 glass water + seasonal fruit (~60 kcal)",
            "breakfast": "Poha with vegetables OR upma + 1 cup chai (~350 kcal)",
            "mid_morning": "Sprouts chaat OR 1 cup buttermilk (chaas) (~120 kcal)",
            "lunch": "2-3 rotis + dal + sabzi + rice + curd + salad (~600 kcal)",
            "evening_snack": "1 cup green tea + roasted peanuts OR fruit (~200 kcal)",
            "dinner": "2 rotis + dal + light sabzi + raita (~500 kcal)",
            "post_dinner": "Warm milk with pinch of nutmeg for good sleep (~120 kcal)",
        },
        "tips": [
            "Include at least 3 colors on your plate at every meal",
            "Use whole grains where possible — jowar, bajra, ragi over maida",
            "Cook with turmeric, ginger, garlic — powerful anti-inflammatory spices",
            "Limit sugar — replace with jaggery (gud) in small amounts",
        ],
    },
}

# ============================================================
#  SYSTEM PROMPT BUILDER — Assembles the full agent prompt
# ============================================================

def build_system_prompt():
    """
    Builds the complete system prompt for the IBM Granite model.
    Combines all AGENT_INSTRUCTIONS sections above.
    """
    return f"""You are {AGENT_NAME}, an AI-powered fitness and wellness coach.

PERSONALITY & TONE:
{AGENT_PERSONALITY}

YOUR FITNESS EXPERTISE:
{AGENT_FITNESS_FOCUS}

NUTRITION PHILOSOPHY:
{AGENT_NUTRITION_STYLE}

HOW YOU MOTIVATE:
{AGENT_MOTIVATIONAL_STYLE}

SAFETY — ALWAYS FOLLOW THESE RULES:
{AGENT_SAFETY_RULES}

RESPONSE STYLE:
{AGENT_RESPONSE_FORMAT}

Remember: You are {AGENT_NAME}. Be warm, helpful, and always culturally aware.
Today's motivation: "Consistency beats perfection. Start where you are. Use what you have. Do what you can. 💪"
"""


def get_daily_tip():
    """Returns a random daily tip from the pool."""
    import random
    return random.choice(DAILY_TIPS)


def get_workout_plan(level: str) -> dict:
    """
    Returns a workout plan dict for the given level.
    levels: 'beginner', 'intermediate', 'weight_loss', 'yoga_flexibility'
    """
    return WORKOUT_TEMPLATES.get(level, WORKOUT_TEMPLATES["beginner"])


def get_meal_plan(goal: str) -> dict:
    """
    Returns a meal plan dict for the given goal.
    goals: 'weight_loss', 'muscle_gain', 'balanced'
    """
    return MEAL_PLANS.get(goal, MEAL_PLANS["balanced"])


def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Calculates BMI and returns category, advice, and ideal weight range.
    """
    if height_cm <= 0 or weight_kg <= 0:
        return {"error": "Invalid measurements"}

    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)

    # BMI categories (WHO standards)
    if bmi < 18.5:
        category = "Underweight"
        color = "info"
        advice = "You're below the healthy range. Focus on nutrient-dense foods and strength training to build healthy mass."
        emoji = "📉"
    elif 18.5 <= bmi < 25.0:
        category = "Normal / Healthy Weight"
        color = "success"
        advice = "Excellent! You're in the healthy BMI range. Focus on maintaining this with balanced nutrition and regular exercise."
        emoji = "✅"
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        color = "warning"
        advice = "Slightly above the healthy range. A combination of cardio, strength training, and mindful eating will help."
        emoji = "⚠️"
    else:
        category = "Obese"
        color = "danger"
        advice = "Please consult a doctor before starting any intensive program. Small, consistent lifestyle changes are the safest approach."
        emoji = "🏥"

    # Ideal weight range (using BMI 18.5–24.9)
    ideal_min = round(18.5 * (height_m ** 2), 1)
    ideal_max = round(24.9 * (height_m ** 2), 1)

    return {
        "bmi": bmi,
        "category": category,
        "color": color,
        "advice": advice,
        "emoji": emoji,
        "ideal_min": ideal_min,
        "ideal_max": ideal_max,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
    }


def calculate_calories(weight_kg: float, height_cm: float, age: int,
                        gender: str, activity_level: str, goal: str) -> dict:
    """
    Calculates daily calorie needs using Mifflin-St Jeor equation.
    """
    # Base Metabolic Rate
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    multiplier = activity_multipliers.get(activity_level, 1.375)
    tdee = round(bmr * multiplier)

    # Goal adjustments
    if goal == "weight_loss":
        target = tdee - 300
        goal_label = "Weight Loss (moderate deficit)"
    elif goal == "muscle_gain":
        target = tdee + 300
        goal_label = "Muscle Gain (moderate surplus)"
    else:
        target = tdee
        goal_label = "Maintenance"

    return {
        "bmr": round(bmr),
        "tdee": tdee,
        "target_calories": target,
        "goal": goal_label,
        "protein_g": round(weight_kg * 1.6),  # 1.6g per kg body weight
        "carbs_g": round((target * 0.45) / 4),
        "fat_g": round((target * 0.25) / 9),
    }
