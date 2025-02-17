from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List

      
extract_preferences_prompt = PromptTemplate(
    input_variables=["history", "user_message"],
    template="""
        You are an assistant helping recommend cars.
        Based on the conversation history and user input, extract the following details:
        - Budget (e.g., "$20,000")
        - Type of car (e.g., sedan, SUV, electric)
        - Features or preferences (e.g., "good mileage", "electric", "luxury")
        
        History:
        {history}

        User: {user_message}

        Provide the extracted preferences in this format:
        - Budget: [Extracted Budget]
        - Type of car: [Extracted Type]
        - Features: [Extracted Features]
    """,
    validate_template=True,
)

generate_recommendations_prompt = PromptTemplate(
    input_variables=["preferences"],
    template="""
        You are a car recommendation expert.
        Based on the user's preferences: {preferences}, suggest 3 cars with the following details:

        For each car, provide:
        - Car Name
        - Estimated Price
        - Key Features
        - Safety Rating
        - Unique Feature

        Provide the recommendations as a list of cars.
    """,
    validate_template=True,
)


class UserPreferences(BaseModel):
    budget: str = Field(description="The user's budget for the car")
    car_type: str = Field(description="The type of car the user wants")
    features: List[str] = Field(description="List of features or preferences the user wants")


class CarRecommendation(BaseModel):
    name: str = Field(description="The name of the car")
    price: str = Field(description="The estimated price of the car")
    features: List[str] = Field(description="Key features of the car")
    safety_rating: str = Field(description="Safety rating of the car")
    unique_feature: str = Field(description="A unique feature of the car")


class CarRecommendations(BaseModel):
    recommendations: List[CarRecommendation] = Field(description="List of car recommendations")