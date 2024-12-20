import json
import requests
import webbrowser, os
import time
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute
from gmplot import gmplot   
import sys 

# Global variables
lats = []
longs = []
j = 0

# Plots the coordinates found from the ip addresses in main
def plot_lat_long():
    newlats = []
    newlongs = []

    # Removing any duplicates from the latitude and longitude lists
    for lat in lats:
        if lat not in newlats:
            newlats.append(lat)

    for long in longs:
        if long not in newlongs:
            newlongs.append(long)

    # # For debugging
    # print(newlats)
    # print(newlongs)
   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)
    gmap = gmplot.GoogleMapPlotter(newlats[0], newlongs[0], 3, apikey = "APIKEY")
    
    #Handle path issue for windows, so that marker images can optionally be found using gmplot
    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
        
    # Places markers on each coordinate pair
    # Specific labels for each number of arguments
    if (len(newlats) == 2):
        gmap.scatter( newlats, newlongs, '#FF00FF', 
                              size = 40000,
                              marker = True,
                              label=['1', '2']) 
    if (len(newlats) == 3):
        gmap.scatter( newlats, newlongs, '#FF00FF', 
                              size = 40000,
                              marker = True,
                              label=['1', '2', '3']) 
    elif (len(newlats) == 4):
        gmap.scatter( newlats, newlongs, '#FF00FF', 
                              size = 40000,
                              marker = True,
                              label=['1', '2', '3', '4']) 
    elif (len(newlats) == 5):
        gmap.scatter( newlats, newlongs, '#FF00FF', 
                              size = 40000,
                              marker = True,
                              label=['1', '2', '3', '4', '5']) 
    elif (len(newlats) == 6):
        gmap.scatter( newlats, newlongs, '#FF00FF',
                              size = 40000,
                              marker = True,
                              label=['1', '2', '3', '4', '5', '6']) 
    elif (len(newlats) == 7):
        gmap.scatter( newlats, newlongs, '#FF00FF',
                            size = 40000,
                            marker = True,
                            label=['1', '2', '3', '4', '5', '6', '7']) 
    elif (len(newlats) == 8):
        gmap.scatter( newlats, newlongs, '#FF00FF',
                            size = 40000,
                            marker = True,
                            label=['1', '2', '3', '4', '5', '6', '7', '8']) 
    elif (len(newlats) == 9):
        gmap.scatter( newlats, newlongs, '#FF00FF',
                            size = 40000,
                            marker = True,
                            label=['1', '2', '3', '4', '5', '6', '7', '8', '9']) 
    elif (len(newlats) == 10):
        gmap.scatter( newlats, newlongs, '#FF00FF',
                            size = 40000,
                            marker = True,
                            label=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']) 
    
    # Plot lines between each of the coordinate pairs
    gmap.plot(newlats, newlongs)

    cwd = os.getcwd()
    
    # saving the map as an HTML into the project directory
    gmap.draw('traceroute.html')
    
    # opening the HTML via default browser
    webbrowser.open(cwd +"/traceroute.html")
#"file:///" +

# find the latitude and longitude 
def find_and_plot_coordinates():
    j = 0
    while(j < len(ips)):
        # tool for finding latitutde and longitude of ip address
        url = "http://dazzlepod.com/ip/{}.json".format(ips[j])
        
        # debugging the URLs
        print(url)
        response = requests.get(url)
        data = response.json()

        
        # making sure the wesbsite gave us lat and long
        if 'latitude' in data and 'longitude' in data:
            lats.append(data['latitude'])
            longs.append(data['longitude'])
            print("The coordinates for this IP Address are: ")
            print(data['latitude'],data['longitude'])
                            
        # pausing for 2 seconds to make sure we don't get banned by dazzlepod.com
        time.sleep(SLEEP_SECONDS)
        j += 1

    #calls function to plot the lats and longs
    plot_lat_long()

SLEEP_SECONDS = 1

# hostname to traceroute to and convert to IP address
hostname = input("Please enter your desired URL: ")
ip = socket.gethostbyname(hostname)

#'res' -- results from traceroute 
res, _ = traceroute(ip,maxttl=255,verbose = 0)

# will store retrieved IPs here.
ips = []

# going through the traceroute results and extracting IP addresses into the array
for item in res.get_trace()[ip]:
    ips.append(res.get_trace()[ip][item][0])
print("These are the IP Addresses within this path: ")
print(ips)
    
find_and_plot_coordinates()


