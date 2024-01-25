import requests
from usp.tree import sitemap_tree_for_homepage
import xmltodict
import markdownify 
from bs4 import BeautifulSoup
import os 
"""
This Script Will Download & Organize all the articles 
it can retrieve from the F1 Website
"""
class SiteMapNotFound (Exception): pass

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
			(file, status, date) = page_to_markdown(r["loc"], r["lastmod"]) 
		except Exception as e: 
			print("Failed %s " % r["loc"])

		print("Simte Map(%s) %s/%s %s: %s %s" % (i, page, len(raw["urlset"]["url"]),status, file, date))


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
	file = os.path.join(os.getcwd(), "RAG",  "%s.%s" % (updated[:10], os.path.basename(base)))
	
	if os.path.isfile(file):
		return (file, "Skipped", updated)

	path = os.path.join(os.getcwd(), "RAG", )
	create_folder(path) 
	res = requests.get(url)
	soup = BeautifulSoup(res.text)
	content = soup.find_all("div", {"class": "f1-article--rich-text"})[0]

	write_to_file(file, content.text)
	return (base, "Created", updated)


i = 0
while True:
	i += 1
	try:
		tree = fetch_sitemap(i)
	except SiteMapNotFound as e: pass
	except Exception as e: print(e)
	
