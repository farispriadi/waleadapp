import requests
from requests.auth import HTTPBasicAuth
import json
import sys


def get_contacts(url="",api_key="", tag="", phone_col="phone"):
    headers = {'Content-Type': 'application/json',
                'Authorization' : api_key
            }

    tags = tag.split("/")
    parent=""
    tag = tags[-1]
    if len(tags) >= 2:
        parent = tags[0]

    data = '{"params": {"tag": "'+tag+'" ,"parent":"'+parent+'", "phone_col": "'+phone_col+'" } }'
    res = requests.post(url+'/contacts', data=data, headers=headers)

    json_data = res.json()
    result = json.loads(json_data["result"])

    contacts = {}
    for  key, val in result.items():
        for val_key in val.keys():
            if val_key not in contacts:
                contacts[val_key] = [val[val_key]]
            else:
                contacts[val_key].append(val[val_key])

        if 'id' not in contacts:
            contacts['id'] = [key]
        else:
            contacts['id'].append(key)

    return contacts

def get_tags(url="",api_key=""):
    headers = {'Content-Type': 'application/json',
                'Authorization' : api_key
            }

    data = '{"params": {"tag":"Prospects","parent":""} }'
    res = requests.post(url+'/tags', data=data, headers=headers)

    json_data = res.json()
    result = json.loads(json_data["result"])    


    tags = [tag["name"] if not tag["parent"] else "/".join([tag["parent"], tag["name"]]) for tag in result.values()]

    return tags
if __name__ == "__main__":

    tags = get_tags(url='http://localhost:10014/web/waleadappi', api_key='83b1c6646a75adcf994e3e09141ffc31f72cf940')
    print("TAGS ", tags)
    print("selected Tag:",tags[-3])

    contacts = get_contacts(url='http://localhost:10014/web/waleadappi', api_key='83b1c6646a75adcf994e3e09141ffc31f72cf940', tag=tags[-3],phone_col="mobile")
    print(contacts)



#     headers = {'Content-Type': 'application/json',
#                 'Authorization' : '83b1c6646a75adcf994e3e09141ffc31f72cf940'
#             }

#     if len(sys.argv) >=2:
#         data = '{"params": {"tag":""} }'
#         res = requests.post('http://localhost:10014/web/waleadappi/tags', data=data, headers=headers)
#     else:
#         data = '{"params": {"tag":"Prospects","parent":""} }'
#         res = requests.post('http://localhost:10014/web/waleadappi/contacts', data=data, headers=headers)

#     data = res.json()
#     print(data)

