import os
import pickle

import pyautogui
import time
import datetime as dt

from context_extractor.context_extractor_processor import extract_image_context, process_and_save_image_context
from presentation_builder.presentation_builder_processor import build_presentation_data, build_knowledge_graph

REFRESH_INTERVAL = 5


def tracking_mode():
    username = input("Context tracking will begin, please provide your username: ")
    print("Context tracking is now active. Frequency refresh interval is 5 seconds.")
    while True:
        time.sleep(REFRESH_INTERVAL)
        screen = pyautogui.screenshot()
        timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
        # create folder for user if not exists
        if not os.path.exists(f"context_screenshots/{username}"):
            os.makedirs(f"context_screenshots/{username}")
        save_path = f"context_screenshots/{username}/{timestamp}.png"
        print("#: ", save_path)
        screen.save(save_path)


def analysis_mode():
    # recursively iterate through the contents of the context_screenshots folder
    for root, dirs, files in os.walk("context_screenshots"):
        for file in files:
            if root.__contains__("/"):
                username = root.split("/")[1]
                filename = file.split(".")[0]
                # extract context
                print(f"Extracting context for {username} - {filename}")
                context_data = extract_image_context(image_path=f"{root}/{file}", username=username, filename=filename)
                # save context
                process_and_save_image_context(username=username, filename=filename, context_data=context_data)


def presentation_mode():
    for limit in [10, 20, 40, 50, 60, 80, 100, 200, 250, 300, 400, 500, 700, 800, 1000]:
        freqs = build_presentation_data()
        build_knowledge_graph(freqs, limit_words=limit)


def main():
    mode = input("Context Tracker is ready to start. \n Press (1) for Tracking "
                 "Mode. \n Press (2) for Analysis Mode. \n Press (3) for Presentation Mode. \n")
    if mode == "1":
        tracking_mode()
    elif mode == "2":
        analysis_mode()
    elif mode == "3":
        presentation_mode()
    else:
        print("Invalid input. Please try again.")
        main()


if __name__ == "__main__":
    # run the app
    main()
