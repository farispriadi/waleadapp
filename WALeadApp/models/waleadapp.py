import argparse
import copy
import datetime
import filetype
import math
import os
import pandas as pd
import pathlib
import re
import shutil
import signal
import subprocess
import sys
import time
from collections import OrderedDict

from emoji import UNICODE_EMOJI
from phone_iso3166.country import phone_country

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException
from config import BASE_PATH, ROOT_PATH
from wawebxpath import WAXPATH

WEBDRIVER_PATH = ROOT_PATH.joinpath("chromedriver_autoinstaller").resolve()


def is_phone(mobile_number):
    # txt = "+6282121325532"
    matching = re.search("^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{2,3})[-. )]*(\d{3,4})[-. ]*(\d{2,3})(?: *x(\d+))?\s*$", mobile_number)
    return matching

def get_platform_architecture():
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return platform, architecture

def check_chrome_version():
    """
    :return: the version of chrome installed on client

    https://github.com/yeongbin-jo/python-chromedriver-autoinstaller
    """
    platform, _ = get_platform_architecture()
    if platform == 'linux':
        chromium = False
        try:
            with subprocess.Popen(['chromium-browser', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').replace('Chromium', '').strip()
                version = version.replace('Google Chrome', '').strip()
                chromium = True
        except:
            pass # No chromium

        if not chromium:
            with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').strip()
                version = version.replace('Google Chrome', '').strip()
                chromium = True

    elif platform == 'mac':
        process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google Chrome', '').strip()
    elif platform == 'win':
        process = subprocess.Popen(
            ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )
        output = process.communicate()
        if output:
            version = output[0].decode('UTF-8').strip().split()[-1]
        else:
            process = subprocess.Popen(
                ['powershell', '-command', '$(Get-ItemProperty -Path Registry::HKEY_CURRENT_USER\\Software\\Google\\chrome\\BLBeacon).version'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            version = process.communicate()[0].decode('UTF-8').strip()
    else:
        return 
    return version

def get_major_version(version):
    """
    :param version: the version of chrome
    :return: the major version of chrome
    """
    if version:
        return version.split('.')[0]
    return

current_platform, _ = get_platform_architecture()
version_detail = check_chrome_version()
version = get_major_version(version_detail)

if "win" in get_platform_architecture():
    WEBDRIVER_FILENAME = "chromedriver.exe" # chrome or firefox
    USER_DATA_PATH = os.path.join(os.environ['USERPROFILE'],"AppData","Local","WALeadApp","User_Data")
else:
    WEBDRIVER_FILENAME = "chromedriver" # chrome or firefox
    USER_DATA_PATH = "./User_Data"
if version:
    try:
        CHROMEDRIVER_PATH = str(WEBDRIVER_PATH.joinpath(version,WEBDRIVER_FILENAME).resolve())
        chromedriver_file = pathlib.Path(CHROMEDRIVER_PATH)
        if not chromedriver_file.exists():
            CHROMEDRIVER_PATH = None
    except FileNotFoundError as e:
        CHROMEDRIVER_PATH = None
else:
    CHROMEDRIVER_PATH = None
    

template = str(BASE_PATH.joinpath("template","messages.txt").resolve())
CONTACTS_PATH = str(BASE_PATH.joinpath("contacts","contacts.csv").resolve())
REPORTS_PATH = BASE_PATH.joinpath("reports").resolve()
ATTACHMENT_PATH = BASE_PATH.joinpath("media").resolve()
URL = "https://web.whatsapp.com/"

wait = None
browser=None

def get_browser():
    global browser

    return browser

def convert_ID(mobile_number):
    """ Covert valid mobile to ID phone code"""
    number_str = ''.join(filter(str.isdigit, str(mobile_number)))
    if number_str[:2] != '62':
        number_str = '62'+number_str[1:]
    return number_str


def load_contacts(file_path=None, refine=True, column=None):
    """
    load from csv or excel 
    force refine mobile to ID

    return
    ------
    DataFrame object
    """
    try:
        path = pathlib.Path(file_path).suffix
        if path == ".csv":
            contact_df = pd.read_csv(file_path, dtype=str)
        else: #if excel
            contact_df = pd.read_excel(file_path, engine="openpyxl", dtype=str)
            is_NaN = contact_df.isnull()
            row_all_NaN = is_NaN.all(axis=1)
            contact_df = contact_df[~row_all_NaN]
    except:
        raise
        contact_df = pd.DataFrame()
    if refine and not contact_df.empty:
        if column is not None:
            contact_df[column] = contact_df[column].apply(convert_ID)
        elif "phone" in contact_df.columns:
            contact_df["phone"] = contact_df["phone"].apply(convert_ID)
        else:    
            contact_df["mobile"] = contact_df["mobile"].apply(convert_ID)
    return contact_df


def is_valid(mobile_number):
    """mobile has valid format (using country code)
        Support ID only country code
        Length must be 10, 11 or 12
    """
    number_str = ''.join(filter(str.isdigit, str(mobile_number)))
    if len(number_str) >9 and len(number_str)<= 12:
        """ Perlu cek ke provider"""
        try:
            country_code = phone_country(number_str)
            if country_code == 'ID':
                return True
        except Exception as e:
            print("error cek invalid",e)

    return False

def get_chat_data(chat_elements, token):
    global browser
    # get response
    chats = {'data_id':[], 'info':[], 'message':[], 'status': []}
    
    for id_chat,chat_element in enumerate(chat_elements):
        data_id = chat_element.get_attribute("data-id")
        chat_xpath = '{}/div[{}]'.format(WAXPATH["element"]["chat_boxes"],str(id_chat+1)) # chat_element

        try:
            image_element= chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box_image"]["image"])
            info_element = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box_image"]["info"])
            browser.implicitly_wait(20)
            status_element  = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box_image"]["status"])
            message_element = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box_image"]["message"])
            # print("Chat with image")
        except:
            info_element = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box"]["info"])
            browser.implicitly_wait(20)
            status_element  = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box"]["status"])
            message_element = chat_element.find_element_by_xpath(WAXPATH["element"]["chat_box"]["message"])
            # print("Chat Text")

        info = info_element.get_attribute('data-pre-plain-text')
        message = message_element.text
        status = str(status_element.get_attribute('aria-label')).strip()

        chats['data_id'].append(data_id)
        chats['info'].append(info)
        chats['message'].append(message)
        chats['status'].append(status)
        if data_id == token:
            break
    return chats

def get_response_by_token(token):
    """ fitur untuk mengambil percakapan respon by token"""
    global browser
    responses = {'data_id':[], 'info':[], 'message':[], 'status': []}
    # try:
    # ditambahkan scroll sampai paling bawah
    xpath = WAXPATH["element"]["chats_container_by_class"]
    parent = WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))

    browser.implicitly_wait(30)
    action = ActionChains(browser)
    count = 0
    while count < 5 and (token not in responses['data_id']):
        ## Scrolling chat
        for i in range(10):
            action.move_to_element(browser.find_element(By.XPATH, WAXPATH["element"]["first_chat_presented"])).perform()
            browser.implicitly_wait(10)

        # chats  = parent.find_elements_by_xpath('.//div[@data-id]')
        chats  = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, WAXPATH["element"]["chat_boxes"])))

        chats_visible_count=len(chats)
        chats.reverse()
        # list comp ini dapat diefisienkan dengan menambahkan for ch in chats.reverse
        # nilai big O kecil
        # chats_tokens = [chat.get_attribute("data-id") for chat in chats ]
        responses = get_chat_data(chats, token)
        count+=1

    id_chat_token = responses['data_id'].index(token)

    return responses

