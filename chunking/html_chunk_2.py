import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Fetch and parse the HTML content
url = 'https://en.wikipedia.org/wiki/Email_marketing'  # Replace with the URL of the page you want to scrape
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Step 2: Extract headers
headers = []
for level in range(1, 7):
    header_tag = f'h{level}'
    for header in soup.find_all(header_tag):
        headers.append((header_tag, header.get_text(strip=True)))

# Step 3: Initialize a directed graph
G = nx.DiGraph()

# Step 4: Add nodes and establish relationships
previous_headers = {f'h{level}': None for level in range(1, 7)}

for tag, text in headers:
    G.add_node(text, level=tag)
    level = int(tag[1])
    if level > 1:
        parent_level = level - 1
        # Find the most recent header of the parent level
        while parent_level > 0:
            if previous_headers[f'h{parent_level}'] is not None:
                G.add_edge(previous_headers[f'h{parent_level}'], text)
                break
            parent_level -= 1
    previous_headers[tag] = text

# Step 5: Visualize the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_color='black', font_weight='bold')
plt.show()

# Optional: Print the graph nodes and edges
print("Nodes:", G.nodes(data=True))
print("Edges:", G.edges())
