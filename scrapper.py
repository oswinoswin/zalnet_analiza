import requests
from bs4 import BeautifulSoup

BASE_ULR=f"https://zalnet.pl/blog/page/"

def download_urls():
    urls = []
    for page in range(1, 11):
        url = f"{BASE_ULR}{page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.select('h2.entry-title > a[rel="bookmark"]'):
                full_url = requests.compat.urljoin(url, tag["href"])
                print(f"Found URL: {full_url}")
                if full_url not in urls:
                    urls.append(full_url)

            print(f"Page {page} matching URLs:")
            for found_url in urls:
                print(found_url)
        else:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")

    with open("urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")


def download_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        content_div = soup.find("div", class_="entry-content")
        if content_div:
            return content_div.get_text(separator="\n", strip=True)
        else:
            print(f"No content found for URL: {url}")
            return None
    else:
        print(f"Failed to fetch URL: {url}, status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # download_urls()
    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f.readlines()]

        for url in urls:
            content = download_content(url)
            if content:
                filename = url.split("/")[-2] + ".txt"  # Use the second last part of the URL as filename
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Saved content to {filename}")