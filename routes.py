from flask import Blueprint, request, jsonify
import openai
import os

# Create a Blueprint for the webhook route
webhook_bp = Blueprint('webhook', __name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')  # Load the key from Render's environment variables

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_message = req['queryResult']['queryText']

    try:
        # Attempt to use GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
    except openai.error.OpenAIError as e:
        # Log the error and switch to GPT-3.5-turbo as a fallback
        print(f"Error using GPT-4: {e}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

    # Extract the response from ChatGPT
    chatgpt_response = response['choices'][0]['message']['content']
    print(f"Response from OpenAI: {chatgpt_response}")  # Log the response

    # Send the response back to Dialogflow
    return jsonify({
        "fulfillmentText": chatgpt_response
    })
