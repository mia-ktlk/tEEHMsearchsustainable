import threading
import threading
import time
from abc import ABC, abstractmethod
from typing import List

from attr import asdict
from attr import attrs as attrs
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@attrs(auto_attribs=True)
class ItemEntry:
    """
    Class to represent a single item entry in the database
    """

    name: str
    img_src: str
    search_terms: str
    brand: str
    price: str
    rating: float
    date_stored: float
    url: str
    vendor: str


class Spyder(ABC):
    """
    Abstract base class for all the different Spyders to be built for different
    websites.
    """

    browser: WebDriver
    url: str

    def __init__(self, url: str):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.url = url

    @abstractmethod
    def search_item(self, search_name: str, num_items: int) -> List[ItemEntry]:
        pass

    def format_price(self, price_str: str) -> str:
        return format(float(price_str.strip().replace("$", "")), ".2f")

    def handle_img(self, img_src: str, need_url: bool = False) -> str:
        if img_src:
            if need_url:
                return self.url + img_src
            return img_src
        else:
            return "https://raw.githubusercontent.com/mia-ktlk/hbp2021process/main/img/default.jpg"



class UncommonGoodsSpyder(Spyder):
    """
    Spyder for getting items from https://www.uncommongoods.com
    """

    def __init__(self):
        super().__init__("https://www.uncommongoods.com")

    def search_item(self, search_name: str, num_items: int) -> List[ItemEntry]:
        query = search_name.replace(" ", "%20")
        self.browser.get(f"{self.url}/search?q={query}")
        tree = html.fromstring(self.browser.page_source)

        item_names = tree.xpath('//span[@itemprop="name"]/text()')[:num_items]
        item_imgs = tree.xpath('//img[@itemprop="image"]')[:num_items]
        item_prices = tree.xpath('//span[@itemprop="offers"]/text()')[:num_items]
        # call .attrib["content"] on item_rating
        item_ratings = tree.xpath('//meta[@itemprop="ratingValue"]')[:num_items]
        # call .attrib["href"] on item_url
        item_urls = tree.xpath('//a[@class="a-secondary"]')[:num_items]
        item_brand = "Uncommon Goods"
        item_vendor = "Uncommon Goods"

        items = []
        findable = min(
            num_items,
            *map(len, [item_names, item_imgs, item_prices, item_ratings, item_urls]),
        )
        for i in range(findable):
            items.append(
                ItemEntry(
                    name=item_names[i],
                    img_src=self.handle_img(item_imgs[i].attrib["src"], need_url=True),
                    search_terms=search_name,
                    brand=item_brand,
                    price=self.format_price(item_prices[i]),
                    rating=float(item_ratings[i].attrib["content"]),
                    date_stored=time.time(),
                    url=self.url + item_urls[i].attrib["href"],
                    vendor=item_vendor,
                )
            )

        return items

    def format_price(self, price_str):
        return super().format_price(price_str.split()[0])


class GroveCollaborativeSpyder(Spyder):
    """
    Spyder for getting items from https://www.grove.co
    """

    def __init__(self):
        super().__init__("https://www.grove.co")

    def search_item(self, search_name: str, num_items: int) -> List[ItemEntry]:
        query = search_name.replace(" ", "%20")
        self.browser.get(f"{self.url}/catalog/?q={query}")
        try:
            WebDriverWait(self.browser, 4).until(EC.title_contains("Results"))
        except TimeoutError:
            return []
        tree = html.fromstring(self.browser.page_source)

        item_names = tree.xpath(
            '//div[@class="ProductTileMedium_ProductTitle"]/text()'
        )[:num_items]
        item_imgs = tree.xpath('//div[@class="ProductTileMedium_ImageContainer"]/img')[
            :num_items
        ]
        # strip price
        item_prices = tree.xpath('//div[@data-test-id="ptm-price"]/text()')[::2][
            :num_items
        ]
        # call self.parse_rating(item_rating.attrib["aria-label"])
        item_ratings = tree.xpath('//div[@data-test-id="ptm-rating"]/svg')[:num_items]
        item_urls = tree.xpath('//meta[@itemprop="url"]')[:num_items]
        # strip
        item_brands = tree.xpath(
            '//div[@class="ProductTileMedium_ProductTitle section-heading-small"]/text()'
        )[:num_items]
        item_vendor = "Grove Co."

        items = []
        findable = min(
            num_items,
            *map(
                len,
                [
                    item_names,
                    item_imgs,
                    item_prices,
                    item_ratings,
                    item_urls,
                    item_brands,
                ],
            ),
        )
        for i in range(findable):
            items.append(
                ItemEntry(
                    name=item_names[i].strip(),
                    img_src=self.handle_img(item_imgs[i].attrib["src"]),
                    search_terms=search_name,
                    brand=item_brands[i].strip(),
                    price=self.format_price(item_prices[i]),
                    rating=self._parse_rating(item_ratings[i].attrib["aria-label"]),
                    date_stored=time.time(),
                    url=item_urls[i].attrib["content"],
                    vendor=item_vendor,
                )
            )

        return items

    def _parse_rating(self, rating: str) -> float:
        """
        Helper func to parse float rating from string structured as 'Rated x out of y stars'
        """
        return float(rating.split()[1])


