I have created a crawler.py to scrape the website https://franchisesuppliernetwork.com/. Due to the strong security measures of this website, I used an advanced version of the Python requests library called "curl_cffi."

Approach:
It is easy to get and crawl all pages of any website from its sitemap. For this website the sitemap URLs are nested as follows: 
sitemap -> some URLs, sitemap -> some URLs, sitemap -> URLs. 
To address this problem and dynamically crawl each web page, I used a Depth-First Search (DFS) data structure algorithm in my code.

There are two major functions in the code:


Function (1) - Crawl and Download Data
-> Using DFS, the crawler will crawl all the pages. There is a parameter in the class's __init__ function called "self.max_pages_limit_crawl". If we want to crawl a limited number of pages from the website, we can set a specific number for the maximum pages to be crawled. If you want to crawl the entire website and all its pages, set this parameter to False.

-> As we are extracting data from a web page, it contains text, reference URLs, images, and other various types of data. There is a toggle parameter to choose what to download and what not to download. Set it to True or False.
Note: Changing the toggle parameters can affect the analyzing function, which is executed after downloading all the data.

-> All the data will be saved in the present directory as a file database structure. A folder called "Downloaded_data" will be automatically created, containing all the downloaded data.

Within that folder, a subfolder will be created for each URL page. For example:
URL: https://franchisesuppliernetwork.com/2023-marketing-trends/
Folder name: 2023-marketing-trends

-> This folder will contain two files and one folder:

text_file.txt (downloaded text data)
reference_urls.json (a list of reference URLs present on the webpage)
images (a folder containing all images downloaded from the webpage)


Function (2) analyze Downloaded Data:
-> After downloading all the data, the "analyse_data" function will be called to check and analyze all the folders and files in "Downloaded_data".
-> After successfully analyzing the data, it will create a JSON file called "Analysed_stats.json," where you can see the statistics of all downloaded data. You can easily map the folder names and URLs using this JSON file and the corresponding folders inside the "Downloaded_data" directory.



all the required python libraries are in requirements.txt
to install 
use command - "pip install -r requirements. txt" in your present Directory terminal

Or you can manaully install required libraries using below commands in terminal
pip install beautifulsoup4==4.12.3
pip install cffi==1.16.0
pip install curl_cffi==0.6.2 


