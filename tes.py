import urllib.request
response = urllib.request.urlopen('https://api.telegram.org/bot533495913:AAHG-ssiGLwQMCPVBSDG-WVUA8M3aUYzo-0/deleteMessage?chat_id=167315364&message_id=2920')
print(response.read())