class PackageFreeSpyder(Spyder):
    """
    Spyder for getting items from https://packagefreeshop.com
    """

    def __init__(self):
        super().__init__("https://packagefreeshop.com")

    def search_item(self, search_name: str, num_items: int) -> List[ItemEntry]:
        query = search_name.replace(" ", "+")
        self.browser.get(f"{self.url}/search?q={query}")
        tree = html.fromstring(self.browser.page_source)

        elems = tree.xpath('//div[@data-domain="{{itemDomain}}"]')[:num_items]
        attribs = [e.attrib for e in elems]
        item_names = [att["data-name"] for att in attribs]
        item_imgs = [att["data-image-url"] for att in attribs]
        price_wrappers = tree.xpath('//p[@class="price_wrapper"]')[:num_items]
        item_prices = [
            pw.xpath('.//span[@class="money"]/text()')[0] for pw in price_wrappers
        ]
        # dealing with if an item is sold out
        item_soldout = [bool(pw.xpath(".//em/text()")) for pw in price_wrappers]
        item_soldout_index = [item_soldout.index(b) for b in item_soldout if b]
        # v call float(item_rating.split()[0])
        item_ratings = tree.xpath('//span[@class="sr-only"]/text()')
        item_urls = [self.url + att["data-url"] for att in attribs][:num_items]
        item_brand = ""
        item_vendor = "Package Free"

        items = []
        findable = min(
            num_items,
            *map(len, [item_names, item_imgs, item_prices, item_ratings, item_urls]),
        )
        for i in range(findable):
            if i in item_soldout_index:
                continue
            items.append(
                ItemEntry(
                    name=item_names[i],
                    img_src=self.handle_img(item_imgs[i]),
                    search_terms=search_name,
                    brand=item_brand,
                    price=self.format_price(item_prices[i]),
                    rating=self._parse_rating(item_ratings[i]),
                    date_stored=time.time(),
                    url=item_urls[i],
                    vendor=item_vendor,
                )
            )

        return items

    def _parse_rating(self, rating: str) -> float:
        return float(rating.split()[0])


class SpyderWeb:
    """
    All collection of spyders to run and search on

    :cvar spyders:
        List of Spyders to use when scraping
    :cvar spyders_finished:
        List of booleans for if a spyder has finished it's task. Used when running
        multiple spyders at once, a Spyder will update it's index boolean to True once
        it has completed.
    :cvar item_list:
        List of ItemEntry's to be added to as Spyders crawl.
    """

    spyders: List[Spyder]
    spyders_finished: List[bool]
    item_list: List[ItemEntry]

    def __init__(self):
        self.spyders = [
            UncommonGoodsSpyder(),
            GroveCollaborativeSpyder(),
            PackageFreeSpyder(),
        ]
        self.spyders_finished = [False for _ in self.spyders]
        self.item_list = []

    def search(self, search_term: str, num_results: int) -> List[ItemEntry]:
        index = 0
        for spyder in self.spyders:
            spy_thread = threading.Thread(
                target=self.run_spyder_search,
                args=(
                    spyder,
                    index,
                    search_term,
                    num_results,
                ),
            )
            spy_thread.start()
            index += 1

        while not all(self.spyders_finished):
            pass

        items = self.item_list
        self.item_list = []
        self.spyders_finished = [False for _ in self.spyders]
        print("\n".join([str(asdict(item)) for item in items]))
        return items

    def run_spyder_search(
        self, spyder: Spyder, index: int, search_term: str, num_results: int
    ) -> None:
        items = spyder.search_item(search_term, num_results)
        for i in items:
            self.item_list.append(i)
        self.spyders_finished[index] = True


if __name__ == "__main__":
    print("starting web!")

    web = SpyderWeb()

    while True:
        name = input(">>  ")
        if name.lower() in ["exit", "quit", "exit()"]:
            break
        web.search(name, 3)
