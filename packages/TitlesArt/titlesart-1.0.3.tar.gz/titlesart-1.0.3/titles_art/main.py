# Importa las funciones necesarias del archivo abecedario_ascii.py
from titles_art.abecedario_ascii import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, space

def textToCol(text):
    # Código para convertir el texto en arte ASCII usando las funciones importadas
    return [space() if c == ' ' else globals()[c.lower()]() for c in text if c == ' ' or c.lower() in globals()]

def printText(text_arrays):
    for line in zip(*text_arrays):
        print("".join(line))
