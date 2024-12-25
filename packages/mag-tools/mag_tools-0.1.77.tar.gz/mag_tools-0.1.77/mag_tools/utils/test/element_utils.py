from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ElementUtils:
    @staticmethod
    def local_expression(name, control_type=None, class_name = None, automation_id = None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ElementUtils.global_expression(name, control_type, class_name, automation_id, parent_name, parent_control_type, extended_type)
        return f".{exp}"

    @staticmethod
    def global_expression(name, control_type=None, class_name = None, automation_id = None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ""
        if parent_name:
            parent_tag_name = f"{parent_control_type.__value}" if parent_control_type is not None else "*"
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
    def find_element_by_type(element, name, control_type=None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ElementUtils.local_expression(name, control_type, None, None, parent_name, parent_control_type, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_element_by_class(element, name, class_name=None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ElementUtils.local_expression(name, None, class_name, None, parent_name, parent_control_type, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_element_by_automation(element, automation_id, extended_type=None):
        exp = ElementUtils.local_expression(None, None, None, automation_id, None, None, extended_type)
        return element.find_element(By.XPATH, exp)

    @staticmethod
    def find_elements_by_type(element, name, control_type=None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ElementUtils.local_expression(name, control_type, None, None, parent_name, parent_control_type, extended_type)
        return element.find_elements(By.XPATH, exp)

    @staticmethod
    def find_elements_by_class(element, name, class_name=None, parent_name=None, parent_control_type=None, extended_type=None):
        exp = ElementUtils.local_expression(name, None, class_name, None, parent_name, parent_control_type, extended_type)
        return element.find_elements(By.XPATH, exp)

    @staticmethod
    def find_element_by_types(element, name, control_types, parent_name=None, parent_control_type=None, extended_type=None):
        ele = None
        for control_type in control_types:
            try:
                ele = ElementUtils.find_element_by_type(element, name, control_type, parent_name, parent_control_type, extended_type)
            except NoSuchElementException:
                pass
        return ele

