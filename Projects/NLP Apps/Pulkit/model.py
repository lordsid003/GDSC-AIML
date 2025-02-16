from langchain_groq import ChatGroq
from config import (
    extract_preferences_prompt,
    generate_recommendations_prompt,
    UserPreferences,
    CarRecommendations,
)
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="key.env")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("API Key is missing!")
else:
    print("API Key is loaded!")


class CarChatbot:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.8,
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
        )
        self.history = []

    def chat(self, user_message: str):
        self.history.append(f"User: {user_message}")
        history_text = "\n".join(self.history)


        extract_chain = extract_preferences_prompt | self.llm.with_structured_output(UserPreferences)
        try:
            preferences = extract_chain.invoke({"history": history_text, "user_message": user_message})
            self.history.append(f"Assistant (Preferences): {preferences.dict()}")


            generate_chain = generate_recommendations_prompt | self.llm.with_structured_output(CarRecommendations)
            recommendations = generate_chain.invoke({"preferences": preferences.dict()})


            formatted_recommendations = []
            for rec in recommendations.recommendations:
                formatted_recommendations.append(
                    f"🚗 {rec.name} - {rec.price}\n"
                    f"Key Features: {', '.join(rec.features)}\n"
                    f"Safety Rating: {rec.safety_rating}\n"
                    f"Unique Feature: {rec.unique_feature}\n"
                )
            return "\n\n".join(formatted_recommendations)

        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    chatbot = CarChatbot()
    print("CarChatbot is ready!")