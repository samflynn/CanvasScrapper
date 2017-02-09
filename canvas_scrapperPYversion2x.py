# -*- coding: utf-8 -*-

import os
#import urllib2
from bs4 import BeautifulSoup as bs
#import mechanize
#import cookielib
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#import time
import re
import requests


def course_selector():
    print " "
    i = 0
    for code in num:
        print code  + " " + raw_name[i].string + " [" + str(i) + "]"
        i += 1
    print " "
    print "Enter number [ ] corresponding to the course you want to download or enter 400 to download all, if a list of courses hasn't been printed above, please run the program again." 
    number =  raw_input()
    #print type(number)
    if number == str(400):
        l = range(len(lnk))
        print "Courses selected: %s " % (l)
    else:
        print "Courses selected: %s " % (l)
        l = number.split()
        l = [int(a) for a in l]
        l.sort()
    course_downloader(l)



def course_downloader(l):
    #print l
    for a in l:
#       browser.get(lnk[a])
#        print num_lnk[num_lnk.keys()[a]]
        origi = os.getcwd()
        print "Creating folder: %s" % num[a]
        if not os.path.exists(num[a]):
                os.makedirs(num[a])
        os.chdir(num[a])
        browser.get(lnk[a])
        print browser.current_url
        course = bs(browser.page_source, 'html.parser')
        mod = course.findAll(True, {'class' : "item-group-condensed context_module student-view"})
        if not mod:
            #print "Empty"
            mod = course.findAll(True, {'class' : "item-group-condensed context_module "})
        #print mod[0]
        i = 0
        for n in mod:
            foldnme = mod[i].find(True, {"class" : "name"}).string
            print "Creating folder: %s" % foldnme
            origi2 = os.getcwd()
            if not os.path.exists(foldnme):
                   os.makedirs(foldnme)
            os.chdir(foldnme)
            # also add condition if the folder does exist then skip them all together 
            # Need to change directory to the new foldnme 
            # Create folder for subject name
            down = mod[i].findAll(True, {"class": "ig-title title"})
            j = 0
            for m in down:
                downlink = "https://sit.instructure.com" + down[j]['href']
                browser.get(downlink)
                downlink= browser.current_url
                file_creator(downlink)
                j += 1
            os.chdir(origi2)
            i +=1
        os.chdir(origi)
    
        
def file_creator(downlink):
#    os.mkdir(foldnme)

    text = downlink
    if "files" in text:
        text = re.findall("h.+[0-9](?=\?)", text)
        text = ' '.join(text)
        text = text + "/download?download_frd=1"
        # need to convert downlink to a actual downloadable link
        response = session.get(text)
        filename = re.findall("filename=\"(.+)\"", response.headers['content-disposition'])
        filename = ' '.join(filename)
        print "Creating file: %s" % filename
        if not os.path.isfile(filename):
            with open(filename, 'wb') as f:
                f.write(response.content)
    else: 
        print " "
        
#    os.chdir(origi)

print " "
print "###################################################################"
print "##                     Built by Shrey Mudgal                     ##"
print "##                    Built under Python - 2.7                   ##"
print "## Dependancies: os BeautifulSoup PhantomJs Selenium re requests ##"
print "###################################################################"
print " "

#origi = os.getcwd()
cd = os.getcwd() + r"\phantomjs-2.1.1-windows\bin\phantomjs.exe"
#phantomjs = origi + "\phantomjs-2.1.1-windows\bin\phantomjs.exe"
browser = webdriver.PhantomJS(cd)

print " "
browser.get("https://sit.instructure.com")
print "This \"https://shibboleth.stevens.edu/idp/Authn/UserPassword\" should be printed below, else there is some issue with the Internet connection or PhantomJs or the program needs to be run as Admin"
print browser.current_url 

print "Enter stevens Username"
user = raw_input() 
print "Enter Password"
passw = raw_input()

username = browser.find_element_by_name("j_username")
password = browser.find_element_by_name("j_password")

username.send_keys(user)
password.send_keys(passw)

#username.send_keys("")
#password.send_keys("")

login_attempt = browser.find_element_by_xpath("//*[@type='submit']")

login_attempt.submit()

print "This \"https://sit.instructure.com\" should be printed below, to show successfull login"
print browser.current_url
if browser.current_url != "https://sit.instructure.com/":
    quit()
    
main= bs(browser.page_source, 'html.parser')
session = requests.Session()
cookies = browser.get_cookies()

for cookie in cookies: 
    session.cookies.set(cookie['name'], cookie['value'])

num = []
lnk = []

for link in main.findAll('a', {'class' : 'ic-DashboardCard__link'}):
    flink = "https://sit.instructure.com" + link['href'] + "/modules"
    lnk.append(flink)
    num.append(link.string)

raw_name = main.findAll(True, {'class' : "ic-DashboardCard__header-subtitle ellipsis"})

#print raw_name
#print lnk
#print num

course_selector()




#==============================================================================
# br = mechanize.Browser()
# cj = cookielib.LWPCookieJar()
# br.set_cookiejar(cj)
# 
# br.set_handle_equiv(True)
# br.set_handle_gzip(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
# br.set_handle_robots(False)
# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# 
# br.addheaders = [('User-agent', 'Chrome')]
# 
# 
# br.open('https://shibboleth.stevens.edu/idp/Authn/UserPassword')
# 
# for f in br.forms():
#     print f
# 
#==============================================================================

#==============================================================================
# num_nme ={}
# 
# for name in soup.findAll('a', {'class' : "ic-DashboardCard__header-subtitle ellipsis"}):
#     
#==============================================================================


#wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
#
#page = urllib2.urlopen(wiki)
#
#soup = bs(page)

#browser = webdriver.Firefox('C:/geckodriver/geckodriver.exe')

#browser = webdriver.Chrome('C:/chromedriver/chromedriver.exe')




