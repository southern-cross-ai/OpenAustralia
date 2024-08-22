import os

import requests
from bs4 import BeautifulSoup


def build_urls(min_page=1, max_page=55):
    post_urls = set()  # remove duplicate links each time when adding new links
    for page in range(min_page, max_page+1):
        # retrieve the page content
        page_url = f'https://www.openaustralia.org.au/comments/recent/?p={page}'
        page_response = requests.get(page_url)
        # parse the page to extract the post links
        soup = BeautifulSoup(page_response.content, 'html.parser')
        page_href_anchors = soup.find_all('a', string='Read comment')
        page_hrefs = [anchor.get('href') for anchor in page_href_anchors]
        # add all links together to post_urls
        for href in page_hrefs:
            post_url = ('https://www.openaustralia.org.au' + href).split('#')[0]
            post_urls.add(post_url)
    return list(post_urls)


def retrieve_content(post_urls, save_root):
    for post_url in post_urls:
        try:
            print(f"Retrieving from {post_url}")
            # retrieve the post content
            post_response = requests.get(post_url)
            # parse the post to extract the main post
            soup = BeautifulSoup(post_response.content, 'html.parser')
            name = post_url.split('/')[3] + '_' + post_url.split('=')[1] + '.html'
            path = os.path.join(save_root, name)
            with open(path, 'w') as f:
                f.write(f"<!--{post_url}-->\n")
                f.write(soup.prettify())
            print(f"Saved as {path}")
        except:
            print(f"Failed to retrieve from {post_url}")
            

if __name__ == '__main__':
    # last time updated on 22 Aug 2024
    post_urls = build_urls(min_page=1, max_page=55)
    save_root = '/Users/yifan/Documents/GitHub/datasets/Gale-Literature-Criticism/recent_comments'
    retrieve_content(post_urls, save_root)
    