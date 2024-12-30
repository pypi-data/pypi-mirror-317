from time import sleep

from appium import webdriver
from appium.webdriver import WebElement
from mag_tools.exception.app_exception import AppException
from mag_tools.model.data_type import DataType
from mag_tools.utils.common.string_utils import StringUtils
from mag_tools.utils.file.json_file_utils import JsonFileUtils
from selenium.webdriver import ActionChains

from bean.element_info import ElementInfo
from mag_test.core.app_driver import AppDriver
from model.action_type import ActionType
from model.control_type import ControlType
from utils.table_utils import TableUtils


class EventUtils:
    @staticmethod
    def process_event(driver:AppDriver, element:WebElement, element_info:ElementInfo, attachment: str=None):
        if element is None:
            raise AppException(f'未找到指定的控件 {element_info}')

        return_type = ControlType.get_by_element(element)
        if return_type in {ControlType.BUTTON, ControlType.SPLIT_BUTTON, ControlType.MENU_ITEM}:  # 单击控件
            element.click()
        elif return_type in {ControlType.EDIT, ControlType.DOC, ControlType.COMBO_BOX}:  # 可编辑控件
            element.click()
            if element_info.action == ActionType.SEND_KEYS:
                element.send_keys(element_info.value)
            elif element_info.action == ActionType.CLEAR:
                element.clear()
            else:
                element.clear()
                element.send_keys(element_info.value)
        elif return_type in {ControlType.LABEL}:
            element.click()
        elif return_type in {ControlType.TREE_ITEM}:
            offset = element_info.get_offset(element.size['width'], element.size['height']) if element_info.value else None
            EventUtils.click_offset(driver, element, offset)
        elif return_type in {ControlType.TAB_ITEM, ControlType.LIST_ITEM}:
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()
        elif return_type == ControlType.TABLE:
            if element_info.value:
                value_array = JsonFileUtils.load_json(attachment)
                TableUtils.set_table(element, value_array, element_info.init_status)
        elif return_type in {ControlType.CHECKBOX, ControlType.RADIO}:  # 复选按钮选择
            value = StringUtils.to_value(element_info.value, DataType.BOOLEAN)

            if (value and not element.is_selected()) or (not value and element.is_selected()):
                element.click()
        elif return_type == ControlType.PANE:
            if element_info.control_type == ControlType.DATETIME:
                element.send_keys(element_info.value)
            else:
                element.clear()
        elif return_type == ControlType.WINDOW:
            EventUtils.__click_window(driver, element_info.value)
        else:
            raise f"Unsupported type or action: {element_info.control_type} : {return_type}"

        element.clear()
        element.send_keys(element_info.value)

    @staticmethod
    def click_offset(driver: webdriver.Remote, element: WebElement, offset: tuple[int, int] = None):
        if offset:
            offset_x, offset_y = offset
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(element, offset_x, offset_y).click().perform()
            sleep(1)
        else:
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform()

    @staticmethod
    def __click_window(driver: AppDriver, value: str):
        if value == 'close':
            driver.close()
            driver.quit_app()
        elif value == 'max':
            driver.maximize_window()
        elif value == 'min':
            driver.minimize_window()