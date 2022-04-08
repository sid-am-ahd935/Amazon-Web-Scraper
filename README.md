This repo is for Credicxo Python Task 1.


# Credicxo-Python-Developer-Task-1

This project was created for submission to Credicxo under Python Developer Task 1. This project is made using built in python libraries and modules mainly handling the functionalities like transferring data to and from JSON files, reading the CSV file, visiting the urls and scraping the data, etc.

First, the given CSV  file is loaded either by dowloading the whole file or by  directly loading data from it. Then the countries and asins are extracted and the required url is constructed from it using the anonymous lambda function named 'make_url'. A while loop iterates over indexes from 0 to 999, iterating over all countries and asins collected, then the required url is made, then it is visited.

The url is transferred into a function named as 'visit' which takes in the url and sends a get request and then stores the response under a vairable named as 'r'. This variable is then scanned to view whether the visited url was successfully visited or there were any issues. Then from the response's status code, either the html content is passed into the extractor function named 'extract' which further stores the extracted data inside cache, or if the response was invalid then the response is printed for its unavailability.

If the request was considered as a bot, then the captcha resolver functions inside the Bonus Task handle and extract the captcha and submit it. This is done by using the Tesseract OCR recognition package. This package is available to python under the pytesseract module. From more precision in generating the OCR captcha data, open-cv module is used to grayscale the image and feed it to the Tesseract package.

After extracting the captcha, it is then submitted to the website again via a post request. Then the data is extracted again as normal.

If the captcha is not valid and multiple captcha submissions are being required, then the scraper takes a break (which increases upon each captcha) to pass through undetected.

If the scraper is still caught, then only human captcha submission would be liable, hence it restricts further sending requests, and breaks the loop.

At the end of all functionality, the program then saves the cached data into the required JSON files.

Note that there is also an extra directory created for storing error HTMl templates for further investigation, and all the time stamps of each round is stored in another JSON file.



## To run the program directly:

[![Google Colab Notebook](https://colab.research.google.com/img/colab_favicon_256px.png)](https://colab.research.google.com/drive/1vbYyOB_-YdQamzkKnAeSHjDsqe8eCItH?usp=sharing)


