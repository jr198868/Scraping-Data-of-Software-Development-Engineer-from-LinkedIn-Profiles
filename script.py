
import csv
import paramaters
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(paramaters.file_name, 'wb'))
writer.writerow(['Name', 'Job Title', 'Location', 'URL'])

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_name('session_key')#code has been modified due to the web page's configuration changing
username.send_keys(paramaters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_name('session_password')#code has been modified due to the web page's configuration changing
password.send_keys(paramaters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
sign_in_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(paramaters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls_YC = []
for i in range(25):
    sign_in_button = driver.find_element_by_id('pnnext')
    #code has been modified due to the web page's configuration changing
    linkedin_urls = driver.find_elements_by_xpath("//div[@class='r']/a")
    
    for urls in linkedin_urls:
        linkedin_urls_YC.append(urls.get_attribute("href"))
    #linkedin_urls = [url for url in linkedin_urls]
    #linkedin_urls_new = 'httpsuk.linkedin.com/in/'
    #url_new = linkedin_urls[33:-6]
    #url_string = str(url_new)
    #linkedin_urls_new += url_string
    sign_in_button.click()
    sleep(2)


for linkedin_url in linkedin_urls_YC:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//li[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first()

    job_title = sel.xpath('//h2/text()').extract_first()

    location = sel.xpath('//li[@class="t-16 t-black t-normal inline-block"]/text()').extract_first()

    linkedin_url = driver.current_url

    name = validate_field(name)
    job_title = validate_field(job_title)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)

    print '\n'
    print 'Name:'+name
    print 'Job Title:'+job_title
    print 'Location:'+location
    print 'URL:'+linkedin_url
    print '\n'

    writer.writerow([name.encode('utf-8'),
                     job_title.encode('utf-8'),
                     location.encode('utf-8'),
                     linkedin_url.encode('utf-8')])

    '''try:
        driver.find_element_by_xpath('//span[text()="Connect"]').click()
        sleep(3)

        driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
        sleep(3)

    except:
        pass'''

driver.quit()
