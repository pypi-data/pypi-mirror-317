from turtle import Turtle
from typing import List, Optional, Tuple

import numpy as np
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from mag_tools.model.control_type import ControlType
from mag_tools.utils.test.element_utils import ElementUtils


class TableUtils:
    @staticmethod
    def get_table_headers(table: WebElement) -> List[str]:
        headers = ElementUtils.find_elements_by_type(table, None, ControlType.HEADER)
        return [header.text for header in headers]

    @staticmethod
    def get_size(table: WebElement) -> Tuple[int, int]:
        table_items = ElementUtils.find_elements_by_type(table, None, ControlType.DATA_ITEM)
        headers = ElementUtils.find_elements_by_type(table, None, ControlType.HEADER)

        if not headers:
            raise ValueError("No headers found in the table.")

        column_num = len(headers)
        row_num = int(len(table_items) / column_num)
        return row_num, column_num

    @staticmethod
    def find_table_cell_by_name(table:WebElement, edit_name:Optional[str]):
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
    def find_table_cell_by_position(table:WebElement, row:int, col:int):
        return table.find_element(By.XPATH, f".//DataItem[{row}]//Edit[{col}]")

    @staticmethod
    def set_table(driver, table:WebElement, data:List[List[str]]):
        table_items = ElementUtils.find_elements_by_type(table, None, ControlType.DATA_ITEM)
        row_num, column_num = TableUtils.get_size(table)

        table_items_array = np.array(table_items).reshape((row_num, column_num)).tolist()
        for row_index in range(row_num):
            for col_index in range(column_num):
                data_item = table_items_array[row_index][col_index]
                cell = ElementUtils.find_element_by_type(data_item, None, ControlType.EDIT)
                if row_index < len(data) and col_index < len(data[row_index]):
                    actions = ActionChains(driver)
                    actions.move_to_element(cell).send_keys(data[row_index][col_index]).perform()

    @staticmethod
    def get_table_data(table:WebElement) -> List[List[str]]:
        table_data = [[]]
        table_items = ElementUtils.find_elements_by_type(table, None, ControlType.DATA_ITEM)
        row_num, column_num = TableUtils.get_size(table)

        table_items_array = np.array(table_items).reshape((row_num, column_num)).tolist()
        for row_index in range(row_num):
            for col_index in range(column_num):
                data_item = table_items_array[row_index][col_index]
                cell = ElementUtils.find_element_by_type(data_item, None, ControlType.EDIT)
                table_data[row_index][col_index] = cell.text

        return table_data