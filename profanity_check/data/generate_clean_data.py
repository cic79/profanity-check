import pandas as pd

dtype = {'comment_text': str, 'toxic': bool, 'severe_toxic': bool, 'obscene': bool, 'threat': bool, 'insult': bool,
         'identity_hate': bool}
rows = pd.read_csv('jigsaw-toxic-comment-train-google-it-cleaned.csv', dtype=dtype)

datas = []

for row in rows.itertuples(index=False, name=None):
    comment_text = row[3]
    # At least one between toxic, severe_toxic, obscene, threat, insult and identity_hate is True
    is_offensive = int(bool(row[4:].count(True)))
    datas.append((is_offensive, comment_text))

columns = ['is_offensive', 'text']
df = pd.DataFrame(data=datas, columns=columns)
df.to_csv('clean_data_it.csv', index=False)
