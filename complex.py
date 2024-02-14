import re
import numpy as np



def read_file_to_dic(filepath):
    line_dict = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for index, line in enumerate(file):
                clean_line = line.strip()
                if clean_line not in line_dict: 
                    line_dict[clean_line] = index
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return line_dict

def clean_word(word):
    word = str(word)
    word = word.lower()  # Lowercase the word
    # Remove leading/trailing/inter-word punctuation
    cleaned_word = re.sub(r'(?<!\w)[\'\"?!;:,.]|(?<=\s)[\'\"?!;:,.]|[\'\"?!;:,.](?!\w)', '', word)
    return cleaned_word

def is_verbs(word, verbs_dic):
    return verbs_dic.get(word) is not None

def clean_text(text):
    text = str(text)
    words = text.split()
    cleaned_words = [clean_word(word) for word in words if clean_word(word)]
    return cleaned_words
    
def calculate_complexity(text: str, verbs_dic: dict )->float:
    words = clean_text(text)
    complexity = 0.0
    values = []
    has_one = False
    for word in words:
        if verbs_dic.get(word)is not None:
            has_one = True
            complexity += verbs_dic[word]
            values.append(verbs_dic[word])
    if not has_one:
        return 0
    return np.median(values)
    # return complexity / len(words), np.median(values), np.std(values), np.std(values) / np.median(values) 

def get_text_in_file(filepath):
    try:
        with open(filepath,
                    'r', encoding='utf-8') as file:
                text = file.read()
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return text

def get_words_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return clean_text(text)
