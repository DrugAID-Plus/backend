# encoding: utf-8
from ..dataset.sheets import Sheets
import pickle


class Data(object):
  def __init__(self, chunk_spreadsheet_id, credentials):
    self.chunk_spreadsheet_id = chunk_spreadsheet_id
    self.sheets = Sheets(credentials)
    self._get_chunk_ids()
    self.sentences = []
    for chunk_id in self.chunk_ids:
      print('Analyzing Chunk ID: {0}'.format(chunk_id))
      for sentence in self.get_chunk_data(chunk_id):
        if len(sentence) > 0:
          self.sentences.append(sentence)

  def _get_chunk_ids(self):
    self.chunks = self.sheets.get_spreadsheet_data(self.chunk_spreadsheet_id, 'A2:B')
    self.chunk_ids = []
    for chunk in self.chunks:
      self.chunk_ids.append(chunk[1])

  def get_chunk_data(self, chunk_id):
    values = self.sheets.get_spreadsheet_data(chunk_id, 'A2:B')
    sentences = []
    sentence = []
    for index, value in enumerate(values):
      if len(value) == 0 or len(value[0]) == 0:
        if len(sentence) != 0:
          sentences.append(sentence)
        sentence = []
        continue
      elif len(value) == 1:
        if len(values[index + 1]) == 1:
          break
        else:
          if value[0] == 'I\\xe2\\x80\\x99m':
            sentence.append(('I\'m', 0))
          else:
            sentence.append((value[0].encode('utf-8').strip(), 0))
      else:
        if value[0] == 'I\\xe2\\x80\\x99m':
            sentence.append(('I\'m', 0))
        else:
          sentence.append((value[0].encode('utf-8').strip(), value[1]))
    return sentences

  def get_sentences(self):
    return self.sentences

  def get_data_metrics(self):
    print('Total Number of Reviews: {0}'.format(len(self.sentences)))

  def save_data(self, file_path):
    with open(file_path, 'wb') as f:
      pickle.dump(self.sentences, f)