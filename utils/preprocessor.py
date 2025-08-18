from sentence_transformers import SentenceTransformer
import os

# Carga una sola vez el modelo de embeddings
EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'
embed_model = SentenceTransformer(EMBED_MODEL_NAME)

def cargar_corpus(path: str = 'legal_corpus'):
    """
    Lectura de todos los archivos .md en la carpeta
    se segmentan en trozos los parrafos y devuelve listas de textos y sus fuentes
    """
    textos = []
    fuentes = []
    for fname in sorted(os.listdir(path)):
        full_path = os.path.join(path, fname)
        if not (fname.endswith('.md') or fname.endswith('.txt')):
            continue
        with open(full_path, encoding='utf-8') as f:
            contenido = f.read()
        # Dividir por doble salto de linea
        trozos = [t.strip() for t in contenido.split('\n\n') if t.strip()]
        textos.extend(trozos)
        fuentes.extend([fname] * len(trozos))
    return textos, fuentes

def vectorizar_textos(textos: list[str]):
    """
    Dado un listado de textos sw retorna sus embeddings en un numpy array
    """
    embeddings = embed_model.encode(
        textos,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings
