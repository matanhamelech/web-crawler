"""search for urls and save their html content to files asynchronously"""
import asyncio
import aiohttp
import constants
from bs4 import BeautifulSoup


async def fetch(session, url):
    """
    fetch html format of a website asynchronously
    :param session: the session to use for getting html
    :param url: the url of the site
    :return: html format of the website
    """
    async with session.get(url) as response:
        html = await response.text()
        return html


async def fetch_all(urls):
    """
    fetch html formats of websites asynchronously
    :param urls: urls of websites
    :return: list of html formats of the websites
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url))
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses


def main(url: list) -> None:
    """
    start a web crawler with a url given
    :param url: url of the website
    """
    WebCrawler(url)


def WebCrawler(urls: list) -> None:
    """
    asynchronously and recursively save html content of websites to files and find other urls
    :param urls: list of the urls of website to crawl in
    """
    constants.urls_to_check = []
    pages = asyncio.run(fetch_all(urls))
    for i in range(len(pages)):
        page = pages[i]
        SaveWebsite(page, urls[i])
        try:
            page_urls = SearchUrls(page)
            for url in page_urls:
                if CheckUrl(url):
                    constants.urls.append(url)
                    constants.urls_to_check.append(url)
        except:
            pass
    constants.recurse_number += 1
    print("second turn")
    if (constants.recurse_number < 2):
        WebCrawler(constants.urls_to_check)


def SaveWebsite(content: str, url: str) -> None:
    """
    save html content to a file
    :param content: the content of the website
    :param url: the url of the website( for the file name)
    """
    file_name = '__'.join(url.split('/')[2:])
    with open(file_name, "w") as file:
        file.write(content)


def SearchUrls(text: str) -> list:
    """
    search for urls in html content
    :param text: the html content
    :return: list of url in the html content
    """
    soup = BeautifulSoup(text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        content = link.get('href')
        if (content is not None and (
                content[0:8] == "https://" or content[0:7] == "http://")):
            urls.append(content)
            print('"' + content + '"' + ",")
    return urls


def CheckUrl(url: str) -> bool:
    """
    check if url has been searched yet
    :param url: the url to check
    :return: boolean value indicating if the url has been searched or not.
    """
    if url not in constants.urls:
        return True
    return False


if __name__ == "__main__":
    main(["http://www.python.org"])
