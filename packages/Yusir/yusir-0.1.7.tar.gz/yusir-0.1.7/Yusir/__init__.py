import calendar
import datetime
import os
import subprocess
import sys
import time
import pyautogui as pa
import pyperclip


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
        except Exception.args:
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


def wx_search_user(username, img_path):
    """
    搜索用户,并点击搜索到的用户，以便切换到用户界面
    :param img_path: 图片文件目录如：r'../img'
    :param username: 微信用户名
    :return:
    """
    for i in ['C:\\Program Files', 'D:\\Program Files', 'C:\\Program Files (x86)']:
        try:
            subprocess.Popen(fr'{i}\Tencent\WeChat\WeChat.exe')
            break
        except WindowsError:
            print(f'程序不在{i}\\Tencent\\WeChat\\WeChat.exe中')

    loc_user = locate_pic(fr'{img_path}\user.png')
    pa.click(loc_user.left + 77, loc_user.top + 12)
    pyperclip.copy(username)
    time.sleep(1)
    pa.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pa.click(loc_user.left + 77, loc_user.top + 98)


def send_msg_text(ps, img_path):
    """param ps: {'user': '微信用户名', 'msg': '要发送的文本内容'}"""
    wx_search_user(ps['user'], fr'{img_path}')  # 搜索用户并切换到用户界面
    # 点击文本输入框，并输入需要发送的文本内容和点击发送按钮
    loc_msg = locate_pic(fr'{img_path}\msg.png')
    pa.click(loc_msg.left + 100, loc_msg.top + 77)
    pyperclip.copy(ps['msg'])
    pa.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pa.press('enter')
    # 点击【关闭】按钮
    loc_close = locate_pic(fr'{img_path}\close.png')
    pa.click(loc_close.left + 12, loc_close.top + 12)


def send_msg_file(ps, img_path):
    """param ps: {'user': '微信用户名', 'filename': r'文件完整路径'}"""
    wx_search_user(ps['user'], fr'{img_path}')  # 搜索用户并切换到用户界面
    # 点击发送文件【图片按钮】
    loc_file = locate_pic(fr'{img_path}/filebtn.png')
    pa.click(loc_file.left + 10, loc_file.top + 10)
    time.sleep(2)
    pyperclip.copy(ps['filename'])
    pa.hotkey('ctrl', 'v')
    time.sleep(1)
    pa.press('enter')
    # 点击【发送】按钮
    loc_send = locate_pic(fr'{img_path}/sendbtn.png')
    pa.click(loc_send.left + 35, loc_send.top + 15)
    # 点击【关闭】按钮
    loc_close = locate_pic(fr'{img_path}/close.png')
    pa.click(loc_close.left + 12, loc_close.top + 12)


if __name__ == '__main__':
    pass
