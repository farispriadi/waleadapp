from config import ABOUT
import re
import sys
new_iss = ""
for line in open('innosetup.iss','r').readlines():
    line = re.sub(r'#define MyAppName .+',r'#define MyAppName "{}"'.format(ABOUT["app_name"]), line)
    line = re.sub(r'#define MyAppVersion .+',r'#define MyAppVersion "{}"'.format(ABOUT["version"]), line)
    line = re.sub(r'#define MyAppPublisher .+',r'#define MyAppPublisher "{}"'.format(ABOUT["publisher"]), line)
    new_iss = new_iss+line
print(new_iss)

with open('innosetup_waleadapp.iss','w') as out:
	out.write(new_iss)
