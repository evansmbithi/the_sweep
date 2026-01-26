
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
from selenium.webdriver.common.keys import Keys


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


def check_configs():
    try:
        config['USERID']
        config['PASSWORD']
    except KeyError:
        print("Please configure .env with USERID, PASSWORD, PROD and UAT variables")
        exit()



def login():         
    global wait
    global driver
    intfc = False
    while intfc != True:
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
        wait = WebDriverWait(driver, 10) # explicit wait
        check_configs()

        driver.maximize_window()
        try:
            # driver.get(f"{hostname}/login")
            driver.get(f"https://www.instagram.com")
        except:
            print('website is not reachable')
        try:
            # userid = wait.until(EC.presence_of_element_located((By.name, 'email')))
            # userid = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
            userid = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))) #
            intfc = True
        except:
            # driver.refresh()
            driver.close()
            driver.quit()
            print('Browser restart')
            intfc = False

    try:
        password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))) #

        # password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="pass"]')))

        login = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))) #

        # login = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="button"]')))
    except:
        print('Elements not found in login page')
        exit()
    try:
        userid.send_keys(config['USERID'])    
        password.send_keys(config['PASSWORD'])    
    except:
        print('Please configure .env with USERID and PASSWORD')
        exit()    

    print('Login page ✅')
    
    time.sleep(3)
    try:
        login.click()
    except:
        print('login btn unclickable')

    global get_user
    lgn_suc = False
    while lgn_suc != True:
        try:
            profile = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/_.evnz_/?next=%2F']")))
            get_user = '_.evnz_'
            lgn_suc = True
        except:
            try:
                
                # profile = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()='Profile']")))
                profile = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xt0psk2 x3ct3a4 xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x4gyw5p _a6hd']")))[8]
                get_user_link = str(profile.get_attribute('href'))
                get_user = get_user_link.replace('https://www.instagram.com/','').replace('/','')
                print(get_user)
                lgn_suc = True
            except:
                try:
                    login = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
                    login.click()
                except:
                    lgn_suc = False


    try:
        profile.click()
    except:
        print('profile button not found')
    
    print('Profile page ✅')
    time.sleep(2)


def f4f():
    login()
    try:
        followers = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/_.evnz_/followers/?next=%2F']")))
        followers.click()
    except:
        try:
            followers = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{get_user}/followers/?next=%2F']")))
            followers.click()
        except:
            print('followers button not found')
    followers_count = int(str(followers.text).replace('followers', '').replace(',','').strip())
    print(followers.text)

    # try:
    #     # time.sleep(3)
    #     disclaimer = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "Report a problem")))
    #    # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "button + button") ) )
    #     ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
    #     ignore_disclaimer.click()
    #     print('Disclaimer ✅')
    # except:
    #     print('Disclaimer not found')

    time.sleep(5)
    dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    time.sleep(2)

    

    last_item = False
    while last_item != True:
        # Method 1: Scroll using JavaScript 
        for i in range(followers_count): # scroll multiple times 
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 300;", dialog) 
            # time.sleep(1)
            # print(i)

        # items = dialog.find_elements(By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a")
        items = WebDriverWait(dialog, 50).until( EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) button") ) )
        print(len(items))

        if len(items) >= len(items)-5:
            print(len(items))
            last_item = True
        
    print('Scrolling through ✅')


    for item in items: 
        ActionChains(driver).move_to_element(item).perform() 
        time.sleep(1)
        item.click()

        # try:
        #     # time.sleep(3)
        #     disclaimer = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "Report a problem")))
        #     # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "button + button") ) )
        # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
        #     ignore_disclaimer.click()
        #     print('Disclaimer ✅')
        # except:
        #     print('Disclaimer not found')

        # confirm_unfollow = WebDriverWait(item, 10).until( EC.element_to_be_clickable( (By.XPATH, "//button[@CLASS='_a9-- _ap36 _a9-_']") ) )
        # confirm_unfollow.click()
        # time.sleep(2)

