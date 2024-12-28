from selenium.webdriver.remote.webelement import WebElement
class Element:
    
    def __init__(self, element: WebElement=None) -> None:
        self.element = element