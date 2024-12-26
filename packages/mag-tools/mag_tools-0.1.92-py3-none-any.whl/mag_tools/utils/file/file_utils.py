import os
import shutil
from pathlib import Path


class FileUtils:
    @staticmethod
    def copy_and_overwrite(src:str, dst:str):
        """
        将源文件覆盖目标文件
        :param src: 源文件路径
        :param dst: 目标文件路径
        """
        src_path = Path(src)
        dst_path = Path(dst)

        # 确保目标文件所在目录存在
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        # 复制并覆盖文件
        shutil.copy2(src_path, dst_path)

    @staticmethod
    def clear_dir(dir_name):
        for filename in os.listdir(dir_name):
            file_path = os.path.join(dir_name, filename)  # 构建文件的完整路径
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)