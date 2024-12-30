import json
import os

import pytest

from mag_test.bean.base_test import BaseTest
from mag_test.bean.step import Step
from mag_test.core.app_driver import AppDriver
from mag_test.model.control_type import ControlType
from mag_test.model.test_component_type import TestComponentType
from mag_test.model.usage_status import UsageStatus


class Function(BaseTest):
    def __init__(self, home_dir:str, plan_id:str, function_id:str, index:int, name:str, status:UsageStatus=UsageStatus.NORMAL):
        super().__init__(home_dir, name, index, TestComponentType.FUNCTION, None, status)
        self.__plan_id = plan_id
        self.__id = function_id  # 功能标识
        self.__steps = []

        self.__read()

    @pytest.mark.benchmark
    def start(self, driver:AppDriver)->AppDriver:
        """
        启动测试功能
        :param driver: AppDriver
        """
        if self._status != UsageStatus.NORMAL:
            return driver

        test_failed = False
        for step in self.__steps:
            if test_failed:
                step.skip()
            else:
                driver = step.start(driver)
                if step.is_fail():
                    self.fail('该功能测试失败')
                    test_failed = True

        super()._report()
        return driver

    def __read(self):
        function_file = os.path.join(self.script_dir, self.__plan_id, f'{self.__id}.json')
        with open(function_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data['name']:
                self._name = data['name']
                self._status = UsageStatus[data['status']]

            for index, item in enumerate(data.get('elements', []), start=1):
                step = Step(self._home_dir,
                            item.get("step", None),
                            item.get("control_name", None),
                            ControlType[item.get('control_type')] if item.get('control_type') else None,
                            item.get('id', None),
                            item.get('value', None),
                            self._index,
                            index,
                            item.get('parent', None),
                            ControlType[item.get('parent_type')] if item.get('parent_type') else None,
                            item.get('parent_id', None),
                            item.get('pop', None))
                self.__steps.append(step)