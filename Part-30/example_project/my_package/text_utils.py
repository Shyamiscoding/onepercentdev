def clean_text(text):
    """Removes extra spaces and makes everything lowercase."""
    return text.strip().lower()

def count_words(text):
    """Returns the number of words in a string."""
    return len(text.split())

def reverse_words(text):
    """Reverses the order of words. 'hello world' → 'world hello'"""
    return " ".join(text.split()[::-1])
