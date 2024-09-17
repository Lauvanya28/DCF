from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        user_message = req['queryResult']['queryText']
        
        print(f"User message: {user_message}")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        
        print(f"OpenAI Response: {response}")
        
        chatgpt_response = response['choices'][0]['message']['content']
        print(f"ChatGPT Response: {chatgpt_response}")  # Log the response
        
        return jsonify({"fulfillmentText": chatgpt_response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"fulfillmentText": "Sorry, I am experiencing issues. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)

