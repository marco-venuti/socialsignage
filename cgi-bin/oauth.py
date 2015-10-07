#!/usr/bin/env python3

import cgi
import sys
import requests
import configparser

import cgitb
cgitb.enable()

config_error = False
try:
    config = configparser.ConfigParser()
    config.read('../oauth.ini')
    app_id = config['facebook']['app_id']
    redirect_uri = config['facebook']['redirect_uri']
    app_secret = config['facebook']['app_secret']
except:
    config_error = True
else:
    arguments = cgi.FieldStorage()
    
    if 'code' in arguments.keys():
        code = arguments['code'].value
    else:
        print ("Location: https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}".format(app_id=app_id,redirect_uri=redirect_uri))
    
    r_params = {'client_id':app_id,
                'redirect_uri': redirect_uri,
                'client_secret': app_secret,
                'code': code}
    r = requests.get('https://graph.facebook.com/oauth/access_token',params=r_params)
    
    access_token = None
    for i in r.text.split('&'):
        j = i.split('=')
        if j[0] == "access_token":
            access_token = j[1]
            break

    if access_token is not None:
        access_token_file = open("../access_token.txt",'w')
        access_token_file.write(access_token)
        access_token_file.close()
        genconfig = configparser.ConfigParser()
        genconfig['facebook'] = {'access_token': access_token}
        with open('../genconfig.ini','w') as genconfigfile:
            genconfig.write(genconfigfile)

print ("Content-Type: text/html")
print ('\n')
print ("""\
<html>
<body>
<h1>Social signage OAUTH interface</h1>
(by Enrico Polesel)<br><br>
""")
if config_error:
    print ("Error reading configuration file")
else:
    if access_token is not None:
        print ("access_token: {access_token}<br>\n".format(access_token=access_token))
    else:
        print ("No access token found!<br>\n")
        print ("This may be useful:<br>\n")
        print (r.text)
print("""
</body>
</html>
""")

