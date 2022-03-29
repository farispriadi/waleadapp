import yaml,os

XPATH_FILE = os.path.join(os.path.abspath(os.getcwd()),"updater","manifest.yaml")
if os.path.isfile(XPATH_FILE):
    with open(str(XPATH_FILE), 'r') as f:
        WAXPATH = yaml.load(f)
else:
    WAXPATH = {
        "name" : "Web WhatsApp",
        "released": "2021.11.25",
        "version": "2.21.21.19",
        "element":{
            "message_box": '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]',
            "send_button": '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button',
            "popup": '//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div[1]',
            "clip_button": '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div',
            "image_button":'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input',
            "file_button": '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[3]/button/input',
            "send_attach_button": '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div',
            "image_send_button": '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div',
            "image_preview_send_button": '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div',
            "file_send_button": '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div',
            "chats_container_by_class": '//*[@id="main"]/div[3]/div/div[2]/div[@class="y8WcF"]',
            "chats_container_by_index": '//*[@id="main"]/div[3]/div/div[2]/div[3]',
            "chat_boxes": '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[@data-id]',
            "first_chat_presented": '//*[@id="main"]/div[3]/div/div[2]/div[3]/div[2]',
            "scroll_area": '//*[@id="main"]/div[3]/div/div[@class="_33LGR"]',
            "chat_box":{
                "info":   './div/div[1]/div/div[1]',
                "status": './div/div[1]/div/div[2]/div/div/span',
                "message":'./div/div[1]/div/div[1]/div/span[1]/span',
                
            },
            "chat_box_image":{
                "info":   './div/div[1]/div',
                "status": './div/div[1]/div/div/div[3]/div/div/span',
                "message":'./div/div[1]/div/div/div[2]/div/span[1]/span',
                "image": './div/div[1]/div/div/div[1]/div/div[1]/img'
            }
        }
    }