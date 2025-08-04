import faiss
import numpy as np
from utils.preprocessor import cargar_corpus, vectorizar_textos

class BuscadorLegal:
    def __init__(self, corpus_path: str = 'legal_corpus'):
        # 1) Carga y trocea corpus
        self.textos, self.fuentes = cargar_corpus(corpus_path)
        # 2) Calcula embeddings
        self.embeddings = vectorizar_textos(self.textos)
        # 3) Construye índice FAISS
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def buscar(self, query: str, k: int = 3) -> list[dict]:
        """
        Dada una consulta de usuario, devuelve los k parrafos más relevantes.
        """
        # Genera embedding de la consulta
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        q_emb = model.encode([query], convert_to_numpy=True)

        # Busca en FAISS
        D, I = self.index.search(q_emb, k)

        # Prepara resultado con texto y fuente
        resultados = []
        for i, dist in zip(I[0], D[0]):
            resultados.append({
            'texto': self.textos[i],
            'fuente': self.fuentes[i],
            'distancia': round(float(dist), 4)  # mayor legibilidad
        })
        return resultados