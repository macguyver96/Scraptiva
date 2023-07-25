# Processor controls the overall logic of scraping.

import csv
import json
from src.SeleniumActions import *
from src.FirmListGenerator import generate_firm_list
import os


# Get the next several entries to process in the given firm list, the exact number of entries
# to process is specified in config. If some of the previously scraped entries have errors, add
# them to the process_list first.
def get_process_list():
    process_list = list()
    with open(config.firm_list_location, 'r') as firm_list:
        with open(config.scrape_status_location, 'r') as status_file:
            status_dict = json.loads(status_file.read())
        reader = csv.DictReader(firm_list)
        count = 0
        record = False

        next_entry = status_dict["next"]
        for entry in reader:
            if entry == next_entry:
                record = True
            if record and count <= config.entries_to_process:
                process_list.append(entry)
                count += 1
            else:
                status_dict["next"] = entry
                with open(config.scrape_status_location, 'w') as status_writer:
                    json.dump(status_dict, status_writer)
                break
    # potential risk: if "next" in scrape_status is updated but for some reason the returned process_list
    # is not processed nor recorded in the error_list, these entries are lost.
    return process_list


# initiate output file and scrape status file
def init_process():
    with open(config.firm_list_location, 'r') as firm_list:
        firm_list_reader = csv.DictReader(firm_list)
        with open(config.scrape_status_location, 'w+') as status_file:
            json.dump({"next": next(firm_list_reader), "error_list": []}, status_file)
        with open(config.output_location, 'w') as output_file:
            output_writer = csv.DictWriter(output_file, firm_list_reader.fieldnames)
            output_writer.writeheader()


# Start the scraping process. The workflow is as the following:
# for 0 : process_times:
#     try re-scrape entries that led to errors in last scrape for 5 times
#     if they all fail:
#         exit
#     process entries_to_process entries
def process():
    if not os.path.isfile(config.scrape_status_location):
        init_process()

    # login Factiva and only use one webdriver to increase speed
    # may result in a bug if login fails
    driver = webdriver.Chrome() #get_chrome_driver() as alternative
    driver.get('https://www.pollux-fid.de/login')
    sleep(5)
    driver.get('https://www.pollux-fid.de/factiva')
    sleep(5)

    for _ in range(config.process_times):

        # retrieve the error list and re-initiate the error list to be empty
        with open(config.scrape_status_location, 'r') as status_file:
            status_dict = json.loads(status_file.read())
            error_list = status_dict["error_list"]
            status_dict["error_list"] = []
        with open(config.scrape_status_location, 'w') as status_writer:
            json.dump(status_dict, status_writer)

        attempt_count = 0
        while error_list:
            print("--------Processing " + str(len(error_list)) + " unfinished entries from last scrape--------\n")
            generate_firm_list(error_list, driver)
            attempt_count += 1
            if attempt_count >= 5:
                driver.quit()
                print("The error entries in last scrape cannot be scraped.")
                return
        print("--------Processing " + str(config.entries_to_process) + " entries--------\n")
        generate_firm_list(get_process_list(), driver)
    driver.quit()

# TODO: add quit function so that we can quit the program in the middle of the run without damaging file status
