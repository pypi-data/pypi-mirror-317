from alib_lib import module1 as ta
from alib_lib import module2 as tm
from alib_lib.module1 import remove_punctuation, word_tokenize

text = 'Then he was gone, and the sound of his car on the gravel came moments later. Margaret could only watch in disappointment as he sped away. He had forgotten once again. Overwhelmed with frustration, Margaret decided to confront him. She dressed, skipped breakfast, and drove after him to his office. When she opened the office door, her jaw dropped. There was a burst of camera flashes, and a chorus of “Happy Birthday!” filled the room. There was George, grinning ear to ear. In front of her was a sea of all her friends’ faces, and a sumptuous spread of her favourite foods. Then her favourite songs began to play. The office had been transformed into the best party venue she could have hoped for.'
sentence = "The quick brown fox jumps over the lazy dog."
other_sentence = "This is a short sentence!"


print("--- Testing TextAnalyzer (module1) ---")
print("Word frequencies:", ta.word_frequency(text))
print("Average word length in sentence:", ta.average_word_length_in_sentence(sentence))
print("Number of sentences:", ta.count_sentences(text))
print("Longest words:", ta.find_longest_words(text))

print("\n--- Testing TextManipulator (module2) ---")
print("Reversed words:", tm.reverse_words_in_sentence(sentence))
print("Third sentence:", tm.get_nth_sentence(text, 3))
print("Sentence 10:", tm.get_nth_sentence(text, 10))


print("\n---Testing long text---")
print("Longest words in long text:", ta.find_longest_words(text, 5))
print("Reversed long text first sentence:", tm.reverse_words_in_sentence(tm.get_nth_sentence(text, 1)))


print(f"Слова: {word_tokenize(text)}")
