from scrapy import SuumoScrapyJob
from src.const import URL


def main():
    SuumoScrapyJob(URL)


if __name__ == '__main__':
    main()
