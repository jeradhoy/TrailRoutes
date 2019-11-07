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



from zipfile import ZipFile
with ZipFile("./Data/TRAN_Montana_State_Shape.zip") as zipObj:
    file_list = zipObj.namelist()
    trail_files = [filename for filename in file_list if "Trans_Trail" in filename]
    for trail_file in trail_files:
        zipObj.extract(trail_file, "./Data/Shapefiles/")




