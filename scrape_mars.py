from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import os
import pandas as pd

def scrape():
    scrape_mars_dict ={}
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    #printing out the HTML pf that page
    html = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(html)
    soup = bs(response.text, 'lxml')

    #looking through the features to find the title and paragraph
    divs = soup.find('div', class_='features')

    #Printing out the first news title and description. I could not find a paragraph value
    news_title = divs.find('div', class_='content_title').text
    newsp = divs.find('div', class_='rollover_description').text
    scrape_mars_dict['news_title'] = news_title
    scrape_mars_dict['newsp'] = newsp

    #connecting to chrome driver


    #visiting the url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #getting a soup of the website
    html = browser.html
    soup = bs(html, "lxml")

    #getting the image url
    image_div = soup.find('div', class_='default floating_text_area ms-layer')
    image = image_div.find('footer')
    image_url = 'https://www.jpl.nasa.gov'+ image.find('a')['data-fancybox-href']
    scrape_mars_dict['featured_image_url'] = image_url

    #connecting to twitter and printing out the html
    twitter = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter)
    soup = bs(response.text, 'lxml')

    #getting the text from the tweet
    div = soup.find('div', class_='js-tweet-text-container')
    ptext = div.find('p', class_='js-tweet-text').text
    #removing text from the image
    atext =  div.find('a', class_='twitter-timeline-link u-hidden').text
    mars_weather = ptext.replace(atext,'')
    scrape_mars_dict['mars_weather'] = mars_weather

    url = 'https://space-facts.com/mars/'
    tablelist = pd.read_html(url)


    mars_facts = tablelist[0]
    mars_facts.columns = ['Measurement', 'Value']
    mars_facts.set_index('Measurement', inplace=True)


    facts_html = mars_facts.to_html()
    facts_html.replace("\n", "")
    scrape_mars_dict['mars_facts'] = facts_html


    hemisphere_list = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    divs = soup.find_all('div', class_='item')
    base_url ="https://astrogeology.usgs.gov"

    for div in divs:
        hemisphere_dict = {}

        href = div.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)

        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html, 'lxml')

        title = hemisphere_soup.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = title

        img_url = hemisphere_soup.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url

        hemisphere_list.append(hemisphere_dict)

    scrape_mars_dict['hemisphere_image_urls'] = hemisphere_list

    return scrape_mars_dict
