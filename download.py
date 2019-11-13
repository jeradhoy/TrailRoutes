import urllib.request
from bs4 import BeautifulSoup


# Read map html
with open("./The National Map.html") as f:
    data = f.read()
soup = BeautifulSoup(data)

# Get links for state zip files
links = [link.get('href') for link in soup.find_all('a')]
state_links = [link for link in links if ".zip" in link and "NATIONAL" not in link]

# Download each state zip file
for link in state_links:
    urllib.request.urlretrieve(link, "./Data/" + link.split("/")[-1])

CONFIG = {}
CONFIG["DataDir"] = "./Data/"

files = os.listdir(CONFIG["DataDir"])
zip_files = [CONFIG["DataDir"] + filename for filename in files if ".zip" in filename]
zip_files



import os
from zipfile import ZipFile

def unzip_files_that_match(zip_path: str, unzip_dir: str, match_str: str) -> str:
    with ZipFile(zip_path) as zipObj:
        file_list = zipObj.namelist()
        trail_files = [filename for filename in file_list if match_str in filename]
        unzip_path_suffix = zip_path.split("/")[-1].split(".")[0]
        for trail_file in trail_files:
            zipObj.extract(trail_file, unzip_dir + unzip_path_suffix)


for zip_file in zip_files:
    unzip_files_that_match(zip_file, CONFIG["DataDir"] + "Shapefiles/", "Trans_Trail")


