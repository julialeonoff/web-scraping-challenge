from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import time 

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # The news
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find('div', class_='list_text')
    news_title = news.find('div', class_='content_title').text
    news_p = news.find('div', class_='article_teaser_body').text

    # Featured image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup2 = BeautifulSoup(html, 'html.parser')
    image = soup2.find('figure', class_='lede')
    featured_image = image.a['href']
    featured_image_url = (f'https://www.jpl.nasa.gov{featured_image}')

    # Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(5)
    pattern = re.compile('InSight')
    html = browser.html
    soup3 = BeautifulSoup(html, 'html.parser')
    weather = soup3.find("span", text=pattern).text
    mars_weather = print(weather)

    # Mars Facts
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)
    table = df.to_html(classes = 'table table-stripped')

    # Hemisphere pics
    hemisphere_image_url = []
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find_all('div', class_='item')
    for hemisphere in info:
        hemisphere_dict = {}
        hemisphere_dict['title'] = hemisphere.find('h3').text
        hemisphere_image_url.append(hemisphere_dict)
        browser.click_link_by_partial_text(hemisphere.find('h3').text)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_dict['image_url'] = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        browser.visit(hemisphere_url)

    # Dictionary time
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'mars_facts': table,
        'hemisphere_image_url': hemisphere_image_url
    }

    browser.quit()

    return mars_data
