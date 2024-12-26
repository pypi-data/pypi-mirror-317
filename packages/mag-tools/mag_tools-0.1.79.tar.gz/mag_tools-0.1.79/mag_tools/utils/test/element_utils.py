from typing import List, Optional

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from mag_tools.model.control_type import ControlType


class ElementUtils:
    @staticmethod
    def local_expression(name:Optional[str], control_type:Optional[ControlType]=None, class_name:Optional[str] = None,
                         automation_id:Optional[str] = None, parent_name:Optional[str]=None,
                         parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.global_expression(name, control_type, class_name, automation_id, parent_name, parent_control_type, extended_type)
        return f".{exp}"

    @staticmethod
    def global_expression(name:Optional[str], control_type:Optional[ControlType]=None, class_name:Optional[str] = None,
                          automation_id:Optional[str] = None, parent_name:Optional[str]=None,
                          parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ""
        if parent_name:
            parent_tag_name = f"{parent_control_type.code}" if parent_control_type is not None else "*"
            exp = f"{exp}//{parent_tag_name}[@Name='{parent_name}']"

        tag_name = f"{control_type.code}" if control_type is not None else "*"
        exp = f"{exp}//{tag_name}"

        name_str = None
        if name:
            name_str = f"@Name='{name}'"
        if class_name:
            name_str = f"{name_str} and @ClassName='{class_name}'" if name_str else f"@ClassName='{class_name}'"
        if automation_id:
            name_str = f"{name_str} and @AutomationId='{automation_id}'" if name_str else f"@AutomationId='{automation_id}'"

        if name_str:
            exp = f"{exp}[{name_str}]"

        if extended_type:
            exp = f"{exp}//{extended_type.code}"

        return exp

    @staticmethod
    def find_element_by_type(element, name:Optional[str], control_type:Optional[ControlType]=None, parent_name:Optional[str]=None,
                             parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.local_expression(name, control_type, None, None, parent_name, parent_control_type, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_element_by_class(element, name:Optional[str], class_name:Optional[str]=None, parent_name:Optional[str]=None,
                              parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.local_expression(name, None, class_name, None, parent_name, parent_control_type, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_element_by_automation(element, automation_id:str, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.local_expression(None, None, None, automation_id, None, None, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_elements_by_type(element, name:Optional[str], control_type:Optional[ControlType]=None, parent_name:Optional[str]=None,
                              parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.local_expression(name, control_type, None, None, parent_name, parent_control_type, extended_type)
        return element.find_elements(By.XPATH, exp)

    @staticmethod
    def find_elements_by_class(element, name:str, class_name:Optional[str]=None, parent_name:Optional[str]=None,
                               parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        exp = ElementUtils.local_expression(name, None, class_name, None, parent_name, parent_control_type, extended_type)
        return element.find_elements(By.XPATH, exp)

    @staticmethod
    def find_element_by_types(element, name:str, control_types:List[ControlType], parent_name:Optional[str]=None,
                              parent_control_type:Optional[ControlType]=None, extended_type:Optional[ControlType]=None):
        ele = None
        for control_type in control_types:
            try:
                ele = ElementUtils.find_element_by_type(element, name, control_type, parent_name, parent_control_type, extended_type)
            except NoSuchElementException:
                pass
        return ele

    @staticmethod
    def find_table_cell_by_name(table, edit_name:Optional[str]):
        element = None
        if edit_name:
            table_rows = ElementUtils.find_elements_by_type(table, None, ControlType.TABLE_ROW)
            for row_index, row in enumerate(table_rows):
                cells = ElementUtils.find_elements_by_type(row, None, ControlType.EDIT)
                for cell_index, cell in enumerate(cells):
                    if cell.text == edit_name:
                        element = cell
                        break
        return element

    @staticmethod
    def find_table_cell_by_position(table, row:int, col:int):
        return table.find_element(By.XPATH, f".//TableRow[{row}]//Edit[{col}]")

    @staticmethod
    def set_table(table, data:List[List[str]]):
        table_rows = ElementUtils.find_elements_by_type(table, None, ControlType.TABLE_ROW)

        children = table.find_elements(By.XPATH, ".//*")
        for child in children:
            print(f"Tag Name: {child.tag_name}, Text: {child.text}")

        for row_index, row in enumerate(table_rows):
            cells = ElementUtils.find_element_by_type(row, None, ControlType.EDIT)
            for cell_index, cell in enumerate(cells):
                if row_index < len(data) and cell_index < len(data[row_index]):
                    cell_value = data[row_index][cell_index]
                    cell.send_keys(cell_value)