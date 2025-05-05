from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Tillad Cross-Origin fra f.eks. din extension

@app.route('/send', methods=['POST'])
def receive_text():
    try:
        data = request.json
        if not data or "text" not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400

        statement = data["text"]
        print("Modtaget tekst:", statement)
        
        from main import main
        results = main(statement)  # Skal returnere liste med dicts

        return jsonify(results), 200

    except Exception as e:
        print("Fejl under behandling:", str(e))
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
