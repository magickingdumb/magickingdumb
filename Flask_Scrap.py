from flask import Flask, render_template, request, jsonify
import threading
import time
import os
import json

app = Flask(__name__)

# Function to save user activity data
def save_data(data):
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    file_name = f"user_activity_{timestamp}.json"
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Data saved in {file_name}")

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for logging user activity data
@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    save_data(data)
    return jsonify(success=True)

# Main function to start the Flask web server
def main():
    if not os.path.exists("data"):
        os.mkdir("data")
    os.chdir("data")
    app.run()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
