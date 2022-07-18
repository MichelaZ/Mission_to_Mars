# Mission to Mars


## Methods
 During the module I built out an app and started the scraper in jupyter notebooks so it would grab the news title, news paragraph, featured image and a data frame comparing earth and mars facts. 
### Deliverable 1
For deliverable 1 I used Jupyter notebooks to get images and labels for Mars’ four hemispheres. The code can be viewed in the [Mission_to_Mars_starter_code]( https://github.com/MichelaZ/Mission_to_Mars/blob/main/Mission_to_Mars_Challenge_starter_code.ipynb) file. Here are the outputs:
```
[{'img_url': 'https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg',
  'title': 'Cerberus Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg',
  'title': 'Schiaparelli Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg',
  'title': 'Syrtis Major Hemisphere Enhanced'},
 {'img_url': 'https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg',
  'title': 'Valles Marineris Hemisphere Enhanced'}]
```
<details>
<summary>Cerberus Hemisphere Enhanced</summary>

![Cerberus Hemisphere Enhanced](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Submission/img1.png)
 </details>
 <details>
<summary>Schiaparelli Hemisphere Enhance</summary>
 
![Schiaparelli Hemisphere Enhanced](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Submission/img2.png)
 </details>
 <details>
<summary>Syrtis Major Hemisphere Enhanced</summary>
 
![Syrtis Major Hemisphere Enhanced](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Submission/img3.png)
 </details>
 <details>
<summary>Valles Marineris Hemisphere Enhanced</summary>
![Valles Marineris Hemisphere Enhanced](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Submission/img1.png)
</details>

### Deliverable 2
In deliverable 2 I exported the jupyter notebook file to a python file and refactored the code so that I could use it with my flask app. 
#### Scraper
<details>
 <summary>1. I imported the dependencies.</summary>
 
```
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time
```
</details>

 <details>
<summary>2. I created a class called ScraperHelper, defined a function called scrape_all, set the executable path and initialized Splinter.</summary>
 
```
class ScraperHelper():
    def scrape_all():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=True)
    
```
 </details>
 
 <details>
 <summary>3. I grabbed the news title and news paragraph.</summary>
 
```
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        browser.is_element_present_by_css('div.list_text', wait_time=1)

        html = browser.html
        news_soup = soup(html, 'html.parser')

        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
```
 </details>
 
<details>
<summary>4. I got the featured image</summary>
  
```
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
```
 </details>
 <details>
<summary>5. I created a dataframe with the mars facts, converted the table to HTML and formated it.</summary>
  
```        # ### Mars Facts
        facts = pd.read_html('https://galaxyfacts-mars.com')[0]
        facts.columns=['Description', 'Mars', 'Earth']
        facts.set_index('Description', inplace=True)
        #Convert to html add table formatting
        facts = facts.to_html(classes=["table table-dark table-striped table-hover table-responsive"], header=True)
```
 </details>
 
 <details>
<summary>6. After setting up the parser and visiting the browser. I found the parent item. I declared a list to store the image title and URLs for the hemispheres.</summary>
  
 ```
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
```
 </details>
 
 <details>
<summary>7. I used a a for loop to grab all of the URLs and title and append them to the list.</summary>
 
```
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
```
</details>
 
 <details>
  <summary>8. I declared values get each URl for my HTML.</summary>
  
```
#init variables for each hemisphere image
        title1 = hemisphere_image_urls[0]["title"]
        image1 = hemisphere_image_urls[0]["img_url"]
        
        title2 = hemisphere_image_urls[1]["title"]
        image2 = hemisphere_image_urls[1]["img_url"]

        title3 = hemisphere_image_urls[2]["title"]
        image3 = hemisphere_image_urls[2]["img_url"]

        title4 = hemisphere_image_urls[3]["title"]
        image4 = hemisphere_image_urls[3]["img_url"]
```
 </details>
 
<details>
 <summary>9. I added all my variables for the data I want to display on the webpage to a dictionary.</summary>
```
        mars_data = {
                    "news_title": news_title,
                    "news_paragraph": news_paragraph,
                    "featured_image": featured_image,
                    "facts": facts,
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
```
</details>

#### Flask App

<details>
 <summary>1. Import dependecies and the scraperhelper class from the scraping file.</summary>
 
```
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from scraping import ScraperHelper
```
 </details>
 <details>
  <summary>2. Set up the connection to mongo.</summary>
  
```
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
```
 </details>
 
 <details>
  <summary>3. Sets the routes so that the template can find the data.</summary>
  
```
@app.route("/")
def index():
   mars_data = mongo.db.mars_detail.find_one()
   return render_template("index.html", mars=mars_data)
```
 </details>
 
 <details>
  <summary>4. Flask initializes the scraper to gather the data and add it to the mongodb.</summary>
  
```
@app.route("/scrape")
   
def scrape():
   scraper = ScraperHelper
   mars_data = scraper.scrape_all()
   mars_detail= mongo.db.mars_detail
   mars_detail.update_one({}, {"$set": mars_data}, upsert=True)
   return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)
```
</details>

### Deliverable 3
In deliverable 3 I used html and bootstraps to format my webpage and make it responsive. 

<details>
  <summary>1. I updated the bootstraps to a more recent version.</summary>
  
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Mission to Mars</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css"
      integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" 
      crossorigin="anonymous"
    />
```
</details>
<details>
<summary>2. I used an image for the background of the Jumbotron and made the background a gradient. I used badges to style the rest of the titles and I added the news title and paragraph to a card.</summary>

```
</head>
  <body style="background-image: linear-gradient(#fec89a, #001219);">
    <div class="container ">
      <!-- Add Jumbotron to Header -->
      <br>
      <div class="jumbotron text-center" style="background: url(https://mediaproxy.salon.com/width/1200/https://media.salon.com/2022/05/mars-canyons-0517221.jpg) no-repeat center; 
      background-size: cover;
      border-radius: 25px 25px 25px 25px;
      color: white;
      box-shadow: 0px 10px 100px rgba(0, 18, 25,0.5)">
      <br>
      <span class="badge badge-pill" style="background-image: linear-gradient(rgb(187, 62, 3,.85),rgb(187, 62, 3,.85));"><h1>Mission to Mars</h1></span>
        <br>
        <br>
        <!-- Add a button to activate scraping script -->
        <p><a class="btn btn-lg" href="/scrape" role="button" style="background-image: linear-gradient(rgb(233, 216, 166,.85),rgb(233, 216, 166,.85));">Scrape New Data</a></p>
        <br>
      </div>
      <!-- Add section for Mars News -->
      <div class="row" id="mars-news">
        <div class="col-md-12">
          <br>
          <br>
          <div class="card text-white bg-dark">
            <div class="card-header">
                            <h2>Latest Mars News</h2>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ mars.news_title }}</h5>
              <p class="card-text">{{ mars.news_paragraph }}</p>
            </div>
          </div>
          <br>
          <br>
        </div>
      </div>
      <!-- Section for Featured Image and Facts table -->
      <div class="row justify-content-md-center" id="mars-featured-image">
        <div class="col-md-8">
          <span class="badge badge-pill" style="background-image: linear-gradient(rgb(0, 18, 25,.85),rgb(0, 18, 25,.85));"><h2>Featured Mars Image</h2></span>
        <br>
        <br>
          <img
            src="{{mars.featured_image }}"
            class="img-fluid"
            alt="Responsive image"
            style="border-radius: 25px 25px 25px 25px; box-shadow: 0px 10px 100px rgba(0, 18, 25,0.5)"
          />
          <br>
          <br>
        </div>
        <div class="col-md-4 justify-center">
          <!-- Mars Facts -->
          <div class="row justify-content-md-center" id="mars-facts"></div>
            <span class="badge badge-pill" style="background-image: linear-gradient(rgb(0, 18, 25,.85),rgb(0, 18, 25,.85));"><h2>Mars Facts</h2></span>
          <br>
          <br>
                {{ mars.facts | safe }}                   
          </div>
        </div>
      </div>
    </div>
