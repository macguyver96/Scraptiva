from src.SeleniumActions import *
from src.ContentFinder import *
from bs4 import BeautifulSoup
from bs4 import element
from selenium.webdriver.common.by import By






search_criteria = {
    'time': {  # from mm/dd/yyyy to mm/dd/yyyy
        'frm': 1,
        'frd': 1,
        'fry': 2020,
        'tom': 12,
        'tod': 31,
        'toy': 2022
    },
    'sources': ['Süddeutsche Zeitung'],
    'subjects': ['Commentaries/Opinions', 'Columns', 'Editorials'],
    'sub_exclude': ['Letters', 'Content', 'Interviews',  'Images', 'Transcripts', 'Surveys/Polls', 'Statistics', 'Advertorials/Sponsored Content'],
    'language': ['German']
}

chrome_webdriver_location = r"C:\Users\ferdi\OneDriveTUM\Privat\9_Code\Scraptiva\chromedriver.exe"






# WARNING: known source of bug. The article pages on Factiva has slightly different formats, which
#          is why this method may results in exception.
# html: a string that stores the page source code
# return: a dictionary of content information about the article, in the form
#       {Date: --, Time: --, Title: --, Source: --, Content: --}, paragraphs are separated using ' | '
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    article_container = soup.find("div", {"class": "article deArticle"})
    header = article_container.findAll("div", {"class": None})
    # print(header)

    article_info = dict()
    article_info["Title"] = header[0].find("span").string
    article_info["Length"] = header[1].string
    article_info["Date"] = header[2].string
    article_info["Time"] = header[3].string if isinstance(header[3], element.Tag) else header[3]
    article_info["Source"] = header[4].string
    content = list(paragraph.getText()
                   for paragraph in
                   article_container.findAll("p", {"class": "articleParagraph dearticleParagraph"}))
    article_info["Content"] = content #" | ".join(content)
    if soup.find("div", {"class": "author"}):
        article_info["Author"] = soup.find("div", {"class": "author"}).string
    else:
        article_info["Author"] = None

    return article_info

# html: the html page of search result
# links: the links for articles in the form of a list
# Return null if no articles found
def get_article_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    entries = soup.findAll('tr', {'class': 'headline'})
    for entry in entries:
        links.append(entry.find_all('td')[2].find('a')['href'].replace('..', 'https://global-1factiva-1com-1h89pp8pl02e3.proxy.fid-lizenzen.de/'))
    return links

def get_article_pages(driver):
    print("Lets go")
    links = []
    n = 1
    while(n):
        links.append(get_article_links(driver.page_source))
        print("\tPage ", n, " done. ", len([item for items in links for item in items]) )
        sleep(3)
        try:
            driver.find_element(By.CLASS_NAME, "nextItem").click()
            n += 1
            sleep(2)
        except:
            print("Last page reached!")
            n = 0

    links = [item for items in links for item in items]
    max = driver.find_element(By.CLASS_NAME, "resultsBar").text[-3:]
    print("All links received. ", len(links), " / ", max)

    pd.DataFrame(article_pages).to_csv('all_my_links1.csv', index=False, mode='x')
    print("All links saved to csv.")

    result = []
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i in range(0, len(links)):
        #print("\tProcessing article " + str(i + 1) + " of total " + str(len(links)))
        driver.get(links[i])
        sleep(5)
        result.append(driver.page_source)
        printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
        # Factiva blocks you out if you search for articles too quickly
        sleep(3)
    return result



# program entry point
if __name__ == "__main__":

    pollux_mail = "ferdi.baune@tum.de"
    pollux_pass = "Awaken-Syndrome6-Hyperlink"

    driver = webdriver.Chrome(chrome_webdriver_location)
    driver.get('https://www.pollux-fid.de/login')

    email = driver.find_element(By.ID, "emailId")
    email.click()

    email.clear()
    email.send_keys(pollux_mail)

    password = driver.find_element(By.ID, "current-password")
    password.click()
    password.send_keys(pollux_pass)

    login = driver.find_element(By.ID, "submit")
    login.click()

    sleep(3)
    driver.get('https://www.pollux-fid.de/factiva')
    sleep(5)

    search = driver.find_element(By.XPATH, '//*[@id="navmbm0"]/a')
    search.click()
    sleep(3)

    enter_search_criteria(driver)

    driver.find_element(By.ID, "btnSearchBottom").click()

    sleep(5)

    # Get HTML of all articles.
    article_pages = get_article_pages(driver)
    pd.DataFrame(article_pages).to_csv('all_my_links1.csv', index=False, mode='x')

    print("-------- Articles Received --------")

    # Extract information from HTML.
    article_info = []
    n = 0
    for page in article_pages:
        article_info.append(get_content(page))
        print("Article Number ", n, " processed.")
        n += 1
    print("-------- Articles Processed --------")

    # Save the data to a csv file.
    data = pd.DataFrame(article_info)
    data.to_csv('processed_articles2.csv', index=False, mode='x')

    print("-------- Data Saved --------")




#soup = BeautifulSoup(page, 'html.parser')
#article_container = soup.find("div", {"class": "article deArticle"})
#header = article_container.findAll("div", {"class": None})

#pd.read_csv('processed_articles2.csv').info()

