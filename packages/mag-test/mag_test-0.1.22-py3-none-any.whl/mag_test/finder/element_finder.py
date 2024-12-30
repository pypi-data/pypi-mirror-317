import ctypes
from time import sleep

from mag_tools.log.logger import Logger
from mag_tools.model.convert_type import ConvertType
from mag_tools.model.log_type import LogType
from mag_tools.utils.common.time_probe import TimeProbe
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, TimeoutException, \
    WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from mag_test.bean.element_info import ElementInfo
from mag_test.core.app_driver import AppDriver
from mag_test.finder.driver_finder_utils import DriverFinderUtils
from mag_test.finder.element_finder_utils import ElementFinderUtils
from mag_test.finder.window_finder import WindowFinder
from mag_test.model.control_type import ControlType
from mag_test.utils.tree_utils import TreeUtils
from mag_test.utils.event_utils import EventUtils


class ElementFinder:
    @staticmethod
    def find(driver:AppDriver, element_info:ElementInfo):
        Logger.debug(f'开始查找控件：{element_info.self_info()}')
        probe = TimeProbe.get_probe('查找控件')

        parent = ElementFinder.__find_parent(driver, element_info)

        # 按钮/拆分按钮
        if element_info.control_type in {ControlType.BUTTON, ControlType.SPLIT_BUTTON}:
            element = ElementFinder.__find_button(driver, element_info, parent)
        # 菜单
        elif element_info.control_type == ControlType.MENU:
            element = ElementFinder.__find_menu(driver, element_info, parent)
        # 组合框
        elif element_info.control_type == ControlType.COMBO_BOX:
            element = ElementFinder.__find_combox_box(driver, element_info, parent)
        # 列表框
        elif element_info.control_type == ControlType.LIST:
            element = ElementFinder.__find_list_box(driver, element_info, parent)
        # 列表视图
        elif element_info.control_type == ControlType.LIST_VIEW:
            element = ElementFinder.__find_list_view(driver, element_info, parent)
        # 树视图
        elif element_info.control_type == ControlType.TREE:
            element = ElementFinder.__find_tree_view(driver, element_info, parent)
        # 表格
        elif element_info.control_type == ControlType.TABLE:
            element = ElementFinder.__find_table(driver, element_info, parent)
        # 日期时间
        elif element_info.control_type == ControlType.DATETIME:
            element = ElementFinder.__find_datetime(driver, element_info, parent)
        # 窗口
        elif element_info.control_type == ControlType.WINDOW:
            element = ElementFinder.__find_window(driver, element_info)
        # 简单控件（包括：工具栏、Pane等）
        else:
            element = ElementFinder.__find_main_element(driver, element_info, parent)

        probe.write_log()

        return element

    @staticmethod
    def switch_to_window_by_title(driver:AppDriver, window_title:str):
        window_title = window_title.strip()

        if '.exe' in window_title.lower():
            driver = driver.new_driver(window_title)
        else:
            try:
                hwnd_list = WebDriverWait(driver, 10).until(lambda drv: WindowFinder.find_window_by_title(window_title))
                if hwnd_list:
                    hwnd = hwnd_list[0]
                    ctypes.windll.user32.SetForegroundWindow(hwnd)
                else:
                    Logger.error(LogType.FRAME, f"未找到窗口: {window_title}")
            except InvalidSelectorException as e:
                Logger.error(LogType.FRAME, f"查找窗口[{window_title}]选择器无效: {str(e)}")
            except NoSuchElementException as e:
                Logger.error(LogType.FRAME, f"查找窗口[{window_title}]出错: {str(e)}")
            except TimeoutException as e:
                Logger.error(LogType.FRAME, f"查找窗口[{window_title}]超时: {str(e)}")
            except WebDriverException as e:
                Logger.error(LogType.FRAME, f"查找窗口[{window_title}]时通讯异常: {str(e)}")
            except Exception as e:
                Logger.error(LogType.FRAME, f"未知异常：{str(e)}")

        return driver

    @staticmethod
    def __find_button(driver, element_info, parent=None):
        """
        查找按钮控件（包括：普通按钮和拆分按钮）
        参数：
        name 按钮名
        parent 父控件
        """
        for element_type in [ControlType.BUTTON, ControlType.SPLIT_BUTTON]:
            element_info.control_type = element_type
            element = ElementFinder.__find_main_element(driver, element_info, parent)
            if element is not None:
                break
        return element

    @staticmethod
    def __find_menu(driver, element_info, parent=None):
        """
        查找菜单控件
        参数：
        name 菜单及菜单项名，格式：菜单项名/子菜单项名/...
        parent_name 父控件名
        parent_control_type 父控件类型
        """
        items = element_info.get_menu_items()

        element = None
        actions = ActionChains(driver)

        if parent:
            for index, item in enumerate(items):
                element = ElementFinderUtils.find_element_by_type(element, item, ControlType.MENU_ITEM)
                if index < len(items) - 1:
                    actions.move_to_element(element).click().perform()
        else:
            for index, item in enumerate(items):
                element = DriverFinderUtils.find_element_by_type_wait(driver, item, ControlType.MENU_ITEM)
                if index < len(items) - 1:
                    actions.move_to_element(element).click().perform()
        return element

    @staticmethod
    def __find_combox_box(driver, element_info, parent=None):
        """
            查找组合框或列表项
            参数：
            name 组合框及列表项名，格式：组合框名/列表项名/，列表项名可为空
        """
        combo_box = ElementFinder.__find_main_element(driver, element_info, parent)

        if element_info.child_name:
            combo_box.click()
            return ElementFinderUtils.find_element_by_type(combo_box, element_info.child_name, ControlType.LIST_ITEM)
        else:
            return combo_box

    @staticmethod
    def __find_list_box(driver, element_info, parent=None):
        """
        查找列表框
        参数：
        name 列表框名，格式：列表框名/列表项名/菜单名，列表框名和菜单名可为空，只支持简单模式的弹出菜单
        """
        list_box = ElementFinder.__find_main_element(driver, element_info, parent)

        list_box.click()
        element = ElementFinderUtils.find_element_by_type(list_box, element_info.child_name, ControlType.LIST_ITEM)
        element = ElementFinder.__find_context_menu(driver, element, element_info.menu_item)

        return element

    @staticmethod
    def __find_list_view(driver, element_info, parent=None):
        """
            查找列表视图
            参数：
            name 列表视图名，格式：列表视图名/列表项序号/菜单名，列表视图名和菜单名可为空，只支持菜单模式的弹出菜单
        """

        list_view = ElementFinder.__find_main_element(driver, element_info, parent)

        element = ElementFinderUtils.find_element_by_type(list_view, element_info.child_name, ControlType.LIST_ITEM)
        element = ElementFinder.__find_context_menu(driver, element, element_info.menu_item)
        return element

    @staticmethod
    def __find_tree_view(driver, element_info, parent=None):
        """
            查找树视图
            参数：
            name 树视图名，格式：树视图名/树节点名/菜单名，树视图名和菜单名可为空，只支持菜单模式的弹出菜单
        """
        tree_view = ElementFinder.__find_main_element(driver, element_info, parent)

        if element_info.child_name:
            TreeUtils.expand_all(driver, tree_view)
            element = ElementFinderUtils.find_element_by_type(tree_view, element_info.child_name, ControlType.TREE_ITEM)
        else:
            element = tree_view

        if element_info.menu_item:
            element = ElementFinder.__find_context_menu(driver, element, element_info.menu_item)

        if element is not None:
            Logger.debug(LogType.FRAME, f"树或弹出菜单项为：{element}")

        return element

    @staticmethod
    def __find_table(driver, element_info, parent=None):
        """
            查找表格
            参数：
            name 表格名，格式：表格名/文本框名/菜单名，表格名和菜单名可为空，只支持菜单模式的弹出菜单
            返回：TableRow的数组或Edit
        """
        table = ElementFinder.__find_main_element(driver, element_info, parent)

        if element_info.child_name and ConvertType.of_code(element_info.child_name) is None:
            element = None

            table_rows = ElementFinderUtils.find_elements_by_type(table, None, ControlType.TABLE_ROW)
            for row_index, row in enumerate(table_rows):
                cells = ElementFinderUtils.find_elements_by_type(row, None, ControlType.EDIT)
                for cell_index, cell in enumerate(cells):
                    if cell.text == element_info.child_name:
                        element = cell
                        break
        else:
            element = table

        if element_info.menu_item:
            element = ElementFinder.__find_context_menu(driver, element, element_info.menu_item)

        if element is not None:
            Logger.debug(LogType.FRAME, f"表格或弹出菜单项为：{element}")

        return element
    
    @staticmethod
    def __find_datetime(driver, element_info, parent=None):
        """
        查找日期时间控件
        参数：
        name 日期时间控件名
        """
        if parent:
            dt = ElementFinderUtils.find_element_by_class(parent, element_info.name, 'SysDateTimePick32')
        else:
            dt = DriverFinderUtils.find_element_by_class(driver, element_info.name, 'SysDateTimePick32')

        return dt

    @staticmethod
    def __find_window(driver, element_info):
        """
        查找窗口
        参数：
        name 窗口名（关键词）
        """
        return driver.find_element(By.XPATH, f"//Window[contains(@Name, '{element_info.name}')]")
    
    @staticmethod
    def __find_context_menu(driver, element, menu_item_name):
        if menu_item_name:
            actions = ActionChains(driver)
            actions.move_to_element(element)
            actions.context_click(element).perform()

            try:
                menu = DriverFinderUtils.find_element_by_class(driver.root_driver, '上下文', '#32768')
                element = ElementFinderUtils.find_element_by_type(menu, menu_item_name, ControlType.MENU_ITEM)
            except (NoSuchElementException, InvalidSelectorException, WebDriverException) :
                element = DriverFinderUtils.find_element_by_type(driver, menu_item_name, ControlType.MENU_ITEM)

        return element

    @staticmethod
    def __find_main_element(driver, element_info, parent=None):
        try:
            if element_info.automation_id:
                if parent:
                    element = ElementFinderUtils.find_element_by_automation(parent, element_info.automation_id)
                else:
                    element = DriverFinderUtils.find_element_by_automation_wait(driver, element_info.automation_id)
            else:
                if parent:
                    element = ElementFinderUtils.find_element_by_type(parent, element_info.name, element_info.control_type)
                else:
                    element = DriverFinderUtils.find_element_by_type_wait(driver, element_info.name, element_info.control_type)

            if element_info.control_type.is_composite():
                offset = element_info.get_parent_offset(element.size['width'], element.size['height'])
                EventUtils.click(driver, element, offset)
        except NoSuchElementException as e:
            element = None
            Logger.debug(f'未找到主控件：{str(e)}')    # 模糊查找控件时，返回None正常
        except InvalidSelectorException as e:
            element = None
            Logger.debug(f'无效的控件选项：{str(e)}')  # 模糊查找控件时，返回None正常
        except TimeoutException as e:
            element = None
            Logger.debug(f'连接失败：{str(e)}')  # 模糊查找控件时，返回None正常
        except WebDriverException as e:
            element = None
            Logger.debug(f'连接失败或超时：{str(e)}')   # 模糊查找控件时，返回None正常

        return element

    @staticmethod
    def __find_parent(driver, element_info):
        parent = None
        if element_info.need_to_find_parent():
            try:
                Logger.debug(f'开始查找父控件：{element_info.parent_info()}')
                probe = TimeProbe.get_probe('查找父控件')

                if element_info.parent_id:
                    parent = DriverFinderUtils.find_element_by_automation_wait(driver, element_info.parent_id)
                elif element_info.parent_type:
                    parent = DriverFinderUtils.find_element_by_type_wait(driver, element_info.parent_name,
                                                                   element_info.parent_type)

                probe.write_log()
            except (NoSuchElementException, InvalidSelectorException, WebDriverException) as e:
                Logger.error(f'查找父控件失败：{element_info.parent_info()}')
                raise e

        return parent