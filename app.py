from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # This automatically finds index.html inside your templates folder!
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json or {}
    user_input = data.get('text', '')
    print(f"\n🌐 [API ROUTE] Incoming packet caught: '{user_input}'")
    return jsonify({"status": "success", "message": "Weights mapped back to hot cache registers!"})

if __name__ == '__main__':
    print("\n=== PREMEM FULL-STACK API SERVER ACTIVE (PORT 5000) ===")
    app.run(host='127.0.0.1', port=5000, debug=False)
