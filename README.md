# WebScraper-Nordstrom
Scraping for every image in the website directory and downloading them to the correct path

# Instructions

Run `scrape.py` 	 to scrape the specified url

Run `sdownload.py` to download the images (it will put the images in the correct path also)

`img_current.txt` stores the information about how many tabs, categories, subcategories, pages, articles have been scraped

`img_url.txt` stores information about the scraped articles (path,url of image)

`img_downloaded.txt` stores information about how many images have been downloaded

# Warnings
###############################################################################

Do not open or delete these files while the program is running:
	`img_current.txt`
	`img_url.txt`
	`img_downloaded.txt`

To check the contents, simply copy and paste the whole file without opening it

###############################################################################

# To do list
- :heavy_check_mark: Stores information about every tab 
- :heavy_check_mark: Stores information about every category 
- :heavy_check_mark: Stores information about every sub-category 
- :heavy_check_mark: Stores information about every article 
- :heavy_check_mark: Stores information about every color 
- :heavy_check_mark: Downloads images in their correct path
- :heavy_check_mark: Caters errors
- :x: GUI