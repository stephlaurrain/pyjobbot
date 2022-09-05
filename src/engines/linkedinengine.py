# -*-coding:utf-8 -*
import math
from utils.mydecorators import _error_decorator, _trace_decorator
from selenutils.selenutils import Selenutils


class Linkedinengine:
      
        def __init__(self, trace, log, jsprms, driver, humanize, cookieclicked):                                                
                self.trace = trace
                self.log = log
                self.jsprms = jsprms                
                self.driver = driver
                self.humanize = humanize    
                self.cookieclicked = cookieclicked                          

        @_trace_decorator
        @_error_decorator()
        def dosearch(self, site, location, words):                
                #attention linkedin : 80km = distance 50, 120km=75 (osef pour le moment)
                #la distance est en miles
                dist = location["distance"]*1.6
                dist = int(math.ceil(dist / 10.0)) * 10
                prms=f"f_TPR=r604800&geoId={location['code']}&keywords={words}&location={location['geosite']}&distance={dist}&f_TP=1%2C2&redirect=false&position=1&pageNum=0"
                fullurl = f"{site['url']}?{prms}"
                self.driver.get(fullurl)                        
                # f_TP=1%2C2 = la semaine dernière
                # tri par date sortBy=DD

        @_trace_decorator
        @_error_decorator(False)
        def clickcookie(self):
                if not self.cookieclicked.linkedin:                                                          
                        cookbutel = self.driver.find_element_by_xpath('//div[@id="artdeco-global-alert-container"]/div[1]/section/div/div[2]/button[2]')
                        selenutils = Selenutils(self, self.trace, self.driver, self.humanize)
                        selenutils.doclick(cookbutel)
                self.cookieclicked.linkedin = True
                

        @_trace_decorator
        @_error_decorator()
        def getreport(self, site, location, words):
                self.dosearch(site,location, words) 
                self.clickcookie()
                input("Waiting for key:\n")                                       
                        
  
           
           


              
               
    

        
                

        

