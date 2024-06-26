import csv
import cohere
from flask import Flask, request, jsonify

client = cohere.Client(api_key='YOUR_API_KEY')
dataset = []

def load_dataset_from_csv(file_path):
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
    return dataset


def generate_api_response(query, dataset):
    print(dataset)
    try:

        response = client.generate(
            prompt=query,
            max_tokens=500,
            temperature=0.5
        )

        api_response = ''.join(response)
        return api_response
    except Exception as e:
        return f"Error: {str(e)}"

csv_file_path = 'CARS_2.csv'

dataset = load_dataset_from_csv(csv_file_path)

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['message']
    api_response = generate_api_response(user_input, dataset)
    return jsonify({'response': api_response})

if __name__ == '__main__':
    app.run(debug=True)
