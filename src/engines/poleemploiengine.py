# -*-coding:utf-8 -*
from utils.mydecorators import _error_decorator, _trace_decorator
from selenutils.selenutils import Selenutils
from selenium.webdriver.common.by import By

class Poleemploiengine:
      
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
                rnge="0-29"
                prms=f"lieux={location['code']}&motsCles={words}&offresPartenaires=true&range={rnge}&rayon={location['distance']}&tri=1"
                fullurl = f"{site['url']}?{prms}"
                self.driver.get(fullurl)

        @_trace_decorator
        @_error_decorator(False)
        def clickcookie(self):
                if not self.cookieclicked.polemploi:                                                          
                        cookbutel = self.driver.find_element(By.ID, "footer_tc_privacy_button_2")  
                        selenutils = Selenutils(self.trace, self.driver, self.humanize)
                        selenutils.doclick(cookbutel)
                self.cookieclicked.polemploi = True
                
        @_trace_decorator
        @_error_decorator()
        def getreport(self, site, location, words):
                self.dosearch(site, location, words)  
                self.clickcookie()
                input("Waiting for key:\n")                                           
                        
                


              
               
    

        
                

        

