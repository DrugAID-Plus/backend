# encoding: utf-8
from models.experiments.get_data import Data

CHUNK_SPREADSHEET_ID = '1UvutkR2NQagGOsInWKwAtfzNv086wDYxb9JVJgcRsGc'
data = Data(CHUNK_SPREADSHEET_ID, './models/dataset/credentials.json')
sentences = data.get_sentences()
data.get_data_metrics()