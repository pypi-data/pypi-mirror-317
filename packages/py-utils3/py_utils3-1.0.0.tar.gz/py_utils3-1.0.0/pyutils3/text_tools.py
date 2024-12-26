# smart_library/text_tools.py
from collections import Counter

def analyze_text(text):
    """Analyze text: word count, character count, and word frequency."""
    words = text.split()
    char_count = len(text)
    word_count = len(words)
    word_frequency = dict(Counter(words))
    return {'word_count': word_count, 'char_count': char_count, 'word_frequency': word_frequency}

def extract_keywords(text, top_n=5):
    """Extract the top N most frequent keywords from the text."""
    words = text.split()
    word_count = Counter(words)
    return word_count.most_common(top_n)
