import pandas as pd
import numpy as np

i = 0

dtype = {'comment_text': str, 'toxic': np.bool, 'severe_toxic': np.bool, 'obscene': np.bool, 'threat': np.bool,
         'insult': np.bool, 'identity_hate': np.bool}
rows = pd.read_csv('jigsaw-toxic-comment-train-google-it-cleaned.csv', dtype=dtype)

for row in rows.itertuples(index=False, name=None):
    print(row)
    comment = row[2]
    print(comment)
    i += 1
    if i > 1:
        break
