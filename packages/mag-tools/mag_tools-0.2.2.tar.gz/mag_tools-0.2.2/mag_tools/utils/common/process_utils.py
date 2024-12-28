import os

import psutil

'''
    进程处理工具
'''


class ProcessUtils(object):
    @staticmethod
    def find_app(app):
        running = None

        app_name = os.path.basename(app)
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == app_name.lower():
                running = proc
                break
        return running

    @staticmethod
    def terminate_app(app):
        app_name = os.path.basename(app)

        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == app_name:
                proc.terminate()
                break
