from google.colab import drive
import nltk
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
import pymorphy3

nltk.download('punkt_tab')

# Инициализируем морфологический анализатор и считываем текст с файла
morph = pymorphy3.MorphAnalyzer()
with open('text.txt', 'r', encoding="utf-8") as file:
    text = file.read().replace('\n', ' ')
print(text)

# Вспомогательная функция для получения морфологической информации
def get_morph_info(word):
    parsed = max(morph.parse(word), key=lambda p: p.score)
    tag = parsed.tag
    return {
        'lemma': parsed.normal_form,
        'pos': tag.POS,         # часть речи
        'gender': tag.gender,   # род
        'number': tag.number,   # число
        'case': tag.case        # падеж
    }

# Производим сегментацию
sentences = sent_tokenize(text, language="russian")

# Производим токенизацию
pairs = []
ALLOWED_ADJ_POS = {'ADJF', 'ADJS'}

for sentence in sentences:
  tokens = word_tokenize(sentence, language="russian")
  # убираем знаки препинания, пунктацию и т.д
  words = [word for word in tokens if word.isalpha()]

  for i in range(len(words) - 1):
      word1 = words[i]
      word2 = words[i + 1]

      info1 = get_morph_info(word1)
      info2 = get_morph_info(word2)

      pos1 = info1['pos']
      pos2 = info2['pos']

      # Проверяем пары слов на принадлежность к частям речи (существительное + прилагательное)
      if not ((pos1 == 'NOUN' and pos2 in ALLOWED_ADJ_POS) or (pos1 in ALLOWED_ADJ_POS and pos2 == 'NOUN')):
        continue

      # Проверяем согласование по роду, числу и падежу
      if None in [info1['gender'], info1['number'], info1['case'],
                  info2['gender'], info2['number'], info2['case']]:
        continue

      # Проверяем на совпадение рода, числа и падежа
      if (info1['gender'] == info2['gender'] and
          info1['number'] == info2['number'] and
          info1['case'] == info2['case']):
        pair = (info1['lemma'], info2['lemma'])
        pairs.append(pair)

# Выводм результат
for pair in pairs:

  print(f'{pair[0]} {pair[1]}')
