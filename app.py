from flask import Flask, request, jsonify
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure it's set in Render's environment

# Define the webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    if not req or 'queryResult' not in req or 'queryText' not in req['queryResult']:
        return jsonify({"fulfillmentText": "Invalid request from Dialogflow"}), 400

    user_message = req['queryResult']['queryText']

    try:
        # Attempt to use GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
    except openai.error.OpenAIError as e:
        print(f"Error using GPT-4: {e}")
        try:
            # Fallback to GPT-3.5-turbo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
        except openai.error.OpenAIError as e2:
            print(f"Error using GPT-3.5: {e2}")
            return jsonify({
                "fulfillmentText": "Sorry, I am experiencing issues. Please try again later."
            }), 500

    # Extract the response from OpenAI
    chatgpt_response = response['choices'][0]['message']['content']
    print(f"Response from OpenAI: {chatgpt_response}")  # Log the response

    # Send the response back to Dialogflow
    return jsonify({"fulfillmentText": chatgpt_response})

if __name__ == '__main__':
    # Get the port from the environment or use a default (e.g., 5000)
    port = int(os.environ.get('PORT', 10000))

    # Run the app, setting the host to 0.0.0.0 for external visibility
    app.run(host='0.0.0.0', port=port)
