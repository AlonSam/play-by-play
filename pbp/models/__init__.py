def to_camel(string: str) -> str:
    words = [word for word in string.split('_')]
    return ''.join([word.capitalize() if words.index(word) != 0 else word for word in words])