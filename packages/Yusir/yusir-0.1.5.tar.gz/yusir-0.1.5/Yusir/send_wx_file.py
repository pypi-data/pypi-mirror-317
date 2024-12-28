import sys
import pyautogui
import pyperclip
import subprocess
from __init__ import locate_pic
import time


def wx_search_user(username):
    """
    搜索用户,并点击搜索到的用户，以便切换到用户界面
    :param username: 微信用户名
    :return:
    """
    for i in ['C:\\Program Files', 'D:\\Program Files', 'C:\\Program Files (x86)']:
        try:
            subprocess.Popen(fr'{i}\Tencent\WeChat\WeChat.exe')
            break
        except WindowsError:
            print(f'程序不在{i}\\Tencent\\WeChat\\WeChat.exe中')

    loc_user = locate_pic(r'../img/user.png')
    pyautogui.click(loc_user.left + 77, loc_user.top + 12)
    pyperclip.copy(username)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.click(loc_user.left + 77, loc_user.top + 98)


def send_msg_text(ps):
    """param ps: {'user': '微信用户名', 'msg': '要发送的文本内容'}"""
    wx_search_user(ps['user'])  # 搜索用户并切换到用户界面
    # 点击文本输入框，并输入需要发送的文本内容和点击发送按钮
    loc_msg = locate_pic(r'../img/msg.png')
    pyautogui.click(loc_msg.left + 100, loc_msg.top + 77)
    pyperclip.copy(ps['msg'])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1.5)
    pyautogui.press('enter')
    # 点击【关闭】按钮
    loc_close = locate_pic(r'../img/close.png')
    pyautogui.click(loc_close.left + 12, loc_close.top + 12)


def send_msg_file(ps):
    """param ps: {'user': '微信用户名', 'filename': r'文件完整路径'}"""
    wx_search_user(ps['user'])  # 搜索用户并切换到用户界面
    # 点击发送文件【图片按钮】
    loc_file = locate_pic(r'../img/filebtn.png')
    pyautogui.click(loc_file.left + 10, loc_file.top + 10)
    time.sleep(2)
    pyperclip.copy(ps['filename'])
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.press('enter')
    # 点击【发送】按钮
    loc_send = locate_pic(r'../img/sendbtn.png')
    pyautogui.click(loc_send.left + 35, loc_send.top + 15)
    # 点击【关闭】按钮
    loc_close = locate_pic(r'../img/close.png')
    pyautogui.click(loc_close.left + 12, loc_close.top + 12)


if __name__ == '__main__':
    # send_msg_text({'user': '糊涂虫', 'msg': '风华正茂'})  # {'user':'糊涂虫','msg':'风华正茂'}
    send_msg_file({'user': '糊涂虫', 'filename': r'D:\2024\001.png'})
    pass
