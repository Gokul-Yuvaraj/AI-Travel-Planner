from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/plan", methods=["POST"])
def plan():

    destination = request.form["destination"]
    days = request.form["days"]
    budget = request.form["budget"]
    style = request.form["style"]
    interests = request.form["interests"]

    prompt = f"""
    Create a beautiful and well-structured {days}-day travel itinerary.

    Destination: {destination}
    Budget: {budget}
    Travel Style: {style}
    Interests: {interests}

    Format the response in HTML.

    Use these sections:

    <h2>🌍 Destination Overview</h2>

    <h2>📅 Day 1</h2>

    <h2>🍜 Food Recommendations</h2>

    <h2>💰 Estimated Budget Breakdown</h2>

    <h2>🎒 Packing Checklist</h2>

    <h2>💡 Travel Tips</h2>

    Return ONLY HTML.
    Use paragraphs and unordered lists.
    Do NOT use markdown.
    Do NOT use **.
    Do NOT use ```html.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    itinerary = response.choices[0].message.content

    return jsonify({
        "itinerary": itinerary
    })
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )