# Import necessary libraries
import os
import random
import re
import time
import requests
import numpy as np
import pandas as pd
import math
import pickle
import urllib3
import sys
import ssl
from lxml import html
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from collections import Counter, defaultdict
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
from googlesearch import search
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load SentenceTransformer model
model_sent_transformer = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}
exclude = [
    "Thank you for your patience",
    "Subscribe",
    "subscribe",
    "trouble retrieving the article content",
    "browser settings",
    "Thank you for your patience while we verify access. If you are in Reader mode please exit and log into your Times account, or subscribe for all of The Times.",
    "Thank you for your patience while we verify access.",
    "Already a subscriber? Log in.",
    "Want all of The Times? Subscribe.",
    "Advertisement",
    "Site Index",
    "Thank you for your patience while we verify access. If you are in Reader mode please exit andlog intoyour Times account, orsubscribefor all of The Times.",
    "Already a subscriber?Log in.",
    "Want all of The Times?Subscribe.",
    "Site Information Navigation",
    "Please enable JS and disable any ad blocker",
    "©2024 FOX News Network, LLC. All rights reserved. This material may not be published, broadcast, rewritten, or redistributed. All market data delayed 20 minutes.",
]


def fetch_article_text_sequential(url):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:

        # Send a request to the webpage with the specified headers
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Check that the request was successful

        # Parse the webpage content
        soup = BeautifulSoup(response.text, "html.parser")

        # Initialize an empty list to store the text sequentially
        article_content = []

        # Define the tags we are interested in (headlines and paragraphs)
        tags_of_interest = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]

        # Find all tags of interest in the order they appear in the document
        for tag in soup.find_all(tags_of_interest):
            if not any(
                excluded_phrase in tag.get_text() for excluded_phrase in exclude
            ):
                text = tag.get_text(strip=True)
                article_content.append(text)

        return "\n".join(article_content)

    except:
        return None


def fetch_webpage(url):
    # Define a list of user agents
    user_agents = [
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        # Add more User-Agents as needed
    ]

    # Create an unverified SSL context
    context = ssl._create_unverified_context()

    exclude = [
        "Thank you for your patience",
        "Subscribe",
        "subscribe",
        "trouble retrieving the article content",
        "browser settings",
        "Thank you for your patience while we verify access. If you are in Reader mode please exit and log into your Times account, or subscribe for all of The Times.",
        "Thank you for your patience while we verify access.",
        "Already a subscriber? Log in.",
        "Want all of The Times? Subscribe.",
        "Advertisement",
        "Site Index",
        "Thank you for your patience while we verify access. If you are in Reader mode please exit andlog intoyour Times account, orsubscribefor all of The Times.",
        "Already a subscriber?Log in.",
        "Want all of The Times?Subscribe.",
        "Site Information Navigation",
    ]

    """Fetch webpage content with rotating user-agents and bypass SSL verification."""
    try:
        # Randomly select a user-agent
        user_agent = random.choice(user_agents)

        # Set up request with the random user-agent
        req = Request(url, headers={"User-Agent": user_agent})

        # Fetch webpage content, bypassing SSL verification
        with urlopen(req, timeout=10, context=context) as response:
            content = response.read()
            response_encoding = response.headers.get_content_charset() or "utf-8"
            # Decode the content
            content = content.decode(response_encoding)

        if not content.strip():
            return ""

        try:
            # Parse the content using lxml
            tree = html.fromstring(content)
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return ""

        # Extract specified tags and filter content in one loop
        filtered_data = []
        tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p"]
        for tag in tags:
            for element in tree.xpath(f"//{tag}"):
                sentence = element.text_content()
                # Only add the sentence if it does not contain any of the excluded phrases
                if not any(excluded_phrase in sentence for excluded_phrase in exclude):
                    filtered_data.append(sentence)

        return "\n".join(filtered_data)

    except Exception as e:
        print(f"Error: {e}")
        return ""


def get_google_search_results(query, start=0):
    search_url = "https://www.google.com/search"
    params = {"q": query, "start": start}

    response = requests.get(
        search_url, timeout=5, verify=False, params=params, headers=headers
    )
    soup = BeautifulSoup(response.text, "html.parser")

    search_results = []
    for g in soup.find_all(class_="g"):
        title = g.find("h3").text if g.find("h3") else "No title"
        link = g.find("a")["href"] if g.find("a") else "No link"

        if not link.lower().endswith((".pdf", ".PDF")):
            search_results.append({"title": title, "link": link})

    return search_results


def fetch_sentences_from_html(html):
    try:
        # Parse the string with BeautifulSoup
        if html == None:
            return []
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)

        # print(sentences)

        return sentences
    except Exception as e:
        # print(f"Failed to fetch {html}: {str(e)}")
        return []


# Function to rank sentences using cosine similarity
def rank_sentences(sentences):
    if not sentences:
        return []  # Return an empty list if no sentences are found

    embeddings = model_sent_transformer.encode(sentences, convert_to_tensor=True)

    # Compute pairwise cosine similarity between sentences
    similarities = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()

    # Calculate the average similarity for each sentence
    avg_similarities = np.mean(similarities, axis=1)

    # Rank sentences based on their average similarity
    ranked_sentences = sorted(
        zip(sentences, avg_similarities), key=lambda x: x[1], reverse=True
    )
    ranked_sentences = [sentence for sentence, _ in ranked_sentences]

    return ranked_sentences[: min(len(ranked_sentences), 2000)]


