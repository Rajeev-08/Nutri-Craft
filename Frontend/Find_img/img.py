import requests
from bs4 import BeautifulSoup

Not_found_link = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASsAAACoCAMAAACPKThEAAAA...'

def get_images_links(searchTerm):
    try:
        searchUrl = f"https://www.google.com/search?q={searchTerm}&site=webhp&tbm=isch"
        d = requests.get(searchUrl, headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(d, 'html.parser')

        img_tags = soup.find_all('img')

        imgs_urls = []
        for img in img_tags:
            if img['src'].startswith("http"):
                imgs_urls.append(img['src'])

        return imgs_urls[0] if imgs_urls else Not_found_link
    except Exception as e:
        return Not_found_link
