from typing import Optional, Union

from mag_tools.model.base_enum import BaseEnum


class ActionType(BaseEnum):
    CLICK = ("{click}", "单击")   # 按钮、菜单、ITEM等控件的缺省操作
    DOUBLE_CLICK = ("{double_click}", "双击")
    RIGHT_CLICK = ("{right_click}", "右键单击")
    CLEAR = ("{clear}", "清除")
    SUBMIT = ("{submit}", "提交")
    SEND_KEYS = ("{send_keys}", "发送按键")
    # 以下为虚拟或组合的控件事件
    SET_TEXT = ("{set_text}", "设置文件")  # 文本框、文档等可编辑控件的缺省操作，相当于 CLEAR和SEND_KEYS
    SELECT = ("{select}", "选择")   #  # 应用于可选择控件
    CLEAR_DIR = ("{clear_dir}", "清除目录") # 应用于目录操作
    DELETE_FILE = ("{delete_file}", "删除文件") # 应用于文件操作
    MENU_ITEM = ("{menu_item}", "点击菜单项") # 为缺省操作

    @classmethod
    def of_code(cls, code: Optional[Union[str or int]]):
        """
        判定是否为菜单项，当菜单项名不为空且对应类型为None时，则缺省为菜单项
        :param code: 菜单项名
        """
        _type = super().of_code(code)
        if _type is None:
            _type = cls.MENU_ITEM
        return _type

if __name__ == '__main__':
    print(ActionType.of_code('aaa'))
