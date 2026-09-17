import re

import pandas as pd

import os

def make_csv_from_blogposts():
    p = r"blogposts"

    posts = []
    for e in os.scandir(p):
        if e.is_file():
            with open(e.path, "r", encoding="utf-8") as f:
                print("Content of", e.name, ":")
                content = f.read()
                print(content)
                posts.append((e.name, content))

    df = pd.DataFrame(posts, columns=["filename", "content"])
    df.to_csv("dane/blogposts.csv", index=False, sep=",")

def simple_cleaning(text):
    clean_text = text.lower()  # małe litery
    clean_text = re.sub(r"http\S+", "", clean_text)  # usuń linki
    clean_text = re.sub(r"[^a-ząćęłńóśźż\s]", "", clean_text)  # usuń znaki specjalne i emoji
    clean_text = re.sub(r"\s+", " ", clean_text).strip()  # usuń nadmiarowe spacje
    return clean_text


df = pd.read_csv("dane/blogposts.csv", sep=",")
print(df.head())

df["cleaned_content"] = df["content"].apply(simple_cleaning)
df.to_csv("dane/blogposts_cleaned.csv", index=False, sep=",")

print(df.head())