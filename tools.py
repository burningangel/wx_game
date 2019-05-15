#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/5/1 21:46
# @Author  : Burning
# @File    : tools.py
# @Software: PyCharm
import os
import time

import pyautogui
import win32gui


def find_win(name):
    """
    :param name:窗口名
    :return: 窗口ID
    """
    handle = win32gui.FindWindow(None, name)  # 查找对应的窗口
    return handle


def adb_click(x=180, y=1090):
    """
    :param x:点击时手机屏幕的X坐标
    :param y: 点击时手机屏幕的Y坐标
    :return:
    """
    comment = f"adb shell input tap {x} {y}"
    os.system(comment)


def win_click(x, y):
    """
    :param x:桌面坐标X
    :param y: 桌面坐标Y
    :return:
    """
    pyautogui.FAILSAFE = True
    pyautogui.click(x, y, button='left')
