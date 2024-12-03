from pywebcopy import save_webpage
import os

url = "https://w3schools.com/html"
download_folder = "/home/sebas/Piracy/"
print(download_folder)

save_webpage(url, download_folder, open_in_browser=True)