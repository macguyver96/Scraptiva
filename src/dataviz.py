import seaborn as sns
import matplotlib.pyplot as plt

#soup = BeautifulSoup(page, 'html.parser')
#article_container = soup.find("div", {"class": "article deArticle"})
#header = article_container.findAll("div", {"class": None})

#pd.read_csv('processed_articles2.csv').info()

with open('page_file.txt', encoding="utf8") as f:
    page_files = f.readlines()

# opening the file in read mode
file = open("page_file.txt", "r", encoding="utf8")

# reading the file
data = file.read()

# replacing end splitting the text
# when newline ('\n') is seen.
page_files = data.split("\n")
file.close()

# Get CSV files list from a folder
path = 'sz/articles'
csv_files = glob.glob(path + "/*.csv")

# Read each CSV file into DataFrame
# This creates a list of dataframes
df_list = (pd.read_csv(file) for file in csv_files)

# Concatenate all DataFrames
big_df = pd.concat(df_list, ignore_index=True)
big_df['Date'] = big_df['Date'].astype('datetime64[ns]')


sns.histplot(big_df.query("Date < '2023-01-01'"), x='Date', binwidth=3, bins=30)
plt.xticks(rotation=30)
plt.show()