def get_token_message():
    try:
        ### Get chats
        ## Versi sebelumnya 
        # xpath = WAXPATH["chats_container_by_class"]
        # parent = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        # chats  = parent.find_elements_by_xpath('.//div[@data-id]')
        # Versi sekarang
        xpath = WAXPATH["element"]["chat_boxes"]
        chats  = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        ##
        latest_chat = chats[-1]
        data_id = latest_chat.get_attribute("data-id")
        return {'data_id': data_id}
    except Exception as e:
        print("Error get token : ", e)
    return None
    

#####  NOT USED
def get_search(list_token = []):
    result = False
    too_long = 0
    result_list = None
    while (not result and too_long <=5):
        try:
            result_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')))

            result_list = result_box.find_elements_by_xpath("./*")
            result = True
            too_long +=too_long
        except Exception as e:
            pass
    if too_long > 5:
        print("Wait too long!, Element does not existed")
    else:
        for idx in range(len(result_list)):
            not_message = False
            if idx == 0:
                try:
                    # number = browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div['+str(idx+1)+']/div/div/div[2]/div[1]/div[1]/span/span')
                    xpath = '//*[@id="pane-side"]/div[1]/div/div/div['+str(idx+1)+']/div/div/div[2]/div[1]/div[1]/span/span'
                    number = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    time_sent = browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div['+str(idx+1)+']/div/div/div[2]/div[1]/div[2]').text
                    number.click()
                except Exception as e:
                    not_message = True
                if not_message:
                    msg_title= browser.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div['+str(idx+1)+']/div').text
                responses = get_response_by_token(list_token[idx])


