import requests
import json
import base64
import os


global lambda_url
lambda_url = "https://u0pnkhoo7d.execute-api.us-east-1.amazonaws.com/"


def convert_image(image):
    with open(image, "rb") as image_file:
        data = base64.b64encode(image_file.read())

    # Decode bytes to string
    return data.decode('utf-8')



def get_labels(base64):

    image = {'image': base64}
    x = requests.post(lambda_url, json=image)

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
    if not os.path.isfile(image):
        print(f"Error: {image} not found.")
        return

    base64_data = convert_image(image)

    response = get_labels(base64_data)

    labels = parse_response(response)

    proccess_data(labels)



main("client/image/fire.png")
