# -*-coding:utf-8 -*
from utils.mydecorators import _error_decorator, _trace_decorator
from selenutils.selenutils import Selenutils


class Apecengine:
      
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
                prms=f"lieux={location['code']}&distance={location['distance']}&motsCles={words}&anciennetePublication=101851&sortsType=DATE"
                fullurl = f"{site['url']}?{prms}"
                self.driver.get(fullurl)
        
        @_trace_decorator
        @_error_decorator(False)
        def clickcookie(self):
                if not self.cookieclicked.apec:
                        cookbutel = self.driver.find_element_by_id("onetrust-accept-btn-handler")
                        selenutils = Selenutils(self.trace, self.driver, self.humanize)
                        selenutils.doclick(cookbutel)
                self.cookieclicked.apec = True
      
        @_trace_decorator
        @_error_decorator()
        def getreport(self, site, location, words):
                self.dosearch(site, location, words)                          
                self.clickcookie()
                input("Waiting for key:\n")


              
               
    

        
                

        

