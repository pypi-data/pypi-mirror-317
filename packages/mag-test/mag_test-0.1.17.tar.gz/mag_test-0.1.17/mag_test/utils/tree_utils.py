from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mag_test.core.app_driver import AppDriver
from mag_test.model.control_type import ControlType
from mag_test.finder.element_finder_utils import ElementFinderUtils


class TreeUtils:
    @staticmethod
    def expand_all(driver:AppDriver, tree:WebElement):
        try:
            actionChains = ActionChains(driver)

            # 查找所有展开按钮
            tree_items = ElementFinderUtils.find_elements_by_type(tree, None, ControlType.TREE_ITEM)

            for tree_item in tree_items:
                # 双击展开
                actionChains.double_click(tree_item).perform()
                # # 等待子节点加载完成
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, './/Button[@content-desc="Expand"]')))
                # 递归展开子节点
                # TreeUtils.expand_all(driver, tree)
        except Exception as e:
            print(f"Error expanding nodes: {str(e)}")