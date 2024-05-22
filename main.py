from langchain.prompts import PromptTemplate
import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from newsapii import newsapi1,newsapi2
from gemini_bot import gemini_updates,gemin_agent
# Initialize Flask app
app = Flask(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def agent(combined_txt,topic):
    # Define a clear prompt template
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

  # Construct the complete prompt with the user-provided text
  prompt = prompt_template.format(text=combined_txt,topic=topic)
  # Use openai.Completion.create for text generation

  response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
  message_content = response.choices[0].message.content

  return message_content
   
def generate_updates(news_text):
  """
  news_txtrizes a given text using the OpenAI API and GPT-3.5 model.

  Args:
      news_text: The text to be news_txtrized (string).

  Returns:
      A string containing the news_txtrized text.
  """

  # Define a clear prompt template
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

  # Construct the complete prompt with the user-provided text
  prompt = prompt_template.format(text=news_text)
  # Use openai.Completion.create for text generation
  
  response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
  message_content = response.choices[0].message.content

  return message_content

def get_text_chunks(text):
    """Splits text into smaller chunks of 1000 characters each."""
    chunk_size = 15000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

@app.route('/sqlagent/v2/api', methods=['POST'])
def main_function():
    data = request.json
    topic = data.get('topic')
    model= data.get('model')

    # main_article=newsapi2(topic)
    main_article=newsapi1(topic)

    print(len(main_article))
    if model=='gpt-3.5-turbo':
        if len(main_article)>15000:
            print('entered')
            blocks=get_text_chunks(main_article)
            news_txt=''
            for chunk in blocks:
                news_txt+='/n'+generate_updates(chunk)
            final=agent(news_txt,topic)
        else:
            news_txt=generate_updates(main_article)
            final=agent(news_txt,topic)
        print(final)
        print(len(final))
        return jsonify(final)
    elif model=="gemini-pro":
        if len(main_article)>15000:
            print('entered')
            blocks=get_text_chunks(main_article)
            news_txt=''
            for chunk in blocks:
                news_txt+='/n'+gemini_updates(chunk)
            final=gemin_agent(news_txt,topic)
        else:
            news_txt=gemini_updates(main_article)
            final=gemin_agent(news_txt,topic)
        print(final)
        print(len(final))
        return jsonify(final)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)




