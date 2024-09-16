from flask import Flask, request, jsonify
import openai
import os

# Initialize the Flask app
app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Route to handle the root ("/") and return a simple message
@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse the incoming request from Dialogflow
        req = request.get_json(silent=True, force=True)
        user_message = req['queryResult']['queryText']
        
        # Log the received message
        print(f"User message: {user_message}")
        
        # Call OpenAI API using the basic model (gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Log OpenAI response details
        print(f"OpenAI Response: {response}")
        
        # Extract ChatGPT response
        chatgpt_response = response['choices'][0]['message']['content']
        print(f"ChatGPT Response: {chatgpt_response}")  # Log the response
        
        # Return the response to Dialogflow
        return jsonify({"fulfillmentText": chatgpt_response})
    
    except Exception as e:
        # Print the error to logs and return a default message
        print(f"Error: {str(e)}")
        return jsonify({"fulfillmentText": "Sorry, I am experiencing issues. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)

