from crawler.parser import Parser
from crawler.scraper import Scraper
from data_handler.file_handler import file_handler
from utils.logger import logger
from utils.settings import settings

if __name__ == "__main__":
    logger.info("Starting app")
    scraper = Scraper(region=settings.REGION)
    page_source = scraper.get_all_table_pages()
    equities_data = Parser.get_equities_data(page_source)
    file_handler.save_csv(data=equities_data)
