from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def cargar_corpus(path='legal_corpus'):
    textos = []
    fuentes = []
    for fname in os.listdir(path):
        with open(os.path.join(path, fname), encoding='utf-8') as f:
            texto = f.read()
            trozos = texto.split('\n\n')  # División por párrafos
            textos.extend(trozos)
            fuentes.extend([fname] * len(trozos))
    return textos, fuentes

def vectorizar_textos(textos):
    embeddings = model.encode(textos)
    return embeddings
