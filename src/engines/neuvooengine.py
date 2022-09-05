# -*-coding:utf-8 -*
from utils.mydecorators import _error_decorator, _trace_decorator
from selenutils.selenutils import Selenutils


class Neuvooengine:
      
        def __init__(self, trace, log, jsprms, driver, humanize, cookieclicked):                                                
                self.trace = trace
                self.log = log
                self.jsprms = jsprms                
                self.driver = driver
                self.humanize = humanize    
                self.cookieclicked = cookieclicked                

        @_trace_decorator
        @_error_decorator(False)
        def dosearch(self, site, location, words):
                        prms=f"k={words}&l={location['geosite']}&p=1&date=7d&field=&company=&source_type=&radius={location['distance']}&from=&test=&iam=&is_category=no"
                        fullurl = f"{site['url']}/?{prms}"
                        self.driver.get(fullurl)                        
                
        @_trace_decorator
        @_error_decorator()
        def clickcookie(self):                
                self.cookieclicked.neuvoo = True

        @_trace_decorator
        @_error_decorator()
        def getreport(self, site, location, words):
                self.dosearch(site, location, words)      
                # self.clickcookie() Implementer si besoin
                input("Waiting for key:\n")                                     
                                
        
              
               
    

        
                

        

