from time import sleep

from appium import webdriver
from appium.webdriver import WebElement
from selenium.webdriver import ActionChains

from mag_test.core.app_driver import AppDriver


class EventUtils:
    @staticmethod
    def click(driver:webdriver.Remote, element:WebElement, offset:tuple[int,int]=None):
        if offset:
            offset_x, offset_y = offset
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(element, offset_x, offset_y).click().perform()
            sleep(1)
        else:
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()

    @staticmethod
    def click_checkbox(element:WebElement, value:bool):
        if value and not element.is_selected():
            element.click()
        elif not value and element.is_selected():
            element.click()

    @staticmethod
    def click_window(driver:AppDriver, value:str):
        if value == 'close':
            driver.close()
            driver.quit_app()
        elif value == 'max':
            driver.maximize_window()
        elif value == 'min':
            driver.minimize_window()