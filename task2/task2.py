import requests
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

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

def process_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        visible_text = soup.get_text()
        mapped_items = mapper(visible_text)
        word_counts = reducer(mapped_items)
        return Counter(dict(word_counts))
    else:
        print("Failed to fetch URL")
        return Counter()

def main(url):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(process_url, url)
        word_counts = future.result()
        visualize_top_words(word_counts)

if __name__ == "__main__":
    url = "https://www.python.org/"
    main(url)
