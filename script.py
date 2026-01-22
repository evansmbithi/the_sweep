
# https://github.com/SergeyPirogov/webdriver_manager

import time, sys

from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains


# create a .env file with USERID, PASSWORD and COUNTRY variables
config = dotenv_values(".env")

# options = webdriver.ChromeOptions()
options = webdriver.EdgeOptions()
options.accept_insecure_certs = True # (firefox)
options.add_argument('--ignore-ssl-errors=yes') #ignore privacy issues
options.add_argument('--ignore-certificate-errors') #ignore certificate errors (chrome)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# try:
#     mode = sys.argv[3]
#     if mode.lower() in '--headless=true full':
#         options.add_argument("--headless=new")
#         print('--headless=TRUE')
#     else:
#         print('--headless=FALSE')       
# except:
#     options.add_argument("--headless=new")
#     print('--headless=TRUE')
    

# countries = ['rwanda rw','kenya ke','malawi mw','botswana bw','zambia zm']

try:
    cmdline=sys.argv[1]
    # cmdline2=sys.argv[2]    
except:
    err_msg = """Please specify mode as a commandline argument e.g
                'python script.py unfollow'
                'python script.py f4f'
                'python script.py 4llo'"""
    print(err_msg)
    exit()

# if cmdline.lower() in 'botswana bw' and cmdline2.lower() in 'production':
#     hostname = config['BW_PROD']
# if cmdline.lower() in 'rwanda' and cmdline2.lower() in 'production':
#     hostname = config['RW_Aos2_PROD']
# elif cmdline2.lower() in 'production':
#     hostname = config['PROD']
# else:
#     hostname = config['UAT']

# if cmdline not in "".join(countries):
#     print(f'{cmdline} is not in scope')
#     exit()
  
# driver = webdriver.Edge('../msedgedriver', options=options)
# driver = webdriver.Edge(service=EdgeService(executable_path=r'C:\Users\eikindu\Downloads\automation\msedgedriver.exe',service_args=['--log-level=DEBUG','--disable-build-check'],log_output='logs'),options=options)
try:
    # driver = webdriver.Chrome('../chromedriver',options=options)
    # driver = webdriver.Edge('../msedgedriver',service=EdgeService(service_args=['--log-level=DEBUG','--disable-build-check'],log_output='logs'),options=options) # Deprecated
    driver = webdriver.Edge(service=EdgeService(executable_path=r'D:\PROJECTS\the_sweep\msedgedriver.exe',service_args=['--log-level=DEBUG','--disable-build-check'],log_output='logs'),options=options)
except:
    print('Trying to fetch web driver...')
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # use Edge instead
    # https://pypi.org/project/webdriver-manager/#use-with-edge
    try:
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install(),service_args=['--log-level=DEBUG','--disable-build-check'],log_output='logs'),options=options)
    except:
        print('Please update msedgedriver on AUTOMATION/ to proceed')
        exit()
    
# wait time before throwing a Timeout Exception 
driver.implicitly_wait(3) # seconds

# wait for a certain condition to occur before proceeding further in the code
wait = WebDriverWait(driver, 30) # explicit wait

def check_configs():
    try:
        config['USERID']
        config['PASSWORD']
    except KeyError:
        print("Please configure .env with USERID, PASSWORD, PROD and UAT variables")
        driver.close()
        exit()

def error_page():
    try:
        error_msg = driver.find_element(By.CSS_SELECTOR, "div#content.ng-scope").text
        content_wrapper = driver.find_element(By.CSS_SELECTOR, "div#content-wrapper").get_attribute("innerHTML")
    except:
        return True

    if 'Authentication scheme not supported' in error_msg or content_wrapper == False or content_wrapper == None:
        return True
    else:
        return False

