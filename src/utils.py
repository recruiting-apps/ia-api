import requests
import os
import random

def download_file(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")

def sort_applications(applications, indexes, similarites):
    # sorted_applications = []
    # for index in indexes:
    #     sorted_applications.append(applications[index])
    random.shuffle(applications)
    return applications