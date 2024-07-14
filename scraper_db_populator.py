import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin

load_dotenv()


embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")


pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "product-index"

# create Pinecone index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # OpenAI embeddings dimension
        metric="cosine",
        spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
    )

pinecone_index = pc.Index(index_name)



def scrape_product_page(url):
    """Scrapes text from specified classes at the given URL."""
    target_classes = ["mb-4", "qna__question js-qnaResponse"]
    combined_text = []
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for class_name in target_classes:
            elements = soup.find_all(class_=class_name)
            for element in elements:
                combined_text.append(element.get_text(strip=True))
        return ' '.join(combined_text)
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def search_context(query, k=3):
    """Retrieve relevant context from Pinecone based on the query."""
    query_embedding = embeddings.embed_query(query)
    context_response = pinecone_index.query(query_embedding, top_k=k, include_metadata=True)
    contexts = [match['metadata']['text'] for match in context_response['matches']]
    return " ".join(contexts)

def to_json(input_string):
    """Creates a JSON-structured string with a single field named 'text'."""
    return json.dumps({"text": input_string}, indent=4)



def url_to_json(url):
    """Combines scraping and JSON conversion for a single product URL."""
    raw_data = scrape_product_page(url)
    return to_json(raw_data)




def get_product_links(base_url, recursion_depth_level):
    """Retrieves product links from a category page."""
    print(f"Sourcing product links from category: {base_url}")

    parsed_url = urlparse(base_url)
    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    category_segment = parsed_url.path.split('/')[-1]
    category_keyword = category_segment.replace("-Parts.htm", "") + "-"

    product_links = set()
    visited_links = set()
    def make_absolute(href):
        return urljoin(base_domain, href)
    def is_valid_url(url):
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme) and bool(parsed.netloc)
        except ValueError:
            return False
    def scrape_links(url, current_depth):
        if current_depth > recursion_depth_level or url in visited_links or not is_valid_url(url):
            return

        visited_links.add(url)
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']
            absolute_href = make_absolute(href)
            
            if is_valid_url(absolute_href):
                if "SourceCode=18" in href:
                    product_links.add(absolute_href)
                    
                elif category_keyword in href and "SourceCode=18" not in href and absolute_href not in visited_links:
                    scrape_links(absolute_href, current_depth + 1)

        print(f"Current product links count: {len(product_links)}")
        time.sleep(2)  # delay to avoid rate limiting

    scrape_links(base_url, 0)
    return product_links




def create_product_database(base_url, recursion_depth):
    """Creates a database of product information from a category URL."""
    data = []
    urls = get_product_links(base_url, recursion_depth)
    print(urls)

    print("Creating dataset from product links...")

    for url in urls:
        print(url)
        json_obj = url_to_json(url)
        data.append(json.loads(json_obj))
        print("Created JSON for product")
    
    print("Successfully created dataset from category URL.")
    return data




def populate_pinecone():
    category_base_url_fridge = "https://www.partselect.com/Refrigerator-Parts.htm"
    product_data_fridge = create_product_database(category_base_url_fridge, 0)

    print("Populating Pinecone with fridge product data...")
    for i, item in enumerate(product_data_fridge):
        vector = embeddings.embed_query(item['text'])
        pinecone_index.upsert(vectors=[(f"product_{i}", vector, {"text": item['text']})])

    category_base_url_dw = "https://www.partselect.com/Dishwasher-Parts.htm"
    product_data_dw = create_product_database(category_base_url_dw, 0)

    print("Populating Pinecone with dishwasher product data...")
    for i, item in enumerate(product_data_dw):
        vector = embeddings.embed_query(item['text'])
        pinecone_index.upsert(vectors=[(f"product_{i}", vector, {"text": item['text']})])

    print(f"Successfully added {len(product_data_fridge + product_data_dw)} documents to Pinecone.")





if __name__ == '__main__':
    populate_pinecone()







