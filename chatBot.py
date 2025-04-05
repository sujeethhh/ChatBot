from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
import base64
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
#from google import genai
#from google.genai import types

def openAi_bot(user_input):
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key="",
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a friendly human being."},
            {"role": "user", "content": user_input},
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1,
    )

    return response.choices[0].message.content

'''def geminiAi_bot(user_input):
    client = genai.Client(
        api_key="",
    )

    model = "gemini-2.5-pro-preview-03-25"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_input),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
    ):
    return(chunk.text)'''

def deepseek_bot(user_input):

    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
    # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(""),
    )

    response = client.complete(
        messages=[
            SystemMessage(""""""),
            UserMessage(user_input),
        ],
        model="DeepSeek-V3",
        temperature=0.8,
        max_tokens=2048,
        top_p=0.1
    )

    return (response.choices[0].message.content)



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def Home():
    return render_template("chatbot.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form["message"]
    bot_response = deepseek_bot(user_input)  # Call the bot function to get a response
    return jsonify({"response": bot_response})  # Send the bot response as JSON

if __name__ == "__main__":
    app.run(debug=True)
