from typing import Any, Dict, List

import pytest

from mag_test.core.app_driver import AppDriver
from mag_test.model.function_status import FunctionStatus
from mag_test.model.test_component_type import TestComponentType

from mag_test.bean.base_test import BaseTest
from mag_test.bean.function import Function


class Case(BaseTest):
    def __init__(self, home_dir:str, plan_id:str, name:str, description:str, functions:List[Function],
                 index:int, status:FunctionStatus=FunctionStatus.NORMAL):
        super().__init__(home_dir, name, index, TestComponentType.CASE, description)
        self.__plan_id = plan_id
        self.__functions = functions
        self.__status = status if status else FunctionStatus.NORMAL

    @pytest.mark.benchmark
    def start(self, driver:AppDriver):
        if self.__status == FunctionStatus.NORMAL:
            test_failed = False
            for function in self.__functions:
                if test_failed:
                    function.skip()
                else:
                    driver = function.start(driver)
                    if function.is_fail():
                        self.fail('该用例测试失败')
                        test_failed = True

            super()._report()

        return driver

    def append(self, function:Function):
        self.__functions.append(function)

    @staticmethod
    def from_map(home_dir:str, plan_id:str, index:int, data:Dict[str, Any]):
        name = data.get('name')
        description = data.get('desc')
        status = FunctionStatus[data.get('status')]

        case = Case(home_dir, plan_id, name, description, [], index, status)

        for function_index, function_item in enumerate(data.get('functions'), start=1):
            function_id = function_item.get('id')
            function_name = function_item.get('name', '')

            function = Function(home_dir, plan_id, function_id, index, function_name)
            case.append(function)

        return case