import ipinfo, argparse, sys, requests
from opencage.geocoder import OpenCageGeocode
from colorama import Fore, init
init()


def cl_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument("-ip", dest="IP_Address", help="Program to Track devices, Use --help to see usage.")
   arguments = parser.parse_args()
   if not arguments.IP_Address:
       print("Please specify an IP address. Defaulting to User's IP Address. Use --help to see usage.\n")
   return arguments


def get_ip_location(ip_address):
   try:
       token = "Your IPinfo Token here."
       ip_handler = ipinfo.getHandler(token)
       ip_details = ip_handler.getDetails(ip_address)
       for each_key, each_value in ip_details.all.items():
           print(f"{Fore.GREEN}{each_key}: {each_value}")
       global latitude, longitude
       try:
           latitude = ip_details.latitude
           longitude = ip_details.longitude
       except AttributeError:
           print("[-] Coordinates for this IP not found. Might be a spoofed IP.")
   except requests.exceptions.HTTPError and requests.exceptions.ConnectionError:
       print("[-] Please ensure you have a stable internet connection and valid API keys.")


args = cl_arguments()
get_ip_location(args.IP_Address)


OCG = OpenCageGeocode('Your Opencage API key here')
try:
   results = OCG.reverse_geocode(latitude, longitude)
except NameError:
   sys.exit()
else:
   print(f'\n{Fore.RED}The approximate Location is: ', results[0]['formatted'])


