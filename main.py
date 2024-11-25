import re

def get_book_text(path):
    with open(path) as f:
        return f.read()

def get_num_words(text):
    words = text.split()
    return len(words)

def get_chars_dict(text):
    chars = {}
    for c in text:
        lowered = c.lower()
        if lowered in chars:
            chars[lowered] += 1
        else:
            chars[lowered] = 1
    return chars

def sort_on(d):
    return d["num"]

def chars_dict_to_sorted_list(num_chars_dict):
    sorted_list = []
    for ch in num_chars_dict:
        sorted_list.append({"char": ch, "num": num_chars_dict[ch]})
    sorted_list.sort(reverse=True, key=sort_on)
    return sorted_list

def count_syllables(text):
    text = text.lower()
    syllable_count = 0
    vowels = "aeiouy"
    text = re.sub(r'[^a-z]', ' ', text)
    words = text.split()
    
    for word in words:
        word_syllables = 0
        if word[0] in vowels:
            word_syllables += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                word_syllables += 1
        if word.endswith("e"):
            word_syllables -= 1
        if word_syllables == 0:
            word_syllables = 1
        syllable_count += word_syllables
    
    return syllable_count

def get_reading_level(text):
    sentences = text.count('.') + text.count('!') + text.count('?')
    words = len(text.split())
    syllables = count_syllables(text)
    # Implement Flesch-Kincaid Grade Level
    return 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59

def get_word_frequency(text):
    words = {}
    for word in text.lower().split():
        words[word] = words.get(word, 0) + 1
    return words

def get_sentence_stats(text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    lengths = [len(s.split()) for s in sentences]
    return {
        'avg_length': sum(lengths) / len(lengths),
        'max_length': max(lengths),
        'min_length': min(lengths)
    }

def main():
    book_path = "books/frankenstein.txt"
    text = get_book_text(book_path)
    
    num_words = get_num_words(text)
    chars_dict = get_chars_dict(text)
    chars_sorted_list = chars_dict_to_sorted_list(chars_dict)
    reading_level = get_reading_level(text)
    word_frequency = get_word_frequency(text)
    sentence_stats = get_sentence_stats(text)

    print(f"--- Begin report of {book_path} ---")
    print(f"{num_words} words found in the document")
    print()

    for item in chars_sorted_list:
        if not item["char"].isalpha():
            continue
        print(f"The '{item['char']}' character was found {item['num']} times")

    print()
    print(f"Reading Level: {reading_level:.2f}")
    print()
    print("Word Frequency:")
    for word, freq in word_frequency.items():
        print(f"{word}: {freq}")
    
    print()
    print("Sentence Statistics:")
    print(f"Average Sentence Length: {sentence_stats['avg_length']:.2f} words")
    print(f"Longest Sentence Length: {sentence_stats['max_length']} words")
    print(f"Shortest Sentence Length: {sentence_stats['min_length']} words")

    print("--- End report ---")

if __name__ == "__main__":
    main()