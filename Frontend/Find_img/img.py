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
        print(f"Error: {e}")
        return Not_found_link

# Test
search_term = "apple"
image_link = get_images_links(search_term)
print(f"Image URL for '{search_term}': {image_link}")
#out: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaN1Cr1SuDUeoTSVHDIwMvhi26ZGOOTd9jWmvXUl34sSTG35CX_w5JsZWTCng&s