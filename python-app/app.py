from flask import Flask, jsonify
import boto3
from dotenv import load_dotenv
import os

# get data from .env file
load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
TABLE_NAME = os.getenv('DYNAMODB_TABLE')
KEY_NAME = os.getenv('DYNAMODB_KEY_NAME')
KEY_VALUE = os.getenv('DYNAMODB_KEY_VALUE')

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

@app.route('/secret', methods=['GET'])
def get_secret():
    try:
        response = table.get_item(Key={KEY_NAME: KEY_VALUE})
        item = response.get('Item')

        if not item:
            return jsonify({"error": "Secret not found"}), 404

        return jsonify(item), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)