from sentence_transformers import SentenceTransformer

model = SentenceTransformer('../models/all-MiniLM-L6-v2')


embeddings = model.encode(sentences="要生成 embedding 的输入文本，字符串形式。")




for tempembedding in embeddings :
    print(f"{tempembedding}")