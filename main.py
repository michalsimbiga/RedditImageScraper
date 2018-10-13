"""

    Scraping Reddit for images of funny cats or other :)

    Usage: from command line we can specify the url (-l) to scrape from and the directory (-d)
            to save our files to.

    Example: python3 -l https://www.reddit.com/r/Funnypics/ -d Funnypics

    Created by Michał Simbiga

"""

import os
import optparse
import requests
from bs4 import BeautifulSoup


def cleanup_urls(lst):
    """
        Search 'img' tags and retrieve url that is specified in the src= tag
        Iterate the list and ignore non-important links, print out the links
    """
    temp = []
    for item in lst:
        if 'renderTimingPixel' not in item and ('jpg' or 'png' in item):
            print(item)
            if 'preview' in item:
                #   Split preview items and correct them to a correct link:
                #   https://i.reddit.it/name.typeoffile
                temp.append(item.split('preview')[0] + "i" + item.split('preview')[1].split('?')[0])
                print('Image Link :\n ' + str(item) + '\n')
            else:
                temp.append(item)
    return temp


def change_directory(newpath):
    """
        Check's if the directory exists, if not creates it and changes path
        else just changes path
    """
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        os.chdir(newpath)
    else:
        os.chdir(newpath)


#   Parse arguments
PARSER = optparse.OptionParser('usage %prog -l <url_to_scrape> -d <directory_to_save_to>')
PARSER.add_option('-l',
                  dest='url_to_scrape',
                  type='string',
                  default='https://www.reddit.com/r/lolcats/',
                  help='Specify Url To scrape from')
PARSER.add_option('-d',
                  dest='dir_to_save_to',
                  type='string',
                  default='images',
                  help='Folder to save images to')

(OPTIONS, ARGS) = PARSER.parse_args()
PAGE_TO_OPEN = OPTIONS.url_to_scrape
DIRECTORY = OPTIONS.dir_to_save_to

#   Make a Request to a website and get a response,
#   add headers to bypass BOT-protection
REQUEST = requests.get(PAGE_TO_OPEN, headers={'User-agent': 'Image_Scraper'})

#   Read and decode the response
HTML_TO_SCRAPE = REQUEST.text

#   Initiate BF object with parser
SOUP = BeautifulSoup(HTML_TO_SCRAPE, 'html.parser')

#   Search 'img' tags and retrieve url that is specified in the src= tag
IMAGES = cleanup_urls([img['src'] for img in SOUP.find_all('img', {"src": True})])

for image in IMAGES:
    print("Image found: " + image)

#   Change Directory for where to save images to be scraped
change_directory(DIRECTORY)

#   Fetching the files and saving them in specified directory
for image in IMAGES:
    try:
        name = image.split("/")[-1]
        f = open(name, 'wb')
        print("Saving file: " + name + " ...")
        f.write(requests.get(image).content)
        print("...saved\n")
        f.close()
    except:
        print("Couldn't fetch the image!")

print("All done, exiting.")
