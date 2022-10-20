# -*-coding:utf-8 -*

import os
from os import path
import sys
import random
from datetime import datetime
from time import sleep

import utils.mylog as mylog
import utils.jsonprms as jsonprms
import utils.file_utils as file_utils
import utils.str_utils as str_utils
from utils.humanize import Humanize
from utils.mydecorators import _error_decorator, _trace_decorator

from engines.poleemploiengine import Poleemploiengine
from engines.linkedinengine import Linkedinengine
from engines.neuvooengine import Neuvooengine
from engines.monsterengine import Monsterengine
from engines.apecengine import Apecengine
from engines.glassdoorengine import Glassdoorengine

import inspect
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
from structs.cookieclicked import Cookieclicked

class Bot:
      
        def __init__(self):                                
                
                self.cookieclicked = Cookieclicked()

        def trace(self, stck):
                #print (f"{stck.function} ({ stck.filename}-{stck.lineno})")                                
                self.log.lg(f"{stck.function} ({ stck.filename}-{stck.lineno})")

        # init
        @_trace_decorator
        @_error_decorator()
        def init(self):            
                self.trace(inspect.stack()[0])
                
                options = webdriver.ChromeOptions()
                if (self.jsprms.prms['headless']):
                        options.add_argument("--headless")
                else:
                        options.add_argument("user-data-dir=./chromeprofile")
                # anti bot detection
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                # pi / docker
                if (self.jsprms.prms['box']):
                        options.add_argument("--no-sandbox")
                        options.add_argument("--disable-dev-shm-usage")
                        options.add_argument("--disable-gpu")
                        prefs = {"profile.managed_default_content_settings.images": 2}
                        options.add_experimental_option("prefs", prefs)
                options.add_argument(f"user-agent={self.jsprms.prms['user_agent']}")
                options.add_argument("--start-maximized")
                driver = webdriver.Chrome(executable_path=self.chromedriver_bin_path, options=options)                       
                
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                # resout le unreachable
                driver.set_window_size(1900, 1080)
                driver.implicitly_wait(self.jsprms.prms['implicitly_wait'])
                return driver
                

        def stop(self):  
                stopfile =f"{self.root_app}{os.path.sep}stop"
                res = path.exists(stopfile)
                if (res):                                                
                        self.log.lg("=STOP CRAWLING=")
                return res  

        def removestop(self):  
                stopfile =f"{self.root_app}{os.path.sep}stop"
                res = path.exists(stopfile)
                if (res):os.remove(stopfile)

        @_trace_decorator
        @_error_decorator()
        def getlocationfromplace (self,sitename, place):        
                                          
                for location in place["location"]:
                        #print(location["site"])
                        if location["site"]==sitename:
                                #print(f"###{location}###")
                                return location
        
        @_trace_decorator
        @_error_decorator()
        def doreport(self, reportname):  
                places = self.jsprms.prms["places"]
                keywords = self.jsprms.prms["keywords"]
                sites = self.jsprms.prms["sites"]
                                
                for place in places:                                
                        #print(place["name"])
                        for kw in keywords:
                                #words=kw["words"]
                                #wordstostr = '+'.join(words)                                
                                for site in sites:
                                        name=site["name"]
                                        #print(site["name"])                                                
                                        if name=="poleemploi":
                                                if site["ison"]:                                                                
                                                        location =self.getlocationfromplace(name,place)                                                        
                                                        poleemploiengine = Poleemploiengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)
                                                        poleemploiengine.getreport(site, location, kw)
                                        if name=="linkedin":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)                                                        
                                                        linkedinengine = Linkedinengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)
                                                        linkedinengine.getreport(site, location, kw)
                                        if name=="neuvoo":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)                                                        
                                                        neuvooengine = Neuvooengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)                                                          
                                                        neuvooengine.getreport(site, location, kw)    
                                        if name=="monster":
                                                if site["ison"]:                                       
                                                        location =self.getlocationfromplace(name,place)                                                          
                                                        monsterengine = Monsterengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)                                                                
                                                        monsterengine.getreport(site, location, kw)
                                        if name=="apec":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)                                                        
                                                        apecengine = Apecengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)
                                                        apecengine.getreport(site, location, kw)
                                        if name=="indeed":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)
                                                        
                                        if name=="adzuna":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)
                                                        
                                        if name=="glassdoor":
                                                if site["ison"]:
                                                        location =self.getlocationfromplace(name,place)                                                        
                                                        glassdoorengine = Glassdoorengine(self.trace, self.log, self.jsprms, self.driver, self.humanize, self.cookieclicked)               
                                                        glassdoorengine.getreport(site, location, kw)

        def init_main(self, command, jsonfile):
                try:
                        self.root_app = os.getcwd()
                        self.log = mylog.Log()
                        self.log.init(jsonfile)
                        self.trace(inspect.stack()[0])
                        jsonFn = f"{self.root_app}{os.path.sep}data{os.path.sep}conf{os.path.sep}{jsonfile}.json"
                        self.jsprms = jsonprms.Prms(jsonFn)
                        self.chromedriver_bin_path = self.jsprms.prms['chromedriver']
                        # self.test = self.jsprms.prms['test']                       
                        self.global_error = False
                        self.log.lg("=HERE WE GO=")
                        keep_log_time = self.jsprms.prms['keep_log_time']
                        keep_log_unit = self.jsprms.prms['keep_log_unit']
                        self.log.lg(f"=>clean logs older than {keep_log_time} {keep_log_unit}")                        
                        file_utils.remove_old_files(f"{self.root_app}{os.path.sep}log", keep_log_time, keep_log_unit)
                        self.humanize = Humanize(self.trace, self.log, self.jsprms.prms['offset_wait'], self.jsprms.prms['wait'], self.jsprms.prms['default_wait'])
                        # file_utils.remove_old_files(f"{self.root_app}{os.path.sep}data/reports", keep_log_time, keep_log_unit)
                except Exception as e:
                        self.log.errlg(f"Wasted, very wasted : {e}")
                        raise

        def main(self):                         
                try:
                        # InitBot
                        # args
                        
                        nbargs = len(sys.argv)
                        command = "doreport" if (nbargs == 1) else sys.argv[1]
                        #command = "test" if (nbargs == 1) else sys.argv[1]
                        # json parameters from file
                        jsonfile = "default" if (nbargs < 3) else sys.argv[2].lower()          
                        param = "default" if (nbargs < 4) else sys.argv[3].lower()                
                        print(f"command={command}") 
                        self.init_main(command, jsonfile) 
                        self.removestop() #remove stop file
                        #logs
                       
                        # for tests command = "doreport"
                        self.trace(inspect.stack()[0])     
                                                
                        self.driver = self.init()                        
                        print(command)                                                       
                        if (command=="doreport"):                             
                                
                                self.doreport(param)
                                #self.waithuman(1500)
                                #input("enter key")
                                self.driver.close()
                                self.driver.quit()
                        if (command=="test"):   
                                print(inspect.stack()[0])

                        self.log.lg("=THE END COMPLETE=")
                except KeyboardInterrupt:
                        print("==>> Interrupted <<==")
                        pass
                except Exception as e:

                        print("==>> GLOBAL MAIN EXCEPTION <<==")
                        # self.log.errlg(e)
                        self.driver.close()
                        self.driver.quit() 
                        return False
                        # raise                        
                finally:
                        print("==>> DONE <<==")
       
        def testo(self):         
                self.trace(inspect.stack()[0])
                
                try:     
                        
                        pass

                except Exception as e:
                        self.log.errlg(e)  
                        self.driver.close()
                        self.driver.quit()        


              
               
    

        
                

        

