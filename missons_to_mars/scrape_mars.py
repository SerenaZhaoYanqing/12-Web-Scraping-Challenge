# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_all():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo later 
    mars_data = {} 

    # visiting url-nasa news 
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    #getting latest title and paragraph
    first_title = soup.find(class_="content_title") 
    first_para = soup.find('div', class_="article_teaser_body")

    
    #getting featured image 
    url_img="https://spaceimages-mars.com/"
    browser.visit(url_img) 
    # HTML object
    html_img = browser.html
    # Parse HTML with Beautiful Soup
    soup_img = BeautifulSoup(html_img, 'html.parser')
    #scrape feature image 
    featured_image=soup_img.find('img', class_="headerimage fade-in")
    featured_image_url=url_img+featured_image['src']


    # Mars Facts 
    # use the `read_html` function in Pandas to automatically scrape any tabular data from a page.
    url_facts="https://galaxyfacts-mars.com/"
    tables=pd.read_html(url_facts)
    # check through multiple table lists. slice the one we need 
    df=tables[0]
    #rename column
    df.columns=['Description','Mars','Earth']
    #set first column as index
    df.set_index('Description',inplace=True)    
    #convert into html
    facts_html=df.to_html()

    # Mars Hemispheres
    base_url='https://marshemispheres.com/'
    browser.visit(base_url)  
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup_base = BeautifulSoup(html, 'html.parser')
    #return all results ( contain titles, html of all hemispheres links )
    results=soup_base.find_all('div',class_='item')
    # create an empty list
    hemisphere_image_urls=[]

    # loop through url for each hemisphere (then scarping full image)   
    for result in results: 
        url_hemi=base_url+result.a['href']
        browser.visit(url_hemi)
    
    # create html object and parse with bs for each of the hemisphere
        html_hemi=browser.html
        soup_hemi=BeautifulSoup(html_hemi, 'html.parser')
    
    #getting titles
        title=soup_hemi.find('h2', class_ = 'title').text
    
    # get full resolution image(clicl sample on the web) 
        downloads = soup_hemi.find('div', class_ = 'downloads')
        image = downloads.find('a')['href']

    #concate image url 
        image_url=base_url+image
    
    # store titels and image url in a dict format 
        hemisphere_image_urls.append({"title": title, "img url": image_url})
    
    # return all mars data 
    mars_data= {
        "news_title": first_title,
        "news_paragraph": first_para,
        "featured_image": featured_image_url,
        "facts": facts_html,
        "hemispheres": hemisphere_image_urls,
    }
    # Close the browser after scraping
    browser.quit()

    return mars_data