```
</details>

<details>
<summary>3. I added the hemisphere images to the page. The buttons on the image cards for the hemispheres open the image in a new tab.</summary>

```
    <div class="container mt-4 bg-dark rounded"><br>
      <h2 class="text-center text-white">Mars Hemispheres</h2><br>
      <!-- <hr> -->
        <div class = "row">
          <div class="col-md-6">
            <div class="card">
              <img class="card-img-top img-fluid img-thumbnail" src={{ mars.image1 }} alt="Card image cap">
              <div class="card-body">
                <h5 class="card-title">{{ mars.title1 }}</h5>
                <a href={{ mars.image1 }}  target={{ mars.image1 }}  class="btn btn-dark">Fullsize image</a>
              </div>
            
          </div>
        <br>
       </div>
       <div class="col-md-6">
        <div class="card">
          <img class="card-img-top img-fluid img-thumbnail" src={{ mars.image3 }} alt="Card image cap">
          <div class="card-body">
            <h5 class="card-title">{{ mars.title3 }}</h5>
            <a href={{ mars.image2 }}  target={{ mars.image2 }}  class="btn btn-dark">Fullsize image</a>
          </div>
        </div>
        <br>
      </div>
        <div class="col-md-6">
          <div class="card">
            <img class="card-img-top img-fluid img-thumbnail" src={{ mars.image3 }} alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">{{ mars.title3 }}</h5>
              <a href={{ mars.image3 }}  target={{ mars.image3 }}  class="btn btn-dark">Fullsize image</a>
            </div>
        </div>
        <br> 
     </div>
     <div class="col-md-6">
      <div class="card">
        <img class="card-img-top img-fluid img-thumbnail" src={{ mars.image4 }} alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">{{ mars.title4 }}</h5>
          <a href={{ mars.image4 }}  target={{ mars.image4 }}  class="btn btn-dark">Fullsize image</a>
        </div>
      </div>
      <br>
      </div><br><br>
</div>
  </div>
<br>
<br>
  </body>
</html>
```
</details>

<details>
<summary><b>Desktop View</b></summary>

![Desktop Version](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/desktop_full.png)
</details>

<details>
<summary><b>Mobile View</b></Summary>

![](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/mobile1.png)

![](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/mobile2.png)

![](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/mobile3.png)

![](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/mobile4.png)

![](https://github.com/MichelaZ/Mission_to_Mars/blob/main/Resources/mobile5.png)
</details>



#### Resources:
- [Badges](ileriayo.github.io/markdown-badges/)
- [Jumbotron Background](https://mediaproxy.salon.com/width/1200/https://media.salon.com/2022/05/mars-canyons-0517221.jpg)
- [Scraped News](https://redplanetscience.com/)
- [Scraped Featured Image](https://spaceimages-mars.com)
- [Scraped Facts](https://galaxyfacts-mars.com)
- [Scraped Hemispheres](https://marshemispheres.com/)

![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) 
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) 
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) 

