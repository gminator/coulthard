import warnings

# To suppress all warnings
warnings.filterwarnings("ignore")

# To suppress a specific warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

from common import * 
print_colorful_intro("I will now update my library with the latest F1 News")

import requests
from usp.tree import sitemap_tree_for_homepage
import xmltodict
import markdownify 
from bs4 import BeautifulSoup
import os 
import re
import json
from datetime import datetime, timedelta

# Call the function to print the intro


"""
This Script Will Download & Organize all the articles 
it can retrieve from the F1 Website
"""
class SiteMapNotFound (Exception): pass
class NotContentFoundExcetpion (Exception): pass


def convert_to_standard(date_str):
    ago_pattern = re.compile(r'(\d+) (minute|hour|day|week|month|year)s? ago')
    match = ago_pattern.match(date_str)
    
    if match:
        quantity = int(match.group(1))
        unit = match.group(2)
        
        if unit == 'minute':
            delta = timedelta(minutes=quantity)
        elif unit == 'hour':
            delta = timedelta(hours=quantity)
        elif unit == 'day':
            delta = timedelta(days=quantity)
        elif unit == 'week':
            delta = timedelta(weeks=quantity)
        elif unit == 'month':
            delta = timedelta(days=quantity*30)
        elif unit == 'year':
            delta = timedelta(days=quantity*365)
        
        result_date = datetime.now() - delta
        return result_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return date_str

def fetch_sitemap(i=1):	
	url = "https://www.formula1.com/content/fom-website/en/latest/all.sitemap.%s.xml" % i
	res = requests.get(url)

	if res.status_code != 200:
		raise SiteMapNotFound("Could not find %s" % url)

	raw = xmltodict.parse(res.text)
	print("Download %s News Articles" % len(raw["urlset"]["url"]))

	page = 0
	for r in raw["urlset"]["url"]:
		page += 1
		try:
			(file, status, date, author, date) = page_to_markdown(r["loc"], r["lastmod"]) 
		except NotContentFoundExcetpion as e: 
			print("\033[1;38;5;208mNot Content Tag:\033[0m %s %s" % (r["loc"], e))
		except Exception as e: 
			print("\033[1;91mFailed:\033[0m %s %s" % (r["loc"], e))

		print("Simte Map(%s) %s/%s %s: %s %s %s %s" % (i, page, len(raw["urlset"]["url"]),status, author, date,file, date))


def create_folder(path):
    """Create a folder recursively."""
    try:
        os.makedirs(path)
        #print(f"Folder '{path}' created successfully.")
    except OSError as e:
        if os.path.isdir(path):pass
        else:pass

def write_to_file(file_path, content):
    """Write content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        #print(f"Content successfully written to '{file_path}'.")
    except Exception as e: pass

def page_to_markdown(url, updated):
	
	base = os.path.basename(url)
	file = os.path.join(os.getcwd(), "RAG", os.path.basename(base))
	
	if os.path.isfile(file):
		return (file, "\033[1;94mSkipped\033[0m", updated, "Unknown", "Done")

	path = os.path.join(os.getcwd(), "RAG", )
	create_folder(path) 

	res = requests.get(url)
	soup = BeautifulSoup(res.text)

	date = soup.find_all("time")[0]
	try:
		content = soup.find_all("div", {"class": "f1-article--rich-text"})[0]
	except:
		raise NotContentFoundExcetpion("Could not find rich content")

	title = soup.find_all("h1", {"class": "f1--xl"})[0]
	author = print_text_on_one_line(soup.find_all("div", {"class": "f1-special-author--content"})[0].text) if soup.find_all("div", {"class": "f1-special-author--content"}) else "Unknown"

	metadata = {"author" : author,"published on" : convert_to_standard(date.text), "source" : url, "tags" : list(dict.fromkeys([ t.text for t in soup.find_all("a", {"class" : "tag"})]))}
	
	write_to_file(file, "# %s\nPublished On: %s\nAuthor: %s\n%s\n%s" % (title.text.strip(), convert_to_standard(date.text), author, content.text, json.dumps(metadata)))
	return (base, "\033[1;92mCreated\033[0m", updated, author, convert_to_standard(date.text))

#fetch_sitemap(1)

i = 15
while True:
	i += 1
	try:
		tree = fetch_sitemap(i)
	except SiteMapNotFound as e: break
	except Exception as e: 
		print(e)

