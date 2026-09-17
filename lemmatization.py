import requests
# import re
import pandas as pd
import spacy
from tqdm import tqdm


def lemmatize(text, nlp):
    # clean_text = text.lower()  # małe litery
    # clean_text = re.sub(r"[^a-ząćęłńóśźż\s]", "", clean_text)  # usuń znaki specjalne i emoji
    # clean_text = re.sub(r"\s+", " ", clean_text).strip()
    doc = nlp(text)
    clean_lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.lemma_ not in stop_set]
    return " ".join(clean_lemmas)

url = "https://raw.githubusercontent.com/stopwords-iso/stopwords-pl/master/stopwords-pl.txt"
response = requests.get(url)
stopwords_pl = response.text.splitlines()
stop_set = set(stopwords_pl)
nlp = spacy.load("pl_core_news_sm")

df = pd.read_csv("dane/blogposts_cleaned.csv", sep=",")
tqdm.pandas(desc="lemmatize sentences")
df["lemmas"] = df["cleaned_content"].progress_apply(lemmatize, nlp=nlp)
df.to_csv("dane/blogposts_lemmatized.csv", index=False, sep=",")
print(df.head())




