import base64
import os
import pickle
import time

import dotenv
from gpt_client.GPTClient import GPTClient


# load the .env file
dotenv.load_dotenv(dotenv.find_dotenv())
config = dotenv.dotenv_values()


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError as e:
        print(f"Image file ({image_path}) is not found. "
              f"Please check the file name and try again.")
        exit(1)


def extract_image_context(username, filename, image_path):
    encoded_image = encode_image(image_path)
    gpt_client = GPTClient(api_key=config["OPENAI_API_KEY"])
    if not os.path.exists(f"context_pickles/{username}/{filename}.pkl"):
        try:
            result = gpt_client.get_response(encoded_image)
            try:
                result = result.split(",")
            except Exception as e:
                print(f"Error occurred while parsing/splitting the response. "
                      f"Please check the response and try again: ", e)
                exit(1)
            return result
        except Exception as e:
            print(f"Error occurred while getting the response from GPT: ", e)
            if "unsupported image" not in str(e):
                time.sleep(10)
                extract_image_context(username, filename, image_path)
            else:
                return
    else:
        print(f"Context information for {username} - {filename} already exists. Skipping GPT extraction...")
    return


def process_and_save_image_context(username, filename, context_data):
    if not os.path.exists(f"context_pickles/{username}"):
        os.makedirs(f"context_pickles/{username}")
    try:
        if not os.path.exists(f"context_pickles/{username}/{filename}.pkl"):
            # save the context information as a pickle object
            with open(f"context_pickles/{username}/{filename}.pkl", "wb") as file:
                pickle.dump(context_data, file)
        else:
            print(f"Pickle file for {username} - {filename} already exists. Skipping Pickle dumping...")
    except Exception as e:
        print(f"Error occurred while saving the context information as a pickle object. "
              f"Please check the response and try again: ", e)
        exit(1)


if __name__ == "__main__":
    test_result = extract_image_context("../context_screenshots/egedursun/2023-12-25_23-26-13.353559.png")
    print(test_result)
