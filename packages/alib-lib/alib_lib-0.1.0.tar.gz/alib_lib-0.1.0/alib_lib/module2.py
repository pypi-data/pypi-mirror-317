
import re

def reverse_words_in_sentence(sentence):
    """Реверсирует порядок слов в предложении."""
    words = sentence.split()
    reversed_words = [word[::-1] for word in words] # Реверсируем слова
    result = ""

    for index, word in enumerate(words):
        result += reversed_words[index] # Используем index от оригинальных слов
        if index < len(words) - 1:
            result += " "

    return result

def get_nth_sentence(text, n):
    """Извлекает n-ое предложение из текста."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if 0 < n <= len(sentences):
        return sentences[n - 1]
    else:
        return "Invalid sentence number"
    
def is_palindrome(word):
    """Проверяет, является ли слово палиндромом."""
    word = word.lower()
    return word == word[::-1]
