from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Add logic to handle the user message
    return jsonify({'response': "hello world"})

if __name__ == '__main__':
    app.run(debug=True)