def search_by_message(message='', list_token=[]):
    # Search message
    # token_message = "Assalamualaikum, Halo, Nama saya"
    # search_box = browser.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    search_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/div/div[2]')))
    search_box.send_keys(message)
    search_box.send_keys(Keys.ENTER)
    get_search(list_token)
#####  END OF NOT USED


def compose_message(template, contact_df):

    messages = []
    template_without_parents = re.sub('\(.+?\)','',template) # remove parents

    # extract text in double curly bracket
    column_names = re.findall('{(.+?)}',template_without_parents)

    # make sure column header in lower case
    # column header must unique
    contact_df.columns = [str(col).lower() for col in contact_df.columns]

    for idx,row in contact_df.iterrows():
        message_text = template
        replaced_texts = row[column_names].index
        
        for txt in list(replaced_texts):
            message_text = message_text.replace("{"+txt+"}", str(row[txt]))
        messages.append(message_text)
    return messages

def whatsapp_login(chrome_path, headless):
    global wait, browser, URL
    print("Headless Mode:", headless)
    if browser is None:
        chrome_options = Options()
        user_data_dir_arg = "--user-data-dir={}".format(USER_DATA_PATH)
        # chrome_options.add_argument('--user-data-dir=./User_Data')
        chrome_options.add_argument(user_data_dir_arg)
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument("--start-maximized")
        if headless:
            chrome_options.add_argument('--headless')
        if chrome_path:
            browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        else:
            browser = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(browser, 600)

    try:
        browser.get(URL)
    except:
        chrome_options = Options()
        user_data_dir_arg = "--user-data-dir={}".format(USER_DATA_PATH)
        # chrome_options.add_argument('--user-data-dir=./User_Data')
        chrome_options.add_argument(user_data_dir_arg)
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument("--start-maximized")
        if headless:
            chrome_options.add_argument('--headless')

        browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        wait = WebDriverWait(browser, 600)
        browser.get(URL)

    print("QR scanned")
    

def get_saved_name(mobile):
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div/span')))
        saved_name = element.text
        if saved_name != str(mobile):
            return saved_name
    except Exception as e:
        print("Failed get name in saved contacts")
    return ''

# Method 2 : selective pick using regex
def extract_emoji(message):
    """
    get emoji list from template message
    
    note: only emoji unicode and backslash not escape
    """
    exclude_emoji = ['\u2063','']# \u2063 is invisible separator
    emoji_list = re.findall(r'[^\w\s,.\-/?_}{();"\'\[\]`~!@#$%^&+=><|:*]', message)
    emoji_list = [emo for emo in emoji_list if emo not in exclude_emoji]
    return emoji_list

def unique(item_list):
    """
    get unique value (emoji) in list
    """
    unique_list= []
    for i in item_list:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list

def split(message, emojis):
    """
    split message and emoji and new line as list item
    """

    default_sep = "||"
    if emojis:
        unique_emojis = unique(emojis)
        for emo in unique_emojis:
            message  = message.replace(emo,default_sep+emo+default_sep)

    message  = message.replace("\n",default_sep+"\n"+default_sep)
    message = message.replace("\t","    ") # replace tab to 4 spaces
    message = message.replace('\u2063','') # replace invisible separator with empty string
    message_list = message.split(default_sep)
    return message_list


"""
break down method send_message
- open login in browser : login()
- open new url in browser : open_browser(phone)
- typing message : send_message(phone,message)
- send attachments : send_attachment(phone,file)
- tokenize chat :  tokenize_chat(phone,chat)
- update report : update_report(phone)
"""

