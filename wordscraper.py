import requests
import re
from bs4 import BeautifulSoup as bs
import click
from datetime import datetime
from urllib.parse import urlparse, urljoin
from tqdm import tqdm

def get_html_of(url):
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to fetch the page. Status code: {resp.status_code}")
            return None
        return resp.content.decode()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the page. Error: {e}")
        return None

LEET_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7'],
    'b': ['8'],
    'g': ['6'],
    'q': ['9'],
    'z': ['2']
}

def leet_transformations(word, apply_leet=True):
    if not apply_leet:
        return {word}

    transformations = set()
    transformations.add(word)

    def helper(prefix, remaining):
        if not remaining:
            transformations.add(prefix)
            return
        char = remaining[0]
        rest = remaining[1:]

        helper(prefix + char, rest)

        if char.lower() in LEET_MAP:
            for leet_char in LEET_MAP[char.lower()]:
                helper(prefix + leet_char, rest)

    helper('', word)
    return transformations

def get_all_words_from(html):
    soup = bs(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)

def get_internal_links(html, base_url):
    soup = bs(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        url = urljoin(base_url, a_tag['href'])
        if urlparse(url).netloc == urlparse(base_url).netloc:
            links.add(url)
    return links

def crawl(url, depth, visited, word_locations):
    if depth == 0 or url in visited:
        return set()
    visited.add(url)

    html = get_html_of(url)
    if not html:
        return set()

    words = set(get_all_words_from(html))

    for word in words:
        if word not in word_locations:
            word_locations[word] = set()
        word_locations[word].add(url)

    internal_links = get_internal_links(html, url)

    for link in tqdm(internal_links, desc="Crawling links", leave=False):
        words.update(crawl(link, depth - 1, visited, word_locations))

    return words

def password_mutation(word, apply_mutation=False, apply_leet=False, apply_chars=False):
    mutation = set()

    mutation.add(word)
    mutation.add(word.capitalize())
    mutation.add(word.upper())

    if apply_mutation:
        if apply_leet:
            leet_mutations = leet_transformations(word, apply_leet)
            mutation.update(leet_mutations)

        if apply_chars:
            for base in leet_mutations:
                for num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    mutation.add(f"{base}{num}")
            for symbol in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ':', ';', '"', '\'', '<', '>', ',', '.', '?', '/']:
                mutation.add(f"{base}{symbol}")

    return list(mutation)

def search_words(word_locations, target_words):
    found = {word: urls for word, urls in word_locations.items() if word in target_words}
    not_found = set(target_words) - set(found.keys())

    if found:
        print("\nFound words and their locations:")
        for word, urls in found.items():
            print(f"- {word}:")
            for url in urls:
                print(f"  * {url}")
    else:
        print("No matching words were found.")

@click.command()
@click.option('--url', '-u', prompt='Enter Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length to count.')
@click.option('--fixed-length', '-f', default=None, type=int, help='Fixed word length to count.')
@click.option('--count', '-c', default=10, type=int, help='Number of top words to print.')
@click.option('--output', '-o', type=click.File('w'), help='Output file to save the results.')
@click.option('--depth', '-d', default=1, type=int, help='Depth of crawling.')
@click.option('--apply-mutation', '-am', is_flag=True, help="Apply base password mutation.")
@click.option('--apply-leet', '-al', is_flag=True, help="Apply leetspeak mutation.")
@click.option('--apply-chars', '-ac', is_flag=True, help="Apply character-based mutation (numbers, symbols).")
@click.option('--search', '-s', multiple=True, help='Search for specific words.')
def main(url, depth, length, fixed_length, count, output, apply_mutation, apply_leet, apply_chars, search):
    if length > 0 and fixed_length:
        print('Error: --length and --fixed-length are mutually exclusive.')
        return

    visited = set()
    word_locations = {}
    words = crawl(url, depth, visited, word_locations)

    if search:
        search_words(word_locations, search)
        return

    unique_words = set(words)

    if fixed_length:
        unique_words = {word for word in unique_words if len(word) == fixed_length}

    elif length > 0:
        unique_words = {word for word in unique_words if len(word) >= length}

    total_words = len(unique_words)

    if total_words == 0:
        print("No words of the specified length were found.")
        return

    top_words = sorted(unique_words, key=lambda word: len(word), reverse=True)[:count]

    result = []
    for word in top_words:
        result.append(word)
        if apply_mutation:
            mutations = password_mutation(
                word,
                apply_mutation=apply_mutation,
                apply_leet=apply_leet,
                apply_chars=apply_chars
            )
            result.extend(mutations)

    print(f"\nTotal number of unique words found: {total_words}")

    for line in result:
        print(line)

    if output:
        output.write('\n'.join(result))
        print(f'\nResults saved to {output.name}')

if __name__ == '__main__':
    main()
