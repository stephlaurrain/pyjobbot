# -*-coding:utf-8 -*
from utils.mydecorators import _error_decorator, _trace_decorator
from selenutils.selenutils import Selenutils


class Glassdoorengine:
      
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
                # 50 : pas de radius
                # 100 : radius=62, 30 : radius=19                        
                #dijon-chef-de-projet-informatique-emplois-SRCH_IL.0,5_IC3069836_KO6,33.htm?fromAge=7
                #PARIS =SRCH_IL.0,5_IC2881970_KO6,33
                words=words.replace(" ","-")                
                ln = len(f"{location['geosite']}-{words}")
                prms=f"{location['geosite']}-{words}-emplois-SRCH_IL.0,5_IC{location['code']}_KO6,{ln}.htm?fromAge=7"
                print(prms)
                #https://www.glassdoor.fr/Emploi/dijon-chef-de-projet-informatique-emplois-SRCH_IL.0,5_IC3069836_KO6,33.htm
                radius=""
                if location["distance"]!=50:
                        radius=f"&radius={location['distance']}"
                fullurl = f"{site['url']}/{prms}{radius}"
                print(fullurl)
                self.driver.get(fullurl)
                #input ("key")

        @_trace_decorator
        @_error_decorator(False)
        def clickcookie(self):
                if not self.cookieclicked.glassdoor: 
                        cookbutel = self.driver.find_element_by_id("onetrust-accept-btn-handler")
                        selenutils = Selenutils(self, self.trace, self.driver, self.humanize)
                        selenutils.doclick(cookbutel)                        
                self.cookieclicked.glassdoor = True
                                  
        @_trace_decorator
        @_error_decorator()
        def getreport(self, site, location, words):
                        self.dosearch(site, location, words)  
                        self.clickcookie()
                        input("Waiting for key:\n")           
              
               
    

        
                

        