def send_message(mobile, message, attachments=[], is_caption_text = False, row=None):
    global browser
    """ Still can send an attachment in a message, next: multiple attachments
        # attachment_status = (attachments, sent_status)
        # status option : 
            # Failed
            # Sent
            # No Attachment
            # Partially Sent
    """
    url_send = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(mobile)

    message_status = "Sent"
    attachment_status = "No Attachment"
    sent_date = None
    token = None
    name = None
    replied = False
    responses = "info;message\n"
    result = {
                'mobile': mobile,
                'status':message_status, 
                'attachment_status': attachment_status,
                'saved_name': name,
                'token': token,
                'sent_date': sent_date,
                'replied': replied,
                'responses': responses,
                'row': row,
                }
    browser.get(url_send)
    print("Open browser")

    browser.implicitly_wait(5)
    notif_invalid  = get_notif_invalid()

    if notif_invalid:
        # check invalid didepan
        message_status = "Invalid" 
        print("Number is Invalid")
    elif notif_invalid == "":
        try:
            input_box = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, WAXPATH["element"]["message_box"])))
        except Exception as e:
            input_box = None
            message_status = "Failed" 
            print("No message text box defines as Failed",e)
    
    if message_status != "Invalid" and input_box != None:
        input_box = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH, WAXPATH["element"]["message_box"]))) 
        # is_caption_text = False
        if len(attachments) >=1 and is_image_or_video(attachments[0]):
            is_caption_text =True
        else:
            is_caption_text = False

        try:

            emoji_list = extract_emoji(message)
            message_list = split(message, emoji_list)
            if message_list[-1] != "\n":
                message_list.append("\n")
            else:
                last_line = False
                while not last_line:
                    if message_list[-2] == "\n":
                        message_list.pop(-2)
                    else:
                        last_line= True

            print("message_list", message_list)
            for ch in message_list:
                start_time = datetime.datetime.now()
                if ch == "\n":
                    ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                        Keys.SHIFT).perform()
                else:
                    if ch in UNICODE_EMOJI['en'].keys():
                        
                        emoji_str = UNICODE_EMOJI['en'][ch][:-1 ].replace("_"," ")
                        
                        # if multi multi type of emo like folded hands with different color
                        # TODO : buat untuk yang lain juga
                        
                        # if not emoji_str.endswith(" "):
                        #     input_box.send_keys(emoji_str+" ")
                        # else:
                        input_box.send_keys("  ")
                        input_box.send_keys(Keys.BACKSPACE)
                        input_box.send_keys(emoji_str)

                        if emoji_str in [":folded hands"]:
                            ActionChains(browser).key_down(Keys.ENTER).key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).key_up(
                        Keys.ENTER).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
                        else:
                            input_box.send_keys(Keys.ENTER)
                        # input_box.send_keys(emoji_str)
                        # input_box.send_keys(Keys)
                        
                    else:
                        input_box.send_keys(ch)
                end_time = datetime.datetime.now()
                delta_in_second =end_time - start_time
            if not is_caption_text:
                try:
                    send_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["send_button"]))) 
                    send_button.click()
                except:
                    print("exception send button")
                print("Message sent successfully")
                print("wait get token")
                browser.implicitly_wait(30)

                result['token'] = get_token_message()
                print("token", result["token"])
                message_status = "Sent"

        except Exception as e:
            print("Failed to send message exception: ", e)
            if message_status != "Invalid":
                message_status = "Failed"

        try:
            # Bug : load file 
            for idx_attach,attachment in enumerate(attachments):
                is_docs = not is_image_or_video(attachment)
                status_attach = send_attachment(attachment, is_docs)
                if  status_attach== "Failed":
                    if attachment_status in ["Sent","Partially Sent"]:
                        attachment_status = "Partially Sent"
                    else:
                        attachment_status = "Failed"
                else:
                    if "Failed" in attachment_status:
                        attachment_status = "Partially Sent"
                    else:
                        attachment_status = "Sent"
                if is_caption_text and idx_attach == 0 :
                    if attachment_status == "Sent" and message_status not in ["Invalid","Failed"]:
                        print("Message sent successfully")
                        print("wait get token")
                        browser.implicitly_wait(30)
                        result['token'] = get_token_message()
                        print("token", result["token"])
                        message_status = "Sent"
        except Exception as e:
            print("Failed to send message exception: ", e)
            if not message_status == "Invalid":
                message_status = "Failed"
            attachment_status = "Failed"

        if attachment_status == "Failed":
            try:
                send_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["send_button"]))) 
                send_button.click()
            except:
                print("exception send button")
                
            # message_status = "Failed"

        result['saved_name'] = get_saved_name(mobile)
        
        result['status'] = message_status
        result['attachment_status'] = attachment_status 
        result['sent_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Send message result", result)
    else:
        result['status'] = message_status
        result['attachment_status'] = "Failed"
        result['sent_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return result

def collect_response(mobile, token, result={}):
    """
    sleep perlu diubah ke QThread.sleep agar tidak membuat GUI ngehang
    result input is send or previous result
    """
    global browser

    sent_date = None
    name = None
    replied = False
    attachment_status = "No Attachment"
    message_status = "Failed"
    responses = "info;message\n"

    if not result:
        result = {
                    'mobile': mobile,
                    'status':message_status, 
                    'attachment_status': attachment_status,
                    'saved_name': name,
                    'token': token,
                    'sent_date': sent_date,
                    'replied': replied,
                    'responses': responses
                    }

    try:
        mobile_number = str(mobile)

        url_send = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(mobile_number)
        browser.get(url_send)

        response = get_response_by_token(token)
        from_token_massages = copy.copy(response["message"])
        from_token_massages.reverse() # index 0 is token
        from_token_infos = copy.copy(response["info"])
        from_token_infos.reverse() # index 0 is token
        # write log
        result['status'] = response["status"][-1]
        sender_contact = None
        next_chat_is_reply = False
        for info,response_msg in zip(from_token_infos,from_token_massages) :
            if sender_contact is None:
                sender_contact = mobile_number 
            if not next_chat_is_reply and sender_contact not in response["data_id"]:
                next_chat_is_reply = True

            if next_chat_is_reply:
                chat = ";".join(info, response_msg)+"\n"
                result['responses'] = result["responses"] + chat
                if not replied:
                    replied = True
            result["replied"] = replied
            
    except Exception as e:
        print("Failed to collect exception: ", e)

    return result

def get_notif_invalid():
    """ number has active WA number or not"""
    global browser

    notif_text = ''
    try:
        xpath = WAXPATH["element"]["popup"]
        text = ["Starting chat"]
        element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        notif_text = element.text

        while notif_text in text:
            element = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
            notif_text = element.text
    except Exception as e:
        print("No notification Invalid Url: ", e)
        notif_text = ''

    return notif_text

def is_image_or_video(media_filename):
    media_path =  ATTACHMENT_PATH.joinpath(media_filename).resolve()
    file_type = filetype.guess(str(media_path))
    if file_type.mime.split("/")[0] in ['image', 'video']:
        return True
    return False

def get_attachment_type(media_filename):
    media_path =  str(ATTACHMENT_PATH.joinpath(media_filename).resolve())
    file_type = filetype.guess(media_path)
    return file_type.mime

def send_attachment(media_filename, is_docs=False):
    """
        By default or images or videos
        If is_docs is True can send files (pdf, docx, csv etc.)
    """

    # Attachment Drop Down Menu
    try:
        clip_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["clip_button"])))
        clip_button.click()
    except Exception as e:
        print("Clip button Error", e)    
    
    try:    
        if is_docs:
            # To send docs files.
            media_type_button = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, WAXPATH["element"]["file_button"]))) 
        else:
            # To send videos and images.
            media_type_button = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, WAXPATH["element"]["image_button"]))) 
    except Exception as e:
        media_type_button = None
        print("Send attachments error", e)    

    media_path =  str(ATTACHMENT_PATH.joinpath(media_filename).resolve())

    try:
        file_attach = pathlib.Path(media_path)
        if file_attach.exists():
            media_type_button.send_keys(media_path)
    except Exception as e:
        print("error open file attachments", e)

    # Send button
    send_button = None
    browser.implicitly_wait(5)
    
    if is_docs:
        try:
            # send_button = browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')
            send_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["send_attach_button"]))) 
        except Exception as e:
            print("Error expath button, force to enter")
    else:
        try:
            # button send with preview and tools (crop, paint etc)
            # send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div[2]/span/div/span/div/div/div/div/div[2]/div[2]/div/div')
            send_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["send_attach_button"])))

        except:
            print("send_button with tools exception ")
            try:
                # send_button = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div')
                send_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, WAXPATH["element"]["send_attach_button"]))) 
            except:
                print("send_button without tools exception ")
            
    try:
        send_button.click()
        print("media OK")
    except Exception as e:
        print("media NOT OK, Force CLOSED by ESC")
        return "Failed"
    return "Sent"

def login():
    #  Headless Mode: False
    whatsapp_login(CHROMEDRIVER_PATH, False)