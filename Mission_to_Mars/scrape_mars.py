from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