def unfollow_all():
    login()
    try:
        following = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/_.evnz_/following/?next=%2F']")))
        following.click()
    except:
        try:
            following = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{get_user}/following/']")))
            following.click()
        except:
            print('following button not found')

    following_count = int(str(following.text).replace('following', '').replace(',','').strip())
    print(following.text)

    print('Following dialog ✅')

    try:
        # time.sleep(3)
        disclaimer = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "Report a problem")))
        # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "button + button") ) )
        ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
        ignore_disclaimer.click()
        print('Disclaimer ✅')
    except:
        print('Disclaimer not found')


    time.sleep(5)
    dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    time.sleep(2)

    last_item = False
    while last_item != True:
        # Method 1: Scroll using JavaScript 
        for i in range(20): # scroll multiple times 
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

def balance():
    login()
    try:
        following = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/_.evnz_/following/?next=%2F']")))
        following.click()
    except:
        try:
            following = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@href='/{get_user}/following/']")))
            following.click()
        except:
            print('following button not found')

    following_count = int(str(following.text).replace('following', '').replace(',','').strip())
    print(following.text)

    print('Following dialog ✅')

    # try:
    #     # time.sleep(3)
    #     disclaimer = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.LINK_TEXT, "Report a problem")))
    #     # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.element_to_be_clickable( (By.CSS_SELECTOR, "button + button") ) )
    #     ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
    #     ignore_disclaimer.click()
    #     print('Disclaimer ✅')
    # except:
    #     print('Disclaimer not found')


    time.sleep(2)
    dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    time.sleep(2)

    last_item = False
    while last_item != True:
        # Method 1: Scroll using JavaScript 
        for i in range(following_count): # scroll multiple times 
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 300;", dialog) 
            # time.sleep(1)
            # print(i)

        # items = dialog.find_elements(By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a")
        # items = WebDriverWait(dialog, 10).until( EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(3) button") ) )
        
        items = WebDriverWait(dialog, 10).until( EC.presence_of_all_elements_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a") ) )
        print(len(items))

        if int(len(items)) >= 700:
            print(len(items))
            last_item = True
        
    print('Scrolling through ✅')


    for item in items:   
        print('follows loop ✅')
        # Grab the href so we can revisit it later 
        clicked_url = str(item.get_attribute("href")) 
        time.sleep(1)

        ActionChains(driver).move_to_element(item).perform() 
        time.sleep(0.5)
        # item.click()
        ig_user=item.text
        if ig_user == '':
            continue
        # print(ig_user)

        # Step 3: Open the link in a new tab using CONTROL + click (COMMAND on Mac) 
        ActionChains(driver).key_down(Keys.CONTROL).click(item).key_up(Keys.CONTROL).perform() 
        time.sleep(1) # wait for the new tab to open
        
        # Step 3: Switch to the new window/tab 
        original_window = driver.current_window_handle 
        all_windows = driver.window_handles 
        for window in all_windows: 
            if window != original_window: 
                driver.switch_to.window(window) 
                break 
        
        time.sleep(1)
        # Step 4: Do something in the new tab (optional) 
        parts = clicked_url.split("?") # [' /nesser_verse/', 'next=%2F'] 
        path = parts[0] # '/nesser_verse/' 
        try:
            query = parts[1] # 'next=%2F' 
            # Remove trailing slash, add '/following/' 
            new_path = path.rstrip("/") + "/following/" 
            modified_url = new_path + "?" + query
        except:
            print('next=%2F not found')
            query=''
            # Remove trailing slash, add '/following/' 
            new_path = path.rstrip("/") + "/following/" 
            modified_url = new_path
        # Modify the path 
        
        # Rebuild the URL 
        path_with_query = modified_url.split("instagram.com")[-1]
        # print(path_with_query)
        time.sleep(2)
        

        try:
            check_follows = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, f"//a[@href='{path_with_query}']")))
            check_follows.click()
        # except:
        #     try:
        #         time.sleep(2)
        #         disclaimer = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, "Report a problem")))
        #         # ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "button + button") ) )
        #         ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
        #         ignore_disclaimer.click()
        #         print('Disclaimer ✅')
            # except:
            #     try:
            #         print('Disclaimer not found')
            #         driver.refresh()
            #         time.sleep(3)
            #         check_follows = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, f"//a[@href='{path_with_query}']")))
            #         check_follows.click()
        except:
            print('following button not found')
            time.sleep(2)
            x=False
            while x!=True:
                for window in all_windows: 
                    try:
                        if window != original_window:                     
                            driver.close() 
                            continue
                        else: 
                            x=True
                    except:
                        x=False 
            time.sleep(1)

            # Step 6: Switch back to the original window 
            driver.switch_to.window(original_window) 
            time.sleep(2)
            continue
        

        time.sleep(1)
        try:
            go_to_dialog = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='x6nl9eh x1a5l9x9 x7vuprf x1mg3h75 x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))

            time.sleep(1)
            is_evnz = WebDriverWait(go_to_dialog, 5).until( EC.presence_of_element_located( (By.CSS_SELECTOR, "div > div > div > div > div > div > div:nth-child(2) a span") ) )
            # print(is_evnz.text)
            time.sleep(1)
            # print(get_user)
        except:
            print('Unknown error')
            time.sleep(2)
            x=False
            while x!=True:
                for window in all_windows: 
                    try:
                        if window != original_window:                     
                            driver.close() 
                            continue
                        else: 
                            x=True
                    except:
                        x=False 
            time.sleep(1)

            # Step 6: Switch back to the original window 
            driver.switch_to.window(original_window) 
            time.sleep(2)
            continue

        if f'_.evnz_' not in is_evnz.text:
            print(f'{get_user} != {is_evnz.text}')
            try:
                close_dialog = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='html-div xdj266r x14z9mp xat24cr x1lziwak xexx8yu x18d9i69 x9f619 xjbqb8w x78zum5 x15mokao x1ga7v0g x16uus16 xbiv7yw xf159sx xmzvs34 x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1']/button")))
                close_dialog.click()
            except:
                try:
                    # time.sleep(3)
                    disclaimer = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.LINK_TEXT, "Report a problem")))
                    ignore_disclaimer = WebDriverWait(disclaimer, 2).until( EC.visibility_of_element_located( (By.XPATH, "following-sibling::button") ) )
                    ignore_disclaimer.click()
                    print('Disclaimer ✅')
                except:
                    print('Disclaimer not found')
                    driver.refresh()

            time.sleep(1)
            unfollow_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//section[@class='x14vqqas x172qv1o']/div/div/div/div/div/button")))
            unfollow_dropdown.click()
            
            time.sleep(1)
            unfollow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1ja2u2z x1afcbsf x1a2a7pz x6ikm8r x10wlt62 x71s49j x6s0dn4 x78zum5 xdt5ytf xl56j7k x1n2onr6']/div/div/div/div/div/div[8]")))
            unfollow_button.click()


            print(f"Unfollowed:'{ig_user}'") 
            time.sleep(2)
            
            x=False
            while x!=True:
                for window in all_windows: 
                    try:
                        if window != original_window:                     
                            driver.close() 
                            continue
                        else: 
                            x=True
                    except:
                        x=False 
            time.sleep(1)

            # Step 6: Switch back to the original window 
            driver.switch_to.window(original_window) 
            time.sleep(2)
            continue
            

        else:
            time.sleep(2)
            x=False
            while x!=True:
                for window in all_windows: 
                    try:
                        if window != original_window:                     
                            driver.close() 
                            continue
                        else: 
                            x=True
                    except:
                        x=False  
            time.sleep(1)

            # Step 6: Switch back to the original window 
            driver.switch_to.window(original_window) 
            time.sleep(2)
            continue
            
        # # Step 7: Navigate back to the clicked URL (the link’s href) 
        # clicked_url = link.get_attribute("href") 
        # driver.get(clicked_url) 
        # # Keep browser open for a while to observe 
        # time.sleep(5)

        # confirm_unfollow = WebDriverWait(item, 10).until( EC.element_to_be_clickable( (By.XPATH, "//button[@CLASS='_a9-- _ap36 _a9-_']") ) )
        # confirm_unfollow.click()
        

 

if cmdline.lower() in 'unfollow_all':
    unfollow_all()
elif cmdline.lower() in '4llo f4f':
    f4f()
elif cmdline.lower() in 'balance':
    balance()










# break



# user_list = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div[1]/div'))) 


print('DONEEEE🤣')
time.sleep(3600)