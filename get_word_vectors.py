import pickle
from bert_serving.client import BertClient
bc = BertClient()
with open('./model_data.p', 'rb') as f:
    data = pickle.load(f)

sentences = []
final_vectors = []
for value in data:
    sentence = ' '.join(value['sentence'])
    sentences.append(sentence)

for i in range(0, len(sentences), 32):
    vectors = bc.encode(sentences[i: i + 32])
    for vector in vectors:
        final_vectors.append(vector)

for index, vector in enumerate(vectors):
    data[index]['word_vectors'] = vector

with open('model_data_with_word_embeddings.p', 'wb') as f:
    pickle.dump(data, f)