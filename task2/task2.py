import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt


def mapper(text):
    words = text.split()  # Розбиваємо текст на слова
    return [(word.lower(), 1) for word in words]


def reducer(mapped_items):
    word_counts = Counter()
    for word, count in mapped_items:
        word_counts[word] += count
    return word_counts.items()


def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Top {} Words".format(top_n))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        visible_text = soup.get_text()
        mapped_items = mapper(visible_text)
        word_counts = reducer(mapped_items)
        visualize_top_words(Counter(dict(word_counts)))
    else:
        print("Failed to fetch URL")


if __name__ == "__main__":
    url = "https://www.python.org/"
    main(url)
