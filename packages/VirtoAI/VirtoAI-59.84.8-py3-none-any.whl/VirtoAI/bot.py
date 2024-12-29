import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from functools import lru_cache
from sys import stdout, platform
from time import sleep
from os import system
from cryptography.fernet import Fernet
import requests
import threading

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

class Bot:
    key = 'lZcOmICNE1CapiZm-P8FtxRNezI1i2LQkOJAq82MI7Y='
    encrypted_url = 'gAAAAABncO877XCHpnyNBFQ5ZYD26B_CX1Oe3B4kS-TQJUFpVKKqXsEZkINlj2o8GA995W-z154SXlqRO78wN3enFJkHgwk94qhOQtqIt5GDUi4uA69Q2IHMabodVvdi11XiD8Wtq3QW'
    key = key.encode()
    encrypted_url = encrypted_url.encode()
    cipher_suite = Fernet(key)
    url = cipher_suite.decrypt(encrypted_url).decode()
    
    def __init__(self, name):
        self.name = name
        self.data = []
        self.preprocessed_data = []
        self.data_loaded = threading.Event()
        threading.Thread(
            target=self.load_data_async,
            args=(self.url,),
        ).start()

    @lru_cache(maxsize=None)
    def preprocess_text(self, text):
        corrected_text = str(TextBlob(text).correct())
        
        words = word_tokenize(corrected_text)
        
        clean_tokens = [re.sub(r"[^a-zA-Z0-9]", "", token).lower() for token in words]
        
        stop_words = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in clean_tokens if token not in stop_words]
        
        tokens = [token for token in tokens if token]
        
        return tokens

    def evaluate_math_expression(self, expr):
        try:
            math_match = re.fullmatch(r'[0-9+\-*/^(). ]+', expr)
            if math_match:
                result = eval(expr.replace('^', '**'))
                return f"The answer to '{expr.replace('**', '^')}' is {result}."
            else:
                return None
        except (SyntaxError, ValueError):
            return None
        except Exception as e:
            return f"Error: {e}"

    def generate_response(self, user_input):
        try:
            math_expression = self.evaluate_math_expression(user_input)
            if math_expression:
                return math_expression

            user_input_tokens = self.preprocess_text(user_input)
            if len(user_input) < 4:
                return f"Must be a minimum of 4 characters. Not {len(user_input)}."

            max_similarity = 0
            best_response = None

            for question_tokens, answers in self.preprocessed_data:
                if question_tokens and user_input_tokens:
                    common_tokens = set(question_tokens) & set(user_input_tokens)
                    similarity = len(common_tokens) / max(len(question_tokens), len(user_input_tokens))
                else:
                    similarity = 0

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = random.choice(answers)

            if best_response:
                return best_response
            else:
                return "I'm sorry, I didn't understand your question."
        except Exception as e:
            return f"Error: {e}"

    def load_data_async(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
            self.preprocessed_data = [
                (self.preprocess_text(entry["question"]), entry["answers"])
                for entry in self.data
            ]
            self.data_loaded.set()
        except Exception as e:
            print("Error loading AI.")
            quit()

def typewriter(txt):
    min = 0.0000001
    max = 0.01
    for char in txt:
        stdout.write(char)
        stdout.flush()
        sleep(random.uniform(min, max))


def run():
    bot = Bot(name="Virto")

    try:
        while True:
            if not bot.data_loaded.is_set():
                print("Loading...")
                bot.data_loaded.wait()
                
                if platform.lower().startswith("win"):
                    system('cls')
                else:
                    system('clear')

            user_input = input("You: ")
            if user_input.lower() == "exit":
                typewriter("Exiting...\n")
                break
            else:
                response = bot.generate_response(user_input)
                typewriter(f'{bot.name}: {response}\n')

    except KeyboardInterrupt:
        typewriter("\nExiting...\n")


if __name__ == "__main__":
    run()
