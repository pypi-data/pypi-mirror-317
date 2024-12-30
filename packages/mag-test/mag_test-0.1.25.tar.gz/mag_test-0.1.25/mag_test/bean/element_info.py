import json
from typing import Any, Optional

from mag_tools.utils.common.string_utils import StringUtils

from mag_test.model.control_type import ControlType
from mag_test.model.init_status import InitStatus


class ElementInfo:
    """
    控件信息，用于查询条件
    """
    def __init__(self, name:Optional[str]=None, element_type:Optional[ControlType]=None, automation_id:Optional[str]=None,
                 class_name:Optional[str]=None, parent_name:Optional[str] = None,parent_type:Optional[ControlType]=None,
                 parent_id:Optional[str]=None, parent_class:Optional[str]=None, value:Optional[Any]=None,pop_window:Optional[str]=None):
        """
        控件信息，用于查询条件
        :param name: 控件名
        :param automation_id: 控件标识，AutomationId（AccessibilityId）
        :param element_type: 控件类型,不能为空
        :param class_name: 控件类名
        :param parent_name: 父控件名
        :param parent_id: 父控件标识，AutomationId（AccessibilityId）
        :param parent_type: 父控件类型
        :param parent_class: 父控件类名
        """
        self.__full_name = name
        self.__full_automation_id = automation_id
        self.control_type = element_type
        self.class_name = class_name
        self.parent_name = parent_name
        self.parent_type = parent_type
        self.parent_id = parent_id
        self.parent_class = parent_class
        self.value = value
        self.pop_window = pop_window

    @property
    def name(self):
        items = self.__full_name.split('/') if self.__full_name else None
        name_item = items[0] if items and len(items) > 0 else None
        name, _, _ = StringUtils.split_by_keyword(name_item, '{}')
        return name

    @property
    def automation_id(self):
        items = self.__full_automation_id.split('/') if self.__full_automation_id else None
        id_item = items[0] if items and len(items) > 0 else None
        automation_id, _, _ = StringUtils.split_by_keyword(id_item, '{}')

        return automation_id

    @property
    def init_status(self):
        items = self.__full_name.split('/') if self.__full_name else self.__full_automation_id.split('/') if self.__full_automation_id else None
        _item = items[0] if items and len(items) > 0 else None
        _, init_status, _ = StringUtils.split_by_keyword(_item, '{}')
        return InitStatus.of_code(init_status)

    @property
    def child_name(self):
        items = self.__full_name.split('/') if self.__full_name else self.__full_automation_id.split('/') if self.__full_automation_id else None

        child_name = items[1] if items and len(items) == 3 else None
        return child_name

    @property
    def action(self):
        """
        操作类型，为ActionType，如为None，则
        """
        items = self.__full_name.split('/') if self.__full_name else self.__full_automation_id.split('/') if self.__full_automation_id else None

        action = items[2] if len(items) == 3 else items[1] if len(items) == 2 else None
        return action

    def get_menu_items(self):
        return self.__full_name.split('/') if self.__full_name else []

    def need_to_find_parent(self):
        return self.control_type and self.control_type.is_composite() and (self.parent_type or self.parent_id)

    def get_offset(self, default_width=0, default_height=0)->Optional[tuple[int, int]]:
        offset = None
        if self.value:
            value_map = json.loads(self.value)
            if value_map.get('offset_x') or value_map.get('offset_y'):
                offset_x = value_map.get('offset_x') if value_map.get('offset_x') else default_width // 2
                offset_y = value_map.get('offset_y') if value_map.get('offset_y') else default_height // 2
                offset = (offset_x, offset_y)
        return offset

    def get_parent_offset(self, default_width=0, default_height=0)->Optional[tuple[int, int]]:
        offset = None
        if self.value:
            value_map = json.loads(self.value)
            if value_map.get('offset_X') or value_map.get('offset_Y'):
                offset_x = value_map.get('offset_X') if value_map.get('offset_X') else default_width // 2
                offset_y = value_map.get('offset_Y') if value_map.get('offset_Y') else default_height // 2
                offset = (offset_x, offset_y)
        return offset

    def is_virtual_control(self):
        return self.control_type and self.control_type.is_virtual()

    def __str__(self):
        attributes = {k: v for k, v in self.__dict__.items() if v is not None}
        return f"ElementInfo({', '.join(f'{k}={v}' for k, v in attributes.items())})"

    def parent_info(self):
        parent_attributes = {'parent_name': self.parent_name,
                             'parent_type': self.parent_type,
                             'parent_id': self.parent_id,
                             'parent_class': self.parent_class}
        parent_info = {k: v for k, v in parent_attributes.items() if v is not None}
        if parent_info:
            return f"ParentInfo({', '.join(f'{k}={v}' for k, v in parent_info.items())})"
        else:
            return "ParentInfo(None)"

    def self_info(self):
        self_attributes = {'name': self.__full_name,
                           'type': self.control_type,
                           'automation_id': self.__full_automation_id,
                           'class': self.class_name}

        self_info = {k: v for k, v in self_attributes.items() if v is not None}
        if self_info:
            return f"ElementInfo({', '.join(f'{k}={v}' for k, v in self_info.items())})"
        else:
            return "ElementInfo(None)"