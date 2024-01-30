import socket
from ip2geotools.databases.noncommercial import DbIpCity

url = input("Insert a URL:\n")

ip = socket.gethostbyname(url)
response = DbIpCity.get(ip, api_key="free")

print(response)