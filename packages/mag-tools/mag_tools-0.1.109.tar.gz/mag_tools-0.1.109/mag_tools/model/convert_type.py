from model.base_enum import BaseEnum


class ConvertType(BaseEnum):
    ROTATE_90 = ('Rotate_90', '旋转90度')
    ROTATE_180 = ('Rotate_180', '旋转180度')
    ROTATE_270 = ('Rotate_270', '旋转270度')
    TRANSPOSE = ('Transpose', '转置')