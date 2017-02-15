# -*- coding: utf-8 -*-
import getpass
import os
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import requests
# from creds import USERNAME, PASSWORD

def course_selector():
    """
    Lists out all the courses available for in student profile
    """
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
        print "Courses selected: %s " % (number)
        l = number.split()
        l = [int(a) for a in l]
        l.sort()

    course_downloader(l)

def course_downloader(l):
    for a in l:
        origi = os.getcwd()

        print "Creating folder: %s" % num[a]
        
        if not os.path.exists(num[a]):
                os.makedirs(num[a])
        os.chdir(num[a])
        
        browser.get(lnk[a])
        course = bs(browser.page_source, 'html.parser')
        mod = course.findAll(True, {'class' : "item-group-condensed context_module student-view"})
        if not mod:

            mod = course.findAll(True, {'class' : "item-group-condensed context_module "})
        
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

print " "
print "###################################################################"
print "##                     Built by Shrey Mudgal                     ##"
print "##                    Built under Python - 2.7                   ##"
print "## Dependancies: os BeautifulSoup PhantomJs Selenium re requests ##"
print "###################################################################"
print " "

#origi = os.getcwd()
supported_os = {"1": "Windows", "2": "OSX"}
your_os = None
while your_os not in supported_os.keys():
    your_os = raw_input("Please choose your operating system number (1 or 2):\n1.Windows\n2.OSX\n\n>>")


if your_os == '1':
    cd = os.getcwd() + r"\phantomjs-2.1.1-windows\bin\phantomjs.exe"
elif your_os == '2':
    cd = os.getcwd() + r"/phantomjs-2.1.1-macosx/bin/phantomjs"
else:
    pass

browser = webdriver.PhantomJS(cd)

print " "
browser.get("https://sit.instructure.com")
print "This \"https://shibboleth.stevens.edu/idp/Authn/UserPassword\" should be printed below, else there is some issue with the Internet connection or PhantomJs or the program needs to be run as Admin"
print browser.current_url 

student_username = None
student_password = None

while not student_username:
    student_username = raw_input("Enter stevens Username\n>> ") 

while not student_password:
    student_password = getpass.getpass(prompt="Please enter your MyStevens password\n>>")


username = browser.find_element_by_name("j_username")
password = browser.find_element_by_name("j_password")

username.send_keys(student_username)
password.send_keys(student_password)

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

course_selector()