def login():

    check_configs()

    driver.maximize_window()
    try:
        # driver.get(f"{hostname}/login")
        driver.get(f"https://www.instagram.com")
    except:
        print('website is not reachable')

    # while error_page():
    #     driver.refresh() # https://www.codespeedy.com/how-to-refresh-or-reload-a-webpage-in-selenium-python/
    #     # print('Skipping error page')
        
    # time.sleep(2)
    print('Login page ✅')
    try:
        intfc = False
        while intfc != True:
            try:
                # userid = wait.until(EC.visibility_of_element_located((By.name, 'email')))
                # userid = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="email"]')))
                userid = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]'))) #
                intfc = True
            except:
                driver.refresh()
                intfc = False
            finally:
                userid = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]'))) #
                intfc = True

        password = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="password"]'))) #

        # password = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="pass"]')))

        login = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]'))) #

        # login = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@role="button"]')))
    except:
        print('Elements not found in login page')
    try:
        userid.send_keys(config['USERID'])    
        password.send_keys(config['PASSWORD'])    
    except:
        print('Please configure .env with USERID and PASSWORD')    

    time.sleep(3)
    try:
        login.click()
    except:
        print('login btn unclickable')

    lgn_suc = False
    while lgn_suc != True:
        try:
            profile = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/_.evnz_/?next=%2F']")))
            lgn_suc = True
        except:
            try:
                login.click()
                lgn_suc = False
            except:
                print('sth went wrong')
                exit()
    try:
        profile.click()
    except:
        print('profile button not found')
    
    print('Profile page ✅')
    time.sleep(3)


def unfollow_all():
    login()
    try:
        following = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/_.evnz_/following/?next=%2F"]')))
        following.click()
    except:
        print('following button not found')

    following_count = int(str(following.text).replace('following', '').replace(',','').strip())
    print(following.text)

    print('Following dialog ✅')


    time.sleep(5)
    dialog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    time.sleep(2)

    last_item = False
    while last_item != True:
        # Method 1: Scroll using JavaScript 
        for i in range(following_count): # scroll multiple times 
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 300;", dialog) 
            # time.sleep(1)
            # print(i)

        # items = dialog.find_elements(By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a")
        items = WebDriverWait(dialog, 10).until( EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(3) button") ) )
        print(len(items))

        if len(items) >= 1000:
            print(len(items))
            last_item = True
        
    print('Scrolling through ✅')


    for item in items: 
        ActionChains(driver).move_to_element(item).perform() 
        time.sleep(1)
        item.click()

        confirm_unfollow = WebDriverWait(item, 10).until( EC.element_to_be_clickable( (By.XPATH, "//button[@CLASS='_a9-- _ap36 _a9-_']") ) )
        confirm_unfollow.click()
        time.sleep(2)


def f4f():
    login()
    try:
        followers = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/_.evnz_/followers/?next=%2F"]')))
        followers.click()
    except:
        print('followers button not found')

    time.sleep(5)
    dialog = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    time.sleep(2)

    last_item = False
    while last_item != True:
        # Method 1: Scroll using JavaScript 
        for i in range(500): # scroll multiple times 
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 300;", dialog) 
            # time.sleep(1)
            # print(i)

        # items = dialog.find_elements(By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a")
        items = WebDriverWait(dialog, 10).until( EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) button") ) )
        print(len(items))

        if len(items) >= 200:
            print(len(items))
            last_item = True
        
    print('Scrolling through ✅')


    for item in items: 
        ActionChains(driver).move_to_element(item).perform() 
        time.sleep(1)
        item.click()

        # confirm_unfollow = WebDriverWait(item, 10).until( EC.element_to_be_clickable( (By.XPATH, "//button[@CLASS='_a9-- _ap36 _a9-_']") ) )
        # confirm_unfollow.click()
        # time.sleep(2)

if cmdline.lower() in 'unfollow_all':
    unfollow_all()
elif cmdline.lower() in '4llo f4f':
    f4f()









# check_follows = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mount_0_0_Pg']/div/div/div[2]/div/div/div[1]/div[2]/div[2]/section/main/div/div/header/div/section[2]/div/div[2]/div[3]/a")))
# check_follows.click()
# time.sleep(3)
# is_evnz = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div/span/div/a/div/div/span")))

# if '_.evnz_' not in is_evnz.text:
#     close_dialog = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button")))
#     close_dialog.click()
#     unfollow_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button")))

# break



# user_list = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div'))) 



time.sleep(3600)