#from gradio_client import Client, handle_file
from langchain_core.tools import Tool
from typing import List, Optional
import logging
import requests
import os
import json
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_CLASSIFICATION_API = os.environ.get("DISEASE_DETECTION_API_ENDPOINT")
if not IMAGE_CLASSIFICATION_API:
    raise ValueError("OPENAI_API_KEY environment variable not set")
# API endpoint for the image classification model


def classify_image(image_path: str) -> str:
    """
    Retrieves rice leaf disease name by sending the image to an external API.

    Args:
        image_path (str): Path to the image file to classify.

    Returns:
        str: Information about the detected rice leaf disease.
    """
    if not os.path.exists(image_path):
        error_msg = f"Image file not found at path: {image_path}"
        logger.error(error_msg)
        return error_msg

    try:
        # Open the image file in binary mode
        with open(image_path, 'rb') as img_file:
            # Create a multipart form with the image file
            files = {'file': (os.path.basename(image_path),
                              img_file, 'image/jpeg')}

            # Send the POST request to the API
            logger.info(f"Sending image to API: {IMAGE_CLASSIFICATION_API}")
            response = requests.post(IMAGE_CLASSIFICATION_API, files=files)
            # client = Client("Rezuwan/vgg16")

            # response = client.predict(
            #     image=handle_file(image_path),
            #     api_name="/predict"
            # )
            # print(result['label'])

            # Check if the request was successful
            print(response)
            if response.status_code == 200:
                # Parse the JSON response
                result = response.json()
                logger.info(f"Received response: {result}")

                # Format the response
                if isinstance(result, dict):
                    disease_name = result

                    formatted_response = f"""
Disease Detected: {disease_name}
This disease was detected from analyzing the image you provided.
                    """
                    return formatted_response.strip()
                else:
                    return f"API returned unexpected response format: {result}"
            else:
                error_msg = f"API request failed with status code: {response.status_code}"
                logger.error(error_msg)
                return error_msg

    except Exception as e:
        error_msg = f"Error while processing image classification: {str(e)}"
        logger.error(error_msg)
        return error_msg


# Create the tool definition using the LangChain Tool class
disease_detection_tool = Tool(
    name="disease_detection_tool",
    func=classify_image,
    description="Analyzes images of rice plants to detect diseases and provide treatment recommendations. Use this tool when the user uploads an image of a rice plant or asks about identifying plant diseases from images.",

)


# client = Client("Rezuwan/vgg16")
# result = client.predict(
#     image=handle_file(
#         'https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
#     api_name="/predict"
# )
# # Print only the first label from the result
# print(result['label'])
