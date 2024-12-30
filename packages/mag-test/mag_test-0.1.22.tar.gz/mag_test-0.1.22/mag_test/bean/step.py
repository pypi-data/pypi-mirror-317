from sys import exception
from typing import Optional

import pytest
from mag_tools.exception.app_exception import AppException
from mag_tools.log.logger import Logger
from mag_tools.model.convert_type import ConvertType
from mag_tools.model.data_type import DataType
from mag_tools.model.common.message_type import MessageType
from mag_tools.utils.common.string_format import StringFormat
from mag_tools.utils.file.file_utils import FileUtils
from mag_tools.utils.test.table_utils import TableUtils
from mag_tools.utils.file.json_file_utils import JsonFileUtils
from mag_tools.utils.common.string_utils import StringUtils

from selenium.webdriver.remote.webelement import WebElement

from mag_test.model.control_type import ControlType
from mag_test.model.test_component_type import TestComponentType
from mag_test.bean.base_test import BaseTest
from mag_test.bean.element_info import ElementInfo
from mag_test.core.app_driver import AppDriver
from mag_test.finder.element_finder import ElementFinder
from mag_test.utils.event_utils import EventUtils
from mag_test.model.usage_status import UsageStatus


class Step(BaseTest):
    def __init__(self, home_dir:str, name: Optional[str], control_name:Optional[str], control_type:Optional[ControlType],
                 automation_id:Optional[str], value:Optional[str], function_index:Optional[int]=None, step_index:Optional[int]=None,
                 parent_name:Optional[str]=None, parent_type:Optional[ControlType]=None, parent_id:Optional[str]=None,
                 pop_window:Optional[str]=None, status:UsageStatus=UsageStatus.NORMAL):
        super().__init__(home_dir, name, step_index, TestComponentType.STEP, None, status)

        self.__function_index = function_index
        self.__element_info = ElementInfo(control_name, control_type, automation_id, None,
                                          parent_name, parent_type, parent_id, None, StringFormat.format(value), pop_window)

    @pytest.mark.benchmark
    def start(self, driver:AppDriver):
        """
        启动测试步骤
        :param driver: AppDriver
        """
        if self._status != UsageStatus.NORMAL:
            return driver

        try:
            Logger.debug(f'测试步骤[{self._name}]-{self._index}：\n\t{self.__element_info}')

            if self.__element_info.is_virtual_control():
                self.__process_virtual_event()
            else:
                # 查找控件并处理事件
                element = ElementFinder.find(driver, self.__element_info)
                self.__process_event(driver, element)

                # 检查消息提示框
                alert_result = driver.check_alert()
                if alert_result[0] in {MessageType.ERROR}:
                    raise AppException(alert_result[1])

                # 如果指定了弹出窗口，则切换
                if self.__element_info.pop_window:
                    driver = ElementFinder.switch_to_window_by_title(driver, self.__element_info.pop_window)

            self.success()
        except (AppException, Exception) as e:
            Logger.error(f"测试步骤[{self._name}-{self._index}]失败: {self.__element_info.name}({self.__element_info.control_type})\n{str(e)}")
            self.fail(str(e))

        super()._report()
        return driver

    def __process_event(self, driver:AppDriver, element:WebElement):
        """
        启动测试步骤
        :param driver: AppDriver
        """
        if element is None:
            raise exception(f'未找到指定的控件 {self.__element_info}')

        return_type = ControlType.get_by_element(element)
        Logger.debug(f'找到的控件返回类型为：{self.__element_info.control_type} ({return_type})')

        if return_type in {ControlType.BUTTON, ControlType.SPLIT_BUTTON, ControlType.MENU_ITEM,
                            ControlType.TOOL, ControlType.RADIO}:  # 单击控件
            element.click()
        elif return_type in {ControlType.EDIT, ControlType.DOC, ControlType.COMBO_BOX}:  # 可编辑控件
            element.click()
            element.clear()
            element.send_keys(self.__element_info.value)
            # actions = ActionChains(driver)
            # actions.move_to_element(element).click().perform()
            # element.clear()
            # element.send_keys(self.__element_info.value)
        elif return_type in {ControlType.LABEL}:  # 双击控件
            # actions = ActionChains(driver)
            # actions.move_to_element(element).double_click().perform()
            element.click()
        elif return_type in {ControlType.TREE_ITEM,
                              ControlType.TAB_ITEM,
                              ControlType.LIST_ITEM}:  # 复杂交互的点击
            offset = self.__element_info.get_offset(element.size['width'], element.size['height']) if self.__element_info.value else None
            EventUtils.click(driver, element, offset)
        elif return_type == ControlType.TABLE:
            if self.__element_info.value:
                convert_type = ConvertType.of_code(self.__element_info.child_name)
                value_array = JsonFileUtils.load_json(self.get_attachment(self.__element_info.value))

                TableUtils.set_table(element, value_array, convert_type)
        elif return_type in {ControlType.CHECKBOX}:  # 复选按钮选择
            value = StringUtils.to_value(self.__element_info.value, DataType.BOOLEAN)
            EventUtils.click_checkbox(element, value)
        elif return_type == ControlType.PANE:
            if self.__element_info.control_type == ControlType.DATETIME:
                element.send_keys(self.__element_info.value)
            else:
                element.clear()
        elif return_type == ControlType.WINDOW:
            EventUtils.click_window(driver, self.__element_info.value)
        else:
            Logger.info(f"Unsupported type or action: {self.__element_info.control_type} : {return_type}")

    def __process_virtual_event(self):
        if self.__element_info.control_type == ControlType.FILE:
            action = self.__element_info.name
            path = self.__element_info.value
            if action and action.upper() == 'CLEAR_DIR':
                FileUtils.clear_dir(path)
            elif action and action.upper() == 'DELETE_FILE':
                FileUtils.delete_file(path)