import asyncio
import aiohttp
import bs4
import os
import tqdm

 
@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('GET', *args, **kwargs)
    return (yield from response.read_and_close())


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


def img_urls(page):
    soup = bs4.BeautifulSoup(page)
    images = soup.findAll("img")
    image_urls = (image["src"] for image in images)
    image_urls = (image_url for image_url in image_urls if ('avatar' not in image_url and 'static' not in image_url and 'impixu' not in image_url))
    return image_urls


@asyncio.coroutine
def save_image_data(url, sem, output_folder='crawled_data/'):
    with (yield from sem):
        page = yield from get(url)

    destination = output_folder + url.split('//')[1].split('.')[0]
    try:
        os.mkdir(destination)
    except FileExistsError:
        pass

    for img_url in img_urls(page):
        name = img_url.split('/')[-1]
        img = yield from get(img_url)
        f = open(destination+'/'+name, 'wb')
        f.write(img)
        f.close()


def main():
    websites = (website.split(',') for website in open('scraper.cfg') if website[0] != '#')

    websites = ((website[0], int(website[1]), int(website[2])) for website in websites)
    url_sets = ((website[0]+'page/'+str(i) for i in range(website[1], website[2]+1)) for website in websites)
    urls = (url for url_set in url_sets for url in url_set)
    sem = asyncio.Semaphore(50)
    loop = asyncio.get_event_loop()
    try:
        coros = [save_image_data(url, sem) for url in urls]
        print('Pages Crawled : ')
        loop.run_until_complete(wait_with_progress(coros))
    except IndexError:
        print("Configuration error !")
        return

if __name__ == '__main__':
    main()