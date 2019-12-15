#!/usr/bin/env python
# coding: utf-8

# Import dependencies
import pandas as pd

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# get_ipython().system('which chromedriver')

############################################################################
def mars_article(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # extract html and parse using Beautiful Soup
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p

############################################################################
def featured_image(browser):
    # ### Featured Images

    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
       return None
  
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

############################################################################
    
def mars_data():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
      
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    # convert the dataframe into html for display on webpage
    return df.to_html()

############################################################################

def scrape_all():
    import datetime as dt
    # Initiate headless driver for deployment
    
    # Path to chromedriver
    exec_path="C:/Users/rusinghal/Desktop/DTPersonal/Post May 2016 Encryption/Berkley Extension Bootcamp docs/Web Scraping/chromedriver"

    # setting path on Windows 
    executable_path = {'executable_path': exec_path}
    browser = Browser('chrome',**executable_path, headless=False)

    news_title, news_paragraph = mars_article(browser)
       
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_data(),
        "last_modified": dt.datetime.now()
    }
      
##################################################
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # extract html and parse using Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   
    divs = soup.findAll(class_= 'description')
    
    thumbs=[]
    i=0    
    for div in divs:
        img_title=div.find('h3').text
        title=f"title{i}"
        data[title]=img_title
        imghref=div.find('a',href=True)
        thumbs.append(f"https://astrogeology.usgs.gov{imghref['href']}")
        i=i+1
    
    x=0
    for link in thumbs:
        browser.visit(link)
        # extract html and parse using Beautiful Soup
        html2 = browser.html
        soup2 = BeautifulSoup(html2, 'html.parser')
        imgurl=f"img_url{x}"
        
        for imglink in soup2.findAll('a', href=True, text='Sample'):
            data[imgurl]=imglink['href']
        
        x=x+1
####################################################

    return data

############################################################################

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())