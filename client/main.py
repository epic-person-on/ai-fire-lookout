import requests
import json
import base64

global lambda_url
lambda_url = "https://u0pnkhoo7d.execute-api.us-east-1.amazonaws.com/"

def convert_image(image):

    with open(image, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    return data

def get_labels(base64):

    image = {'image': base64}    
    x = requests.post(lambda_url, json = image)

    return x.text

def parse_response(response):
    
    parsed_data = json.loads(response)
    labels = parsed_data["labels"]

    return labels

def proccess_data(labels):
    if "Fire" in labels or "Smoke" in labels:
        print("fire detected")
    else:
        print("no fire detected")

def main(image):
    base_64 = convert_image(image)

    response = get_labels(base64)

    labels = parse_response(response)

    proccess_data(labels)







