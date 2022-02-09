#required imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.by import By

#Insert your data
YOUR_EMAIL='email'
YOUR_PASSWORD='pass'

#open driver
PATH_TO_DRIVER = './chromedriver' # chrome version 98 change the chromium if you use a different version
driver = webdriver.Chrome(executable_path=PATH_TO_DRIVER)#,options=chrome_options)


#launch url using driver
driver.get('https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2Fb%3Fnode%3D12935593031%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')

session_id = driver.session_id
print(session_id)

#email
input1 = driver.find_element(By.XPATH,'//*[@id="ap_email"]')
actions = ActionChains(driver)
actions.move_to_element(input1).send_keys(YOUR_EMAIL).perform()

#next step
driver.find_element(By.XPATH,'//*[@id="continue"]').click()

#password
input2 = driver.find_element(By.XPATH,'//*[@id="ap_password"]')
actions = ActionChains(driver)
actions.move_to_element(input2).send_keys(YOUR_PASSWORD).perform()

#login
driver.find_element(By.XPATH,'//*[@id="signInSubmit"]').click()

#wait loading
sleep(1)

#go to amazon photos
driver.get('https://www.amazon.it/photos/all')

# Scrolling height implement some logic to calculate or just input a really long value (i just scrolled to the end my
# photo library and in the console typed the command : document.body.scrollHeight)
total_height = 2522684

#Init some used variables
buttonClicks= 0
maxClick=1000

#Utuils Method
def clickButtonAction():
    try:
        driver.find_element(By.XPATH,'//*[@id="photos"]/header/div/section[2]/button[3]').click() #Delete button
        sleep(2) #Wait popup to be displayed
        driver.find_element(By.XPATH,'//*[@id="dialog-container"]/div[1]/div/aside/footer/div/button[2]').click() #Confirm delete button
        print('Delete complete')
    except:
        print('Error on clicking the delete button ',str(delBtn))

def maxReached():
    if(buttonClicks >= maxClick):
        print('Stop max item reached')
        clickButtonAction()
        sleep(70) #Think time of amazon to delete ~ it isn't accurate but works 99% of the times
        buttonClicks = 0 # Reset clicks
    else:
        driver.execute_script("arguments[0].click()", buttons[j]) #Execute click
        buttonClicks +=1
        print('buttonClicks: '+str(buttonClicks))


# Start
for i in range(1, total_height, 100): #keep scrolling the window
    driver.execute_script("window.scrollTo(0, {});".format(i))
    #select all photos
    buttons = driver.execute_script("return document.querySelectorAll('div.selector:not(.selected)')")

    maxReached()

    for j in range (0,len(buttons)-1):
        try:
            maxReached()
        except:
            print('Error on clicking the photo: ',str(buttons[j]))
    sleep(0.5) # Adjust the speed, too fast may skip some photos