import google.generativeai as genai
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
def gemini_updates(news_text):
    prompt_template = PromptTemplate.from_template(
        #   "news_txtrize the following text \n{text} the news_txtry should contain atleast 50 words\n\nnews_txtry:"
        #   "Assume you are an expert in Analysing text, use the following text {text} and give some intresting updates and insights in the form of news headlines from the text"
        "Take the following news updates and generate a headline and a single-line description for each update:\n\n"
                "News Updates:\n{text}\n\n"
                "Formatted Updates:\n"
                " Headline: [Headline 1]\n"
                " Description: [Description 1]\n"
                " More details:[url1]\n\n"
                " Headline: [Headline 2]\n"
                " Description: [Description 2]\n"
                " More details:[url2]\n\n"
                "... and so on for each update."
    )
    prompt = prompt_template.format(text=news_text)
    # Specify the Gemini model
    gen_model = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=GEMINI_API_KEY)
    response = gen_model.generate_content(prompt)
    return response.text

def gemin_agent(news_text,topic):
    prompt_template = PromptTemplate.from_template(
    "Take the following {text} and remove non english text, any text not related to the {topic} like 'Enter a different field to search' or 'Note', anything that is not related to the {topic}:\n\n"
    "display the {text} i.e is only in english language in the below format\n"
            " Headline: [Headline 1]\n"
            " Description: [Description 1]\n"
            " More details:[url1]\n\n"
            " Headline: [Headline 2]\n"
            " Description: [Description 2]\n"
            " More details:[url2]\n\n"
            "... and so on for each update." 
    )
    prompt = prompt_template.format(text=news_text,topic=topic)
    # Specify the Gemini model
    gen_model = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=GEMINI_API_KEY)
    response = gen_model.generate_content(prompt)
    return response.text


# Function to send user input and get response
# def chat(user_input):
#   response = gen_model.generate_content(user_input)
#   return response.text

# print(gemini_updates(prompt))
# Chat loop
# while True:
#   user_input = input("You: ")
#   bot_response = chat(user_input)
#   print("Chatbot:", bot_response)

  # Exit on 'bye' command
#   if user_input.lower() == "bye":
#     break

