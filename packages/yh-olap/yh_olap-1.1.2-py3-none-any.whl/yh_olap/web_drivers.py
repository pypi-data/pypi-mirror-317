import os
import subprocess
import shutil
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class Web_drives:
    @staticmethod
    def chrome(chrome_path=None):
        """判断谷歌驱动版本是否和谷歌浏览器版本一致"""
        # 谷歌浏览器可执行文件的完整路径
        if not chrome_path:
            chrome_path = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # 指定谷歌驱动目标位置
        # folder_path = os.getcwd()
        folder_path = os.path.split(os.path.realpath(__file__))[0]
        # 驱动名称
        file_name = 'chromedriver.exe'
        # 路径拼接
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            # 获取chromedriver.exe版本(谷歌浏览器驱动)
            result = subprocess.run([file_path, '--version'], capture_output=True, text=True)
            driverversion = '.'.join(result.stdout.strip().split(' ')[1].split('.')[:-1])

            # 获取chrome.exe版本(谷歌浏览器)
            command = f'wmic datafile where name="{chrome_path}" get Version /value'
            result_a = subprocess.run(command, capture_output=True, text=True, shell=True)
            output = result_a.stdout.strip()
            chromeversion = '.'.join(output.split('=')[1].split('.')[0:3])

            # 判断版本是否一致，不一致就重新下载
            if driverversion != chromeversion:
                # 使用ChromeDriverManager安装ChromeDriver，并获取驱动程序的路径
                download_driver_path = ChromeDriverManager().install()
                # 复制文件到目标位置
                shutil.copy(download_driver_path, folder_path)
            # else:
            #     print("版本一致，无需重新下载！")

        else:
            download_driver_path = ChromeDriverManager().install()
            shutil.copy(download_driver_path, folder_path)
        return file_path

    @staticmethod
    def edge(edge_path=None):
        # EDGE浏览器可执行文件的完整路径
        if not edge_path:
            edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

        # 指定EDGE驱动目标位置
        # folder_path = os.getcwd()
        folder_path = os.path.split(os.path.realpath(__file__))[0]
        # 驱动名称
        file_name = 'msedgedriver.exe'
        # 路径拼接
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            # 获取msedgedriver.exe版本(EDGE浏览器驱动)
            result = subprocess.run([file_path, '--version'], capture_output=True, text=True)
            driverversion = result.stdout.strip().split(' ')[3].strip()
            # msedge.exe版本(EDGE浏览器)
            powershell = f'(Get-Item -Path "{edge_path}").VersionInfo.FileVersion'
            p = subprocess.Popen(["powershell.exe", powershell], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                 shell=True)
            edgeversion = p.communicate()[0].decode().strip()
            if driverversion != edgeversion:
                download_driver_path = EdgeChromiumDriverManager().install()
                shutil.copy(download_driver_path, folder_path)
        else:
            download_driver_path = EdgeChromiumDriverManager().install()
            shutil.copy(download_driver_path, folder_path)
        return file_path
