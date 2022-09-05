import inspect

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Selenutils(metaclass=Singleton):
    
        def __init__(self, trace, driver, humanize):
                self.trace = trace
                self.driver = driver                
                self.humanize = humanize

        
        def doclickex(self,el):
                self.trace(inspect.stack()[0])          
                cpt=0
                while cpt<10:
                        try:         
                                el.click()
                                break
                        except Exception as e:                                
                                print(f"Ah ben nan y click pô: {e}")
                                cpt+=1
                                if cpt ==10:raise
                                self.waithuman(2)
                                
        def doclickwithjs(self,el):
                self.trace(inspect.stack()[0])          
                try:         
                        self.driver.execute_script("arguments[0].click();", el)
                except Exception as e:                                
                        print(f"ClickwithJS Ah ben nan y click pô: {e}")
                        
                        
        def doclick(self,el):
                self.trace(inspect.stack()[0])          
                try:         
                        el.click()
                except Exception as e:                                
                        print(f"Ah ben nan y click pô: {e}")
                        self.doclickwithjs(el)
                        self.waithuman(2)