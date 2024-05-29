import json
import os.path
from bs4 import BeautifulSoup
from curl_cffi import requests
import re

class Crawler:
    def __init__(self):
        self.source_url = "https://franchisesuppliernetwork.com/"
        self.sitemap_url = "https://franchisesuppliernetwork.com/sitemap.xml"

        self.max_pages_limit_crawl = 10  # if you want to crawl limited pages set max page count here
        # else if you want to crawl full website set this parameter to False
        self.page_start_count = 1

        #this can be used for analytical purpose set according to your preference
        self.download_text = True #if you don't want to download text information set this parameter to False
        self.download_images = True #if you don't want to download images set this parameter to False
        self.get_json_of_reference_urls = True #if you don't want to Get reference urls from details page set this parameter to False

        if not os.path.exists("Downloaded_data"):
            os.mkdir("Downloaded_data")

    def crawl(self,url):
        req = requests.get(url=url)      #req is Request Object
        print("Crawling URl - ",url)
        if req.status_code == 200:       # sending Request to url
            more_sitemap_urls = re.findall("""<loc>(.*?)</loc>""",req.text) #regex to find Nested sitemap urls from sitemap
            if more_sitemap_urls:         # DFS logic to check if any other sitemap urls found at deeper level
                for more_sitemap_url in more_sitemap_urls:
                    self.crawl(more_sitemap_url) # if found then calling back the same Crawl function to crawl Nested sitemap urls
            else:
                self.parse_page(req) # if not then sending the Response to be parsed and extract meaningful information.

                #logic to crawl limited pages from website
                if self.max_pages_limit_crawl:
                    if self.page_start_count == self.max_pages_limit_crawl:
                        obj.analyse_data()
                        exit()
                    else:
                        self.page_start_count += 1
        else:
            raise Exception(f"Response Code - {req.status_code} found for URL - {req.url}. Requests May be blocked. Please Use Proxy or Check your Code.")

    def parse_page(self,req):
        print("Parsing Page - ",req.url)
        response = BeautifulSoup(req.text, features='lxml') #parse response object using BeautifulSoup
        folder_name = req.url.replace("https://franchisesuppliernetwork.com",'').replace('/','_').strip("_") #making Folder name from URL

        if self.download_text:
            #saving texts information in folder name as per url
            if not os.path.exists(fr"Downloaded_data/{folder_name}"):
                os.mkdir(fr"Downloaded_data/{folder_name}")
            with open(fr"Downloaded_data/{folder_name}/text_file.txt","w") as f:
                f.write(f"url = {req.url}"+'\n'+'\n'+response.find('body').get_text())
                print("Text Data Downloaded")

        if self.download_images:
            #Downloading Images Present on web Page
            if not os.path.exists(fr"Downloaded_data/{folder_name}/images"):
                os.mkdir(fr"Downloaded_data/{folder_name}/images")
            images = response.find('body').findAll('img')
            for image in images:
                image_response = requests.get(image.get('src'))
                with open(fr"Downloaded_data/{folder_name}/images/{image_response.url.split('/')[-1]}","w") as f:
                    f.write(f"url = {req.url}"+'\n'+'\n'+response.find('body').get_text())
                    print("Image Downloaded")

        if self.get_json_of_reference_urls:
            # Getting json file of reference urls for analytical purpose.
            reference_urls_list = [x.get('href') for x in response.find('body').findAll('a')]
            if not os.path.exists(fr"Downloaded_data/{folder_name}"):
                os.mkdir(fr"Downloaded_data/{folder_name}")
            with open(fr"Downloaded_data/{folder_name}/reference_urls.json", "w") as f:
                f.write(json.dumps(reference_urls_list))
                print("Reference urls Json Downloaded")

        print("\n")


    def analyse_data(self):
        print("\n"+"Analysing Data.......\n")
        site_folder_list = os.listdir(fr"Downloaded_data")
        if site_folder_list:
            analysed_output_list = []
            for site_folder in site_folder_list:
                analysed_output = {}
                sub_folder_or_files = os.listdir(fr"Downloaded_data/{site_folder}")
                analysed_output['folder_name'] = site_folder
                for sub_folder_or_file in sub_folder_or_files:
                    if 'text_file.txt' in sub_folder_or_file:
                        with open(fr"Downloaded_data/{site_folder}/{sub_folder_or_file}") as f:
                            analysed_output['url'] = f.readline().split("=")[-1].strip()
                            text_data = f.read()
                            analysed_output['total_length_of_text'] = len(text_data)
                            analysed_output['total_length_of_text_after_removing_spaces'] = len(''.join(text_data.split()))
                    elif 'images' in sub_folder_or_file:
                        analysed_output['images_count'] = len(os.listdir(fr"Downloaded_data/{site_folder}/{sub_folder_or_file}"))
                    elif 'reference_urls.json' in sub_folder_or_file:
                        with open(fr"Downloaded_data/{site_folder}/{sub_folder_or_file}") as f:
                            analysed_output['reference_urls_count'] = len(json.loads(f.read()))
                analysed_output_list.append(analysed_output)
                print(f"{site_folder} Analysed Successfully")
            print("\n")
            with open("Analysed_stats.json",'w') as f:
                f.write(json.dumps(analysed_output_list))
                print("Analysed_stats.json File Successfully Generated")
        else:
            print("No Site Url Folders found to Analyse. please Recrawl and Download All Data.")



if __name__ == '__main__':
    obj = Crawler()
    obj.crawl(url=obj.sitemap_url) # Function to Crawl Data
    obj.analyse_data() # Function to Analyse Downloaded Data


