# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# In[25]:
class ScraperHelper():

    def scrape_all():
    # Set the executable path and initialize Splinter
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=True)

        # ### Visit the NASA Mars News Site
        # Visit the mars nasa news site
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        news_soup = soup(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()

        # ### JPL Space Images Featured Image

        # Visit URL
        url = 'https://spaceimages-mars.com'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        #featured_image
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # Use the base url to create an absolute url
        featured_image = f'https://spaceimages-mars.com/{img_url_rel}'
        

        # ### Mars Facts
        facts = pd.read_html('https://galaxyfacts-mars.com')[0]
        facts.columns=['Description', 'Mars', 'Earth']
        facts.set_index('Description', inplace=True)
        #Convert to html add table formatting
        facts = facts.to_html(classes=["table table-dark table-striped table-hover table-responsive"], header=True)


        # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
        # ### Hemispheres

        # Use browser to visit the URL 
        url = 'https://marshemispheres.com/'
        browser.visit(url)

        # soupitysoup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        # Use the parent element to find the first a tag
        items = img_soup.find("div",{"class":"results"}).find_all("div", {"class", "item"})

        # Create a list to hold the images and titles.
        hemisphere_image_urls = []

        # for loop to retrieve the image urls and titles for each hemisphere.
        for item in items:
            #get link
            link = item.find("a",{"class": "itemLink"})["href"]
            link_url = url + link
            #visit Browser
            browser.visit(link_url)
            # soupitysoup
            html = browser.html
            img_soup = soup(html, 'html.parser')
            # get image
            img =img_soup.find("img",{"class", "wide-image"})["src"]
            img_url = url + img
            #get title
            title = img_soup.find("h2",{"class": "title"}).text
            #init keys and valus
            data = {"img_url" : img_url, "title": title}
            #append list
            hemisphere_image_urls.append(data)

        #Quit the browser
        browser.quit()
        #init variables for each hemisphere image
        title1 = hemisphere_image_urls[0]["title"]
        image1 = hemisphere_image_urls[0]["img_url"]
        
        title2 = hemisphere_image_urls[1]["title"]
        image2 = hemisphere_image_urls[1]["img_url"]

        title3 = hemisphere_image_urls[2]["title"]
        image3 = hemisphere_image_urls[2]["img_url"]

        title4 = hemisphere_image_urls[3]["title"]
        image4 = hemisphere_image_urls[3]["img_url"]

        # In[45]:

        #Store info in dictionary
        mars_data = {
                    "news_title": news_title,
                    "news_paragraph": news_paragraph,
                    "featured_image": featured_image,
                    "facts": facts,
                    "hemispheres": hemisphere_image_urls,
                    "title1": title1,
                    "title2": title2,
                    "title3": title3,
                    "title4": title4,
                    "image1": image1,
                    "image2": image2,
                    "image3": image3,
                    "image4": image4,
                    }
        return mars_data

