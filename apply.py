import os # to get the resume file
import time # to sleep
import glassdoor_test
import csv
import re






# Fill in this dictionary with your personal details!
JOB_APP = {
    "first_name": "Joe",
    "last_name": "Mother",
    "email": "",
    "phone": "",
    "org": "",
    "resume": "resume.pdf",
    "resume_textfile": "",
    "linkedin": "",
    "website": "",
    "github": "",
    "twitter": "",
    "location": "Chicago, IL, United States",
    "city": "",
    "state": "IL",
    "ZIP":"",
    "address":"",
    "grad_month": '05',
    "grad_year": '2020',
    "pay": '60000',
    "university": "",
    "username": "",
    "password": ""
}

#fills out all fields in a glassdoor easy apply job
def glassdoor(driver):
    #login 
    login(driver)
    time.sleep(1)

    #can't yet tell if you've actually applied
    sucsess = True
     
    try:
        #bring up easy apply form
        driver.find_element_by_xpath("//*[@id='JobView']/div[1]/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/button").click()
        
    except NoSuchElementException:
        pass
    
    time.sleep(1)
    
    #resume must come first because it deletes everything else, and we don't know where it is always 
    resume(driver)

    #any extra questions, can also be matched to your needs
    try:
        for i in range(15):
            glassdoor_easy_questions(driver, divnum= i +1)
    except Exception:
        pass
        
    try:
        #noads
        driver.find_element_by_xpath("//*[@id='ApplySection']/div[2]/label/div").click()
        
    except NoSuchElementException:
        pass



    try:
        #noads2
        driver.find_element_by_xpath("//*[@id='ApplySection']/div[3]/label/div").click()
        
    except NoSuchElementException:
        pass
    
    
    try:
        #apply
        driver.find_element_by_xpath("//*[@id='ApplyContainer']/div/div[2]/div/div[2]/div/div[2]/form/div[2]/div[2]/div[2]/button").click()

        time.sleep(.5)

    except NoSuchElementException:
        sucsess = False



    
def glassdoor_easy_questions(driver,divnum):
    #for each question number we cycle through if statements to try and figure out what kind of question it is, and answer 
    try:
        quest = driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]").text
        
        time.sleep(.2)
        
        if(re.search("authorized", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/label[1]/div[1]").click()
            
        elif(re.search("sponsorship", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/label[2]/div[1]").click()

        elif(re.search("Bachelor's", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/label[1]/div[1]").click()
            
        elif(re.search("experience", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/label[2]/div[1]").click()
            
        elif(re.search("loca", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/label[2]/div[1]").click()

        elif(re.search("[Ee]mail", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['email'])    
            
        elif(re.search("name", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['first_name'] + " " + JOB_APP['last_name'])  
     
            if(re.search("first.*name", quest, re.IGNORECASE)):
                driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
                driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['first_name'])  
    
    
            elif(re.search("last.*name", quest, re.IGNORECASE)):
                driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
                driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['last_name'])   


        elif(re.search("phone.*number", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['phone']) 

        elif(re.search("state", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['state'])               

        elif(re.search("city", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['city']) 
            
        elif(re.search("zip", quest, re.IGNORECASE) or re.search("postal", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['ZIP']) 
            
        elif(re.search("address", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['address']) 
            
        elif(re.search("Linked.?In", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['linkedin'])  
            
        elif(re.search("[cC]ountry", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/div").click()  
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/ul/li[2]").click()  
            
        elif(re.search("Create a job alert", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/div").click()  
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/ul/li[2]").click()  
            

        elif(re.search("[dD]esired.*[pP]ay", quest, re.IGNORECASE) or re.search("salary", quest, re.IGNORECASE)):
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").clear()
            driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(divnum)+"]/div/input").send_keys(JOB_APP['pay'])  


    except NoSuchElementException:
        pass
    
    
def resume(driver):
    try:
        for i in range(15):
            quest = driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(i+1)+"]").text
            if(re.search("resume", quest, re.IGNORECASE)): 
                driver.find_element_by_xpath("//*[@id='ApplyQuestions']/div["+str(i+1)+"]/div[2]/a").click()
                time.sleep(.25)
                driver.find_element_by_xpath("//*[@id='file']").send_keys(os.getcwd()+"/resume.pdf")
                time.sleep(.25)
                break
                
                
    except NoSuchElementException:
        pass
            
        
        
    
    
def login(driver):

    
 
    try:
        #login
        driver.maximize_window()
        driver.find_element_by_xpath("//*[@id='TopNav']/nav/div[2]/ul[3]/li[2]/a").click()
        
        time.sleep(.5)
        
        #login
        username_field = driver.find_element_by_xpath("//*[@id='userEmail']")
        password_field = driver.find_element_by_xpath("//*[@id='userPassword']")
        
        username_field.clear()
        password_field.clear()
        
        username_field.send_keys(JOB_APP['username'])
        password_field.send_keys(JOB_APP['password'])
        
        driver.find_element_by_xpath("//*[@id='LoginModal']/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/form/div[3]/div[1]").click()

        time.sleep(.5)
        
    except NoSuchElementException:
        pass



    
    
def main(): 
    driver = webdriver.Chrome(executable_path='add your webdriver path')
        
        
    applied = ''
    # call get_links to automatically scrape job listings from glassdoor
    aggregatedURLs = get_links.getURLs()    
        
    driver.get(list(aggregatedURLs)[0])
    driver.maximize_window()
    login(driver)
    
    with open('my_file.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Job_title", "Company", "Location" , "Job_text","Outcome"])

        for url in aggregatedURLs:    
            print('\n')
            driver.get(url)
            
            #save application data in a csv
            try:
                text = driver.find_element_by_xpath("//*[@id='JobDescriptionContainer']").text
    
                job_title = driver.find_element_by_xpath("//*[@id='JobView']/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]").text
    
                company = driver.find_element_by_xpath("//*[@id='JobView']/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]").text
    
                location = driver.find_element_by_xpath("//*[@id='JobView']/div[1]/div[2]/div/div/div[2]/div[1]/div[1]/div[2]/div/div/div[3]").text
                writer.writerow([str(job_title), str(company), str(location), str(text), 000])
                    
            except Exception:
                pass
            
            
            #apply to url
            try:
                glassdoor(driver)
                print(f'SUCCESS FOR: {url}')
                applied = applied + url + ','
            except Exception:
                print(f"FAILED FOR {url}")
                continue
            

    f.close()
    driver.close()


    
main()
 

  
    
    


    
    
