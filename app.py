from flask import Flask, render_template, request
import openai
api_key = "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"
openai.api_key = api_key
app = Flask(__name__)



# Define the questions for each section
questions = {
    "personality": [
        "What are your strengths and weaknesses?",
        "Describe your communication style.",
        "How do you handle stress?",
        "What motivates you?",
        "How do you handle teamwork?",
    ],
    "skills": [
        "What are your top skills or talents?",
        "What abilities do you possess that make you unique?",
        "What technical skills do you have?",
        "What soft skills do you have?",
        "What accomplishments are you proud of?",
    ],
    "interests": [
        "What subjects or topics are you passionate about?",
        "What subjects do you excel in?",
        "What subjects do you find challenging?",
        "What recent subjects or areas have you explored?",
        "What subjects are you curious about?",
    ],
}
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve user responses from the form
        user_data = {
            "personality": [],
            "skills": [],
            "interests": [],
        }

        for section in user_data.keys():
            for question in questions[section]:
                user_response = request.form.get(f"{section}_{question}")
                user_data[section].append(user_response)

        # Analyze user data and provide career guidance using GPT-3
        user_profile = " ".join(user_data["personality"] + user_data["skills"] + user_data["interests"])
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"I am a career counselor. Based on your input, I recommend you consider the following career options: {user_profile} career options.",
            max_tokens=150,
            n=1,
        )

        career_recommendations = response.choices[0].text

        return render_template("result.html", career_recommendations=career_recommendations)

    return render_template("index.html", questions=questions)