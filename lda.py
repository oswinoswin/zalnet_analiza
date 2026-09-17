from collections import Counter
from multiprocessing import freeze_support
from pprint import pprint

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

import requests
from gensim.corpora import Dictionary
import pandas as pd
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
url = "https://raw.githubusercontent.com/stopwords-iso/stopwords-pl/master/stopwords-pl.txt"
response = requests.get(url)
stopwords_pl = response.text.splitlines()
stop_set = set(stopwords_pl)




if __name__ == '__main__':
    freeze_support()
    df = pd.read_csv("dane/blogposts_lemmatized.csv")

    texts = df["lemmas"].apply(lambda x: x.split(" ")).tolist()
    words = [word for text in texts for word in text]
    counter = Counter(words)
    lda_input = [
        [token for token in text if counter[token] > 1 if token not in stop_set]
        for text in texts
    ]
    dictionary = Dictionary(lda_input)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(text) for text in lda_input]
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    num_topics = 5
    chunksize = 2000
    passes = 20
    iterations = 400
    eval_every = None  # Don't evaluate model perplexity, takes too much time.

    # Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )

    coherence_model = CoherenceModel(model=model, texts=lda_input, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()
    print(f'Coherence Score: {coherence_score}')

    vis_data = gensimvis.prepare(model, corpus, dictionary)
    pyLDAvis.save_html(vis_data, f'wyniki/lda_{num_topics}_topics.html')