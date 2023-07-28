# This project is developed on Python 3.7 with additional packages Selenium and BeautifulSoup. It also
# requires a chrome webdriver which is obtainable on Selenium website.

search_criteria = {
    'time': {  # from mm/dd/yyyy to mm/dd/yyyy
        'frm': 4,
        'frd': 1,
        'fry': 2022,
        'tom': 4,
        'tod': 21,
        'toy': 2022
    },
    'sources': ['Süddeutsche Zeitung'],
    'subjects': ['Commentaries/Opinions'],
    'language': ['German']
}

# let selenium driver wait for so long before reporting bug (in what unit?)
implicit_wait_time = 100

# web driver location used by selenium
chrome_webdriver_location = 'C:/Users/ferdi/OneDriveTUM/Privat/9_Code/Scraptiva'

# location of firm_list csv file to be scraped
# example of proper formatting:
"""
gvkey,cik,conm,Role,Source,Date,Time,Title,Content
1004,1750,AAR CORP,"CEO, Chief Executive Officer",,,,,
1004,1750,AAR CORP,"CFO, Chief Financial Officer",,,,,
"""
firm_list_location = "C:/Users/ferdi/OneDriveTUM/Privat/9_Code/Scraptiva/short_firmlist.csv"

# location of scraping output
output_location = "/Users/luyuxuan/Desktop/scrape/Scraptiva/test_result.csv"

# location of scrape_status.json. This should be an auto-generated file that keeps track of how much
# work it has done, so that it can "pick up where it left". If this is a location of an existing file,
# this file will be truncated.
scrape_status_location = "C:/Users/ferdi/OneDriveTUM/Privat/9_Code/Scraptiva/scrape_status.json"

# the number of entries in firm_list to process in each try
entries_to_process = 2

# how many cycles we process in each run. The number of companies being scraped each
# run is process_time * entries_to_process. Why do we need two separate counters? That's because
# if the previous cycle results in some error due to network issue, we will rerun it until it
# succeed before processing the next cycle (ie. the next set of entries). If the error is not
# resolved after 5 consecutive tries, quit the program.
process_times = 1

# turn this to true to disable browser window when scraping.
headless = False

# program entry point
if __name__ == "__main__":
    from src.Processor import process
    process()
