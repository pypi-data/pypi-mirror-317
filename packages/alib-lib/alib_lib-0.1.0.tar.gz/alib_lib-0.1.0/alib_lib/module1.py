import re

vowels = "аеёиоуыэюя"  
consonants = "бвгджзйклмнпрстфхцчшщ" 
punctuation = ".,?!:;-" 
russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" 

def is_vowel(char):
    
    return char.lower() in vowels

def is_consonant(char):
    
    return char.lower() in consonants

def is_punctuation(char):
    
    return char in punctuation



def word_frequency(text):
   
    words = re.findall(r'\b\w+\b', text.lower()) 
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

def average_word_length_in_sentence(sentence):
    
    words = re.findall(r'\b\w+\b', sentence)
    if not words:
      return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

def count_sentences(text):
    """Подсчитывает количество предложений в тексте."""
    sentences = re.split(r'[.!?]+', text) 
    return len([s for s in sentences if s.strip()]) 

def find_longest_words(text, num_words=3):
    """Находит n самых длинных слов в тексте."""
    words = re.findall(r'\b\w+\b', text.lower())
    sorted_words = sorted(words, key=len, reverse=True)
    return sorted_words[:num_words]


def remove_punctuation(text):
  """Удаляет знаки препинания из текста."""
  result = ""
  for char in text:
    if not is_punctuation(char):
      result += char
  return result

def word_tokenize(text):
    ##Разбивает текст на слова (по пробелам)
    text = remove_punctuation(text)
    return text.split()