def rank_sentences_new(sentences, query, top_n=20):
    if sentences == None:
        return []
    sentences = re.split("\n", sentences.strip())
    # Remove any empty strings from the list
    [sentence.strip() for sentence in sentences if sentence.strip()]
    vectorizer = TfidfVectorizer().fit_transform([query] + sentences)
    vectors = vectorizer.toarray()
    query_vector = vectors[0]
    sentences_vectors = vectors[1:]
    cosine_similarities = cosine_similarity([query_vector], sentences_vectors).flatten()
    ranked_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return [sentences[idx] for idx in ranked_indices]


domains = [
    "wikipedia.org",
    "nytimes.com",
    "cnn.com",
    "bbc.com",
    "theguardian.com",
    "forbes.com",
    "reuters.com",
    "cnbc.com",
    "bloomberg.com",
    "foxnews.com",
    "npr.org",
    "washingtonpost.com",
    "wsj.com",
    "aljazeera.com",
    "ft.com",
    "huffpost.com",
    "nationalgeographic.com",
    "scientificamerican.com",
    "nature.com",
    "time.com",
    "usatoday.com",
    "apnews.com",
    "abcnews.go.com",
    "cbsnews.com",
    "nbcnews.com",
    "news.yahoo.com",
    "theatlantic.com",
    "vox.com",
    "politico.com",
    "economist.com",
    "en.wikipedia.org",
    "nytimes.com",
    "propublica.org",
    "usatoday.com",
    "latimes.com",
    "thehill.com",
    "pbs.org",
    "timesofindia.indiatimes.com",
    "thetimes.com",
    "telegraphindia.com",
    "ft.com",
    "news.sky.com",
    "cbc.ca",
    "ctvnews.ca",
    "abc.net.au",
    "straitstimes.com",
    "hindustantimes.com",
    "thehindu.com",
    "chinadaily.com.cn",
    "aljazeera.com",
    "gulfnews.com",
    "economist.com",
    "foreignpolicy.com",
    "theintercept.com",
    "nature.com",
]


# def get_web_content(user_query,num_results_needed):
def get_web_content(user_query, num_urls):

    all_results = search(user_query, num_results=num_urls)
    t1 = time.time()
    text_combined = []
    web_context = []
    for result in all_results:
        url = result
        base_domain = urlparse(url).netloc

        # Remove "www." prefix if it exists
        base_domain = re.sub(r"^www\.", "", base_domain)

        if base_domain in domains:
            # if domain in base_domain:
            # print(base_domain, url)

            text = fetch_webpage(result)
            # print(text)

            text = text.splitlines()
            text_combined.extend(text)

    for line in text_combined:
        if not any(excluded_phrase in line for excluded_phrase in exclude):
            if len(line.split()) > 8:
                web_context.append(line)

    top_sentences = rank_sentences(web_context)
    t2 = time.time()
    minutes, seconds = divmod(t2 - t1, 60)

    print(f"{minutes} minutes and {seconds} seconds")

    ans = "\n".join(sentence.strip() for sentence in top_sentences if sentence.strip())
    return ans


def fetch_content_for_url(url):
    try:
        # Extract base domain
        base_domain = urlparse(url).netloc
        base_domain = re.sub(r"^www\.", "", base_domain)

        # Check if domain is in the list of valid domains
        if base_domain in domains:
            print(f"Fetching content from: {url}")
            # Fetch the content of the webpage
            text = fetch_webpage(url)
            if text:
                text = text.splitlines()
                return text
            else:
                return []  # In case the text is empty
        else:
            return []  # If domain is not in the allowed list

    except Exception as e:
        print(f"Failed to fetch content from {url} due to: {str(e)}")
        return []  # Return empty list on failure


def get_web_content_parallelize(user_query, num_urls):
    all_results = search(user_query, num_results=num_urls)
    t1 = time.time()
    text_combined = []
    web_context = []

    # Use ThreadPoolExecutor to fetch content in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Fetch content for all URLs concurrently
        future_to_url = {
            executor.submit(fetch_content_for_url, result): result
            for result in all_results
        }

        for future in concurrent.futures.as_completed(future_to_url):
            try:
                result_text = future.result()  # Get the result of each completed future
                if result_text:
                    text_combined.extend(result_text)
            except Exception as e:
                print(f"Error processing result: {e}")

    for line in text_combined:
        if not any(excluded_phrase in line for excluded_phrase in exclude):
            if len(line.split()) > 8:
                web_context.append(line)

    top_sentences = rank_sentences(web_context)
    t2 = time.time()
    minutes, seconds = divmod(t2 - t1, 60)

    print(f"{minutes} minutes and {seconds} seconds")

    ans = "\n".join(sentence.strip() for sentence in top_sentences if sentence.strip())
    return ans
