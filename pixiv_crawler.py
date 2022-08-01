import logging
import requests
from bs4 import BeautifulSoup as BS
import json
import time
import pathlib as pl

# Set the outputs of log and terminal
fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
level = logging.INFO

formatter = logging.Formatter(fmt, datefmt)
logger = logging.getLogger()
logger.setLevel(level)

file = logging.FileHandler("./pixiv_crawler.log", encoding='utf-8')
file.setLevel(level)
file.setFormatter(formatter)
logger.addHandler(file)

console = logging.StreamHandler()
console.setLevel(level)
console.setFormatter(formatter)
logger.addHandler(console)

class PixivCrawler:
    def __init__(self):
        """
        Initialize the crawler settings

        :return:
        """
        with open("pixiv_settings.json", "r", encoding="utf8") as f:
            self.settings = json.load(f)    # Load settings
        logger.info("Settings loaded")

    def sleep(self, sleep_key: str, delta=0):
        """
        Execute sleeping for a time configured in the settings

        :param sleep_key: the sleep time label
        :param delta: added to the sleep time
        :return:
        """
        _t = self.settings["config"][sleep_key] + delta
        logger.info(f"Sleep {_t} second(s)")
        time.sleep(_t)
        
    def get_pid_lists_by_uid(self, uid: int) -> list:
        """
        Get the user's all works by user id

        :param uid: user id
        :return: pid lists of the user
        """
        # Send request
        url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=zh"
        resp = requests.get(url, headers=self.settings["headers"], proxies=self.settings["proxies"])

        # Get pid lists of all works
        pid_lists = []
        soup = BS(resp.text, 'lxml').get_text()
        soup = json.loads(soup)
        pid_dicts = soup["body"]["illusts"]
        for key in pid_dicts.keys():
            pid_lists.append(key)
        return pid_lists

    def get_links_by_pid(self, pid) -> list:
        """
        Get the download links of works by pid

        :param pid: pid of the works
        :return:
        """
        # Send request
        url = f"https://www.pixiv.net/ajax/illust/{pid}/pages?lang=zh"
        resp = requests.get(url, headers=self.settings["headers"], proxies=self.settings["proxies"])

        # Get download links
        links = []
        soup = BS(resp.text, 'lxml').get_text()
        soup = json.loads(soup)
        works = soup["body"]
        for work in works:
            links.append(work["urls"]["original"])
        return links
        
    def download(self, url: str, filename: str):
        """
        Download the image by url

        :param url: url of the image
        :return:
        """
        resp = requests.get(url, headers=self.settings["headers"], proxies=self.settings["proxies"])
        with open(filename, "wb") as f:
            f.write(resp.content)
        logger.info(f"Download {url.split('/')[-1]}")

    def download_all_works_by_uid(self, uid: int):
        """
        Download all works by user id

        :param uid: user id
        :return:
        """
        # Get the user's name
        resp = requests.get(f"https://www.pixiv.net/ajax/user/{uid}/profile/top?lang=zh", headers=self.settings["headers"], proxies=self.settings["proxies"])
        soup = BS(resp.text, 'lxml').get_text()
        soup = json.loads(soup)
        name = soup["body"]["extraData"]["meta"]["ogp"]["title"]
        
        # Make directory
        dir = pl.Path() / f"pixiv_illusions/{name}"
        if not dir.exists():
            dir.mkdir(parents=True)
            logger.info(f"Make directory {dir}")
        else:
            logger.info(f"Directory {dir} already exists")

        # Save all download links of works of the user
        links = []

        # Get all download links
        pid_lists = self.get_pid_lists_by_uid(uid)
        for pid in pid_lists:
            links += self.get_links_by_pid(pid)
            logger.info(f"Get {len(links)} links as of pid {pid}")

        # Download all works by the links
        for link in links:
            try:
                self.download(link, f"{dir}/{link.split('/')[-1]}")
            except Exception as e:
                logger.error(f"Error: {e}")
                continue
            self.sleep("interval_between_download")

if __name__ == "__main__":
    p = PixivCrawler()
    for uid in p.settings["uid"]:
        p.download_all_works_by_uid(uid)
        logger.info(f"Download all works of user {uid}")
        p.sleep("interval_between_user")
    logger.info("All works downloaded")
