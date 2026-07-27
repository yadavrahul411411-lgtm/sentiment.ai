from flask import Flask, render_template, request
from textblob import TextBlob

# Create Flask app
app = Flask(__name__)


# Recommendations based on mood
RECOMMENDATIONS = {
    "happy": {
        "label": "Happy / Motivated 😄",
        "tips": [
            "Great energy! Use it to tackle a challenging new topic.",
            "Try a hands-on project or coding exercise.",
            "Watch an advanced-level tutorial video."
        ],
        "resources": [
            "Advanced Python: Decorators & Generators",
            "Build a mini project (to-do app, calculator, etc.)",
            "Explore a new topic you've been curious about"
        ]
    },

    "calm": {
        "label": "Neutral / Calm 🙂",
        "tips": [
            "Good state for steady, focused learning.",
            "Review notes and reinforce fundamentals.",
            "Do a mix of theory and light practice."
        ],
        "resources": [
            "Revise previous week's topics",
            "Read a well-structured article or blog post",
            "Solve a few practice problems"
        ]
    },

    "sad": {
        "label": "Sad / Low 😔",
        "tips": [
            "Be kind to yourself — keep it light today.",
            "Short, low-pressure sessions work best.",
            "Revisit topics you already know well for confidence."
        ],
        "resources": [
            "Watch a short, easy explainer video (10-15 min)",
            "Review flashcards or summaries",
            "Take a 5-minute break between short study bursts"
        ]
    },

    "stressed": {
        "label": "Stressed / Anxious 😰",
        "tips": [
            "Avoid cramming hard topics right now.",
            "Break tasks into very small steps.",
            "Consider a short relaxation break before studying."
        ],
        "resources": [
            "5-minute breathing/relaxation break",
            "Simple recap of one small concept",
            "Organize/plan tasks instead of deep studying"
        ]
    }
}


# Stress-related keywords
stress_words = [
    "stressed",
    "anxious",
    "overwhelmed",
    "nervous",
    "tense",
    "worried"
]


# Sad-related keywords
sad_words = [
    "sad",
    "down",
    "unhappy",
    "depressed",
    "gloomy",
    "miserable"
]


# Function to analyze user's mood
def analyze_mood(text):

    # Convert text to lowercase
    text_lower = text.lower()

    # Analyze text using TextBlob
    blob = TextBlob(text)

    # Get sentiment scores
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Check for stress keywords
    if any(word in text_lower for word in stress_words):
        mood = "stressed"

    # Check for sad keywords
    elif any(word in text_lower for word in sad_words):
        mood = "sad"

    # Check for positive sentiment
    elif polarity > 0.2:
        mood = "happy"

    # Check for negative sentiment
    elif polarity < -0.2:
        mood = "sad"

    # Otherwise, calm
    else:
        mood = "calm"

    return mood, round(polarity, 2), round(subjectivity, 2)


# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        # Get user input
        user_text = request.form.get("mood", "").strip()

        # Analyze if input is not empty
        if user_text:

            mood_key, polarity, subjectivity = analyze_mood(user_text)

            # Create result
            result = {
                "input_text": user_text,
                "mood_key": mood_key,
                "polarity": polarity,
                "subjectivity": subjectivity,
                **RECOMMENDATIONS[mood_key]
            }

    return render_template("index.html", result=result)


# Start Flask application
if __name__ == "__main__":
    app.run(debug=True)