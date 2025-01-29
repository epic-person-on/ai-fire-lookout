import json
import boto3
import base64
from botocore.exceptions import ClientError

# Initialize Rekognition client
rekognition_client = boto3.client('rekognition')

def detect_labels_from_base64(image_data):
    try:
        # Convert base64 string to bytes
        image_bytes = base64.b64decode(image_data)

        # Call Rekognition API to detect labels
        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,  # You can adjust this based on your requirements
            MinConfidence=75  # Minimum confidence level for labels to be detected
        )

        labels = [label['Name'] for label in response['Labels']]
        return labels
    except ClientError as e:
        print(f"Error detecting labels: {e}")
        raise e

def lambda_handler(event, context):
    try:
        # Parse the body of the event (base64-encoded image string)
        body = json.loads(event['body'])
        image_data = body['image']

        # Step 1: Detect labels using Rekognition
        labels = detect_labels_from_base64(image_data)
        
        # Return the detected labels in the response
        return {
            'statusCode': 200,
            'body': json.dumps({'labels': labels}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    except Exception as e:
        print(f"Error in Lambda handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }

