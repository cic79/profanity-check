import pandas as pd

from profanity_check import predict, predict_prob
from profanity_check.polygen import get_random_polygen_text


def test_accuracy():
    texts = [
        'Hello there, how are you',
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
        '!!!! Click this now!!! -> https://example.com',
        'fuck you',
        'fUcK u',
        'GO TO hElL, you dirty scum',
    ]
    assert list(predict(texts)) == [0, 1, 0, 1, 1, 1]

    probs = predict_prob(texts)
    for i in range(len(probs)):
        if i == 0 or i == 2:
            assert probs[i] <= 0.5
        else:
            assert probs[i] >= 0.5


def test_edge_cases():
    texts = [
        '',
        '                    ',
        'this is but a test string, there is no offensive language to be found here! :) ' * 25,
        'aaaaaaa' * 100,
    ]
    assert list(predict(texts)) == [0, 0, 0, 0]


def test_italian_accuracy_print(count=10, show_only_profanity=True):
    for i in range(count):
        text = get_random_polygen_text()
        if not show_only_profanity or predict([text])[0]:
            print(text, predict_prob([text])[0], predict([text])[0])


def test_italian_accuracy_csv(count=10):
    datas = []
    for i in range(count):
        text = get_random_polygen_text()
        datas.append((text, predict([text])[0], predict_prob([text])[0]))
    columns = ('text', 'is_offensive', 'prob')
    df = pd.DataFrame(data=datas, columns=columns)
    df.to_csv('test_italian_accuracy.csv', index=False)


if __name__ == '__main__':
    test_italian_accuracy_csv(count=10000)
