#!/usr/bin/env python
# coding: utf-8

# In[1]:

#!/usr/bin/env python
# coding: utf-8

# In[24]:


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
        # In[26]:
        # Visit the mars nasa news site
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)


        # In[27]:


        # Convert the browser html to a soup object and then quit the browser
        html = browser.html
        news_soup = soup(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')


        # In[28]:


        slide_elem.find('div', class_='content_title')


        # In[29]:


        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title


        # In[30]:


        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_paragraph


        # ### JPL Space Images Featured Image

        # In[31]:


        # Visit URL
        url = 'https://spaceimages-mars.com'
        browser.visit(url)


        # In[32]:


        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()


        # In[33]:


        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')
        #img_soup


        # In[34]:


        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel


        # In[35]:


        # Use the base url to create an absolute url
        featured_image = f'https://spaceimages-mars.com/{img_url_rel}'
        #featured_image


        # ### Mars Facts

        # In[36]:


        facts = pd.read_html('https://galaxyfacts-mars.com')[0]
        #facts.head()
        # In[37]:
        facts.columns=['Description', 'Mars', 'Earth']
        facts.set_index('Description', inplace=True)
        #facts
        # In[38]:
        facts = facts.to_html(classes=["table table-dark table-striped table-hover table-responsive"], header=True)


        # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

        # ### Hemispheres

        # In[39]:


        # 1. Use browser to visit the URL 
        url = 'https://marshemispheres.com/'
        browser.visit(url)


        # In[40]:


        html = browser.html
        img_soup = soup(html, 'html.parser')
        items = img_soup.find("div",{"class":"results"}).find_all("div", {"class", "item"})


        # In[41]:


        # 2. Create a list to hold the images and titles.
        hemisphere_image_urls = []

        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for item in items:
            link = item.find("a",{"class": "itemLink"})["href"]
            link_url = url + link
            
            browser.visit(link_url)
            
            html = browser.html
            img_soup = soup(html, 'html.parser')
            
            img =img_soup.find("img",{"class", "wide-image"})["src"]
            img_url = url + img
            
            title = img_soup.find("h2",{"class": "title"}).text
            
            data = {"img_url" : img_url, "title": title}
            
            hemisphere_image_urls.append(data)


        # In[42]:


        # 4. Print the list that holds the dictionary of each image url and title.
        #hemisphere_image_urls


        # In[43]:


        # 5. Quit the browser
        browser.quit()
        title1 = hemisphere_image_urls[0]["title"]
        image1 = hemisphere_image_urls[0]["img_url"]
        
        title2 = hemisphere_image_urls[1]["title"]
        image2 = hemisphere_image_urls[1]["img_url"]

        title3 = hemisphere_image_urls[2]["title"]
        image3 = hemisphere_image_urls[2]["img_url"]

        title4 = hemisphere_image_urls[3]["title"]
        image4 = hemisphere_image_urls[3]["img_url"]

        # In[45]:


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

