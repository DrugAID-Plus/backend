import pickle
from bert_serving.client import BertClient
bc = BertClient()


with open('data.p', 'rb') as f:
    data = pickle.load(f)

final_data = []

for review in data:
    data_point = {}
    sentence = []
    label = []
    for value in review:
        if type(value[0]) == str:
            sentence.append(value[0])
        else:
            sentence.append(value[0].decode('utf8'))
        if type(value[1]) == int:
            label.append(value[1])
        else:
            if value[1].strip() == '':
                label.append(0)
            else:
                label.append(int(value[1]))
    data_point['label'] = label
    data_point['sentence'] = sentence 
    
    final_data.append(data_point)

final_vectors = []
for i in range(0, len(final_data), 32):
    sentences = [' '.join(value['sentence']) for value in final_data[i: i + 32]]
    vectors = bc.encode(sentences)
    for vector in vectors:
        final_vectors.append(vector)
        

for index, vector in enumerate(final_vectors):
    final_data[index]['vector'] = vector

with open('model_data.p', 'wb') as f:
    pickle.dump(final_data, f)