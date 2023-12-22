from flask import Flask, render_template, request, jsonify
import conversation_simulator  # Import your conversation simulator module
import traceback

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converse', methods=['POST'])
def converse():
    try:
        data = request.get_json()
        print('Received JSON data:', data)

        # Extracting parameters from JSON data
        agent1_name = data.get('agent1_name', 'Agent1')
        agent2_name = data.get('agent2_name', 'Agent2')
        referee_name = data.get('referee_name', 'Referee')
        topic = data.get('topic', 'No topic')
        steps = int(data.get('steps', 0))
        max_tokens_per_response = int(data.get('max_tokens_per_response', 50))
        response_delay = int(data.get('response_delay', 2))

        # Call the conversation function from the conversation_simulator module
        completed_conversation = conversation_simulator.converse(
            agent1_name, agent2_name, referee_name, topic, steps, 
            max_tokens_per_response, response_delay
        )

        # Return the JSON response
        return jsonify({'conversation': completed_conversation})

    except Exception as e:
        print(f"Error during conversation: {e}")
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
