from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Tillad Cross-Origin fra f.eks. din extension

# Add extra_files to only watch your project files
extra_files = []
project_dir = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith('.py'):
            extra_files.append(os.path.join(root, file))

@app.route('/send', methods=['POST'])
def receive_text():
    try:
        data = request.json
        if not data or "text" not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400

        statement = data["text"]
        print("Modtaget tekst:", statement)
        
        from main import main
        results, support_percentage = main(statement)  # Unpack the tuple
        
        response = {
            "results": results,
            "support_percentage": support_percentage
        }
        return jsonify(response), 200

    except Exception as e:
        print("Fejl under behandling:", str(e))
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        extra_files=extra_files,  # Only watch project Python files
        use_reloader=True
    )