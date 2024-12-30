from ascii_text.abecedario_ascii import abcii

def text_to_col(text):
    return [abcii.space() if c == ' ' else getattr(abcii, c.lower())() for c in text if c == ' ' or hasattr(abcii, c.lower())]

def print_text(text_arrays):
    # zip(*text_arrays) "desempaqueta" las sublistas y las agrupa por índice
    for line in zip(*text_arrays):
        print("".join(line))
