import calendar
import datetime
import os
import sys
import time
import pyautogui as pa


# 每次更新需要到setup中修改版本号，并重新打包编译
# python setup.py sdist   编译
# python setup.py develop 本地测试(可选)
# twine upload dist/*     上传到自己的pypi服务器
# 安装后【import Yusir】即可使用

def get_first_and_last_day():
    """return返回字符型和日期型【当天、当月第一天和最后一天】日期"""
    today = datetime.date.today()
    year = today.year
    month = today.month
    first_day = today.replace(day=1)
    last_day = today.replace(day=calendar.monthrange(year, month)[1])
    return (today.strftime('%Y%m%d'), first_day.strftime('%Y%m%d'), last_day.strftime('%Y%m%d'),
            today, first_day, last_day)


def locate_pic(path, match=0.85, repeat_count=77):
    """
    :param repeat_count: 重试次数，默认77次
    :param match: 匹配度，默认0.85
    :param path: 图片路径locate_pic(r'x.png')
    :return: 返回当前图片的坐标(x,y)
    """
    for cnt in range(repeat_count):
        try:
            time.sleep(1.5)
            return pa.locateOnScreen(path, confidence=match)
        except Exception as e:
            print(f"{path} try again...")
            time.sleep(1.5)
            continue
    sys.exit()


def get_file_modified_date(file_path):
    timestamp = os.stat(file_path)
    modified_time = datetime.datetime.fromtimestamp(timestamp.st_mtime).strftime('%Y%m%d%H')
    return modified_time


def flag(f1, f2):
    """
    :param f1: 文件1的路径
    :param f2: 文件2的路径
    :return:若文件修改时间等于当前时间则返回flag
    """
    erp = get_file_modified_date(f1)
    hd = get_file_modified_date(f2)
    th = datetime.datetime.now().strftime('%Y%m%d%H')
    if erp == th and hd == th:
        return 'flag'


if __name__ == '__main__':
    # loc_user = locate_pic(r'../img/user.png', 0.95)
    # print(loc_user)
    pass
