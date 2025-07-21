import faiss
import numpy as np
from utils import preprocessor

class BuscadorLegal:
    def __init__(self, corpus_path='legal_corpus'):
        self.textos, self.fuentes = preprocessor.cargar_corpus(corpus_path)
        self.embeddings = preprocessor.vectorizar_textos(self.textos)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def buscar(self, consulta, k=3):
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        emb = model.encode([consulta])
        D, I = self.index.search(emb, k)
        resultados = []
        for i in I[0]:
            resultados.append({
                'texto': self.textos[i],
                'fuente': self.fuentes[i]
            })
        return resultados
