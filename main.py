#!/usr/bin/python

from json import load
from urllib2 import *
import socket
from ast import literal_eval
import subprocess
import os

import gtk
import appindicator
import pynotify

class Gui():
  def __init__(self):
    self.ind = appindicator.Indicator ("example-simple-client", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon ("indicator-messages-new")
    self.ind.set_icon("distributor-logo")

        # create a menu
    self.menu = gtk.Menu()

        # create items for the menu - labels, checkboxes, radio buttons and images are supported:
        
    item = gtk.MenuItem("Regular Menu Item")
    item.show()
    self.menu.append(item)

    check = gtk.CheckMenuItem("Check Menu Item")
    check.show()
    self.menu.append(check)

    radio = gtk.RadioMenuItem(None, "Radio Menu Item")
    radio.show()
    self.menu.append(radio)

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
                    
    self.menu.show()

    self.ind.set_menu(self.menu)

  def quit(self, widget, data=None):
    gtk.main_quit()




class fetch_weather(Gui):
  def __init__(self, city_name_1):
    self.city_name = city_name_1
    self.fetch_raw()

  def fetch_raw(self):
    self.data = urlopen('http://openweathermap.org/data/2.1/find/name?q='+self.city_name+'&units=metric')
    self.cities = load(self.data)

    self.get_info()

  def get_info(self):
    if self.cities['count'] > 0:
      self.city = self.cities['list'][0]

      self.max_temp = (self.city['main']['temp_max'])
      self.temp_min = (self.city['main']['temp_min'])
      self.pressure = (self.city['main']['pressure'])
      self.temp = (self.city['main']['temp'])
      self.humidity = (self.city['main']['humidity'])
 
      self.main = str((self.city['weather'])).split(',')

      self.desc = ''
      for line in self.main:
        self.match = re.search(r"description.+u'(.+)'", line )
        if self.match:
          self.description = self.match.group(1).rstrip()
           
      self.desc1 = self.description.split(' ') 
      self.desc = "_".join(self.desc1)

    for line in self.main:
      self.match = re.search(r".+icon.+'(.+)'", line)
      if self.match:
        self.iconID = self.match.group(1)

    self.fetch_pictures()

  def fetch_pictures(self):
    '''fetching and creating icon of current weather'''

    self.full_path_ico = ''

    self.img_path = r'./ico'
    if not os.path.exists(self.img_path): os.makedirs(self.img_path)

    try:                                                            #check if this icon already exists
      with open(''+self.img_path+'/'+self.iconID+'.png'):pass
    except IOError:                                                 # if icon doesn't exist - create it
      self.img = open(''+self.img_path+'/'+self.iconID+'.png', 'w')
      self.img.write(urlopen('http://openweathermap.org/img/w/'+self.iconID+'.png').read())
      self.img.close()

    self.current_path = os.getcwd()
    self.full_path_ico = self.current_path + '/ico/'+self.iconID + '.png'

    self.notify()

  def notify(self):

    temp = subprocess.Popen(["notify-send -u critical 'Temperature in "+self.city_name+" is "+str(self.temp)+"C \n"+str(self.desc)+"'  -i "+self.full_path_ico+""], stdout=subprocess.PIPE, shell= True).communicate()[0]      

def main():
  gui = Gui()
  gtk.main()
  
if __name__ == '__main__':
  main()
  
