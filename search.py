import os
import sys
import nltk
import requests
import json
from colorama import init, Fore, Style
import re
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# colorama init
init()


# text colors
red_color_code = Fore.RED
green_color_code = Fore.GREEN
reset_color_code = Fore.RESET
yellow_color_code = Fore.YELLOW


def search_files_for_keywords(keywords, directory='Daily'):
    relevant_texts = ''

    # Walk through the directory to find all txt files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                    if any(keyword.lower() in text.lower() for keyword in keywords):
                        relevant_texts = relevant_texts.join(text)

    return relevant_texts


def extract_keywords(question):
    # Tokenize the question and remove stopwords
    words = word_tokenize(question)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.lower() not in stop_words and word.isalnum()]
    return keywords


def check_api(key_file):
    # found
    if os.path.exists(key_file):
        f = open(key_file, 'r')
        try:
            GEMINI_API_KEY = f.readline().strip('\n')
            return GEMINI_API_KEY
        except Exception as e:
            print("Error reading api key from text file.")
            print(e)
            input()
            sys.exit()
    # not found
    else:
        GEMINI_API_KEY = str(input("Enter Gemini API key: "))
        with open(key_file, "w") as f:
            f.write(GEMINI_API_KEY)

        return GEMINI_API_KEY


def search_files_for_answer(question, directory='Daily'):
    # List to store all the texts from the txt files
    all_texts = []

    # Walk through the directory to find all txt files
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_texts.append(f.read())

    # Combine all texts into one large string
    combined_text = "\n".join(all_texts)
    question = question.join("\n\n below is the data separate by dates. According to only the below data answer the above question "
                "very briefly. Also mention the date the same way as below data. keep it very brief and direct."
                "\n\n").join(combined_text)
    # Use OpenAI's API to process the question and search the text
    ask_gemini(question)


def ask_gemini(prompt: str = ""):

    # print(f"{red_color_code}Type 'Kill' & hit enter to leave the chat!!")

    if prompt.lower() != "kill":
        # prompt = input(f"{reset_color_code}Me: ")

        # request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # headers
        headers = {
            'Content-Type': 'application/json'
        }

        # POST request
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            try:
                response_text = response_json.get("candidates")[0].get("content").get("parts")[0].get("text")
                print(f"{green_color_code}Gemini: {response_text}")
            except Exception as e:
                response_text = f"{red_color_code}Error in response: {e}"
            # print(json.dumps(response_json, indent=2))
        else:
            print(f"{red_color_code}Error: {response.status_code}, {response.text}")

    else:
        print(f"{yellow_color_code}Left the chat!🕊️")
        exit()


if __name__ == '__main__':
    # look for API key in txt file
    key_file = "GEMINI_API_KEY.txt"
    GEMINI_API_KEY = check_api(key_file)

    # endpoint URL
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + GEMINI_API_KEY

    question = input(f"{reset_color_code}Me: ")
    keywords = extract_keywords(question)
    print(keywords)

    relevant_texts = search_files_for_keywords(keywords)
    print(relevant_texts)



    # search_files_for_answer(question=question)

    input()

