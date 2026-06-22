from flask import Flask, render_template, request
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
    Create a {days}-day travel itinerary.

    Destination: {destination}
    Budget: {budget}
    Travel Style: {style}
    Interests: {interests}

    Include:
    - Day-wise itinerary
    - Places to visit
    - Food recommendations
    - Estimated costs
    - Packing checklist
    - Travel tips
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

    return f"<pre>{itinerary}</pre>"

if __name__ == "__main__":
    app.run(debug=False)