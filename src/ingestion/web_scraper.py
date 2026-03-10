import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pg_essays(output_dir="src/ingestion/dataset/"):
    # Paul Graham Articles Website. This contains a list of links, where each link is an essay in mostly text format, there are fonts though!
    base_url = "https://paulgraham.com/articles.html"
    root_url = "https://paulgraham.com/"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Fetch the main articles page
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all links to essays
    links = soup.find_all('a')
    
    for link in links:
        href = link.get('href')
        title = link.text.strip()
        
        # Filter for essay links. Specifically in html format. Seems that each essay is a path from the root_url.
        if href and href.endswith('.html') and href not in ['index.html', 'articles.html', 'rss.html']:
            essay_url = urljoin(root_url, href)
            
            try:
                # Fetching each individual essay page
                essay_res = requests.get(essay_url)
                essay_soup = BeautifulSoup(essay_res.content, "html.parser")
                
                # The essay content is inside the font html block, which is unique throughout.
                font_tag = essay_soup.find('font')
                if font_tag:
                    content = font_tag.get_text(separator="\n")
                    
                    # Save each essay to a folder
                    filename = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).rstrip()
                    filename = f"{filename}.txt"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"Title: {title}\nURL: {essay_url}\n\n")
                        f.write(content)
                    
                    print(f"Downloaded: {title}")
                
            except Exception as e:
                print(f"Failed to download {title}: {e}")

if __name__ == "__main__":
    download_pg_essays()
