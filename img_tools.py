#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 21:28
# @Author  : Burning
# @File    : get_data.py
# @Software: PyCharm
import os
import numpy as np
import win32gui, win32ui, win32con
from PIL import Image, ImageGrab


def adb(name="img.png"):
    """
    使用ADB截图
    :param name: 截图名
    :return:
    """
    os.system(f"adb exec-out screencap -p > {name}")


def win_img(handle, name="img.png"):
    """
    使用windows原生API截图
    :param handle:
    :param name:截图名字
    :return:
    """
    left, top, width, height = win32gui.GetWindowRect(handle)
    mfcDC = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(handle))  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建bigmap准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)  # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)  # 截取从左上角（0，0）长宽为（w，h）的图片
    saveBitMap.SaveBitmapFile(saveDC, name)


def py_img(box):
    """
    :param box:left,top,width,height
    :return:截取的表达式区域图像
    """
    img = ImageGrab.grab(box)
    return img


def intercept(top_rate, button_rate, name="img.png"):
    """
    :param name:照片名
    :return: 表达式区域的图片
    """
    img = Image.open(name)
    w, h = img.size
    box = [0, top_rate * h, w, button_rate * h]  # 表达式区域
    region = img.crop(box)
    return region


def binarization(img, threshold=200):
    """
    :param img: 等式区域图像
    :param threshold: 二值化的阈值
    :return: 二值化后的图像
    """
    img = img.convert('L')  # 灰度化
    table = []
    for i in range(256):
        if i > threshold:
            table.append(1)
        else:
            table.append(0)
    bin_img = img.point(table, '1')
    return bin_img


def partition(img, direction=0):
    """
    :param img: 等式区域图像
    :param direction: 1为水平切割，0为垂直切割
    :return: 切割后的所有图像
    """
    imglist = np.array(img).sum(axis=direction)
    width, height = img.size
    res_img = []
    index = 0
    for img_sum in imglist:
        if img_sum == 0:  # 空白区域
            if (len(res_img) % 2) == 0:
                index += 1
                continue
            else:
                res_img.append(index)  # 结束区域
        else:  # 数字区域
            if (len(res_img) % 2) == 0:
                res_img.append(index)  # 开始位置
            else:
                index += 1
                continue
        index += 1
    if (len(res_img) % 2) != 0:  # 若最后不为0，将最后的结束区域加上
        res_img.append(index)
    imgs = []
    for i in range(0, int(len(res_img)), 2):
        start = res_img[i]
        end = res_img[i+1]
        if direction == 1:
            box = (0, start, width, end)  # 左上右下
            sub_img = img.crop(box)
            imgs.append(sub_img)
        else:
            box = (start, 0, end, height)  # 左上右下
            sub_img = img.crop(box)
            sub_img = sub_img.resize((60, 100))
            imgs.append(sub_img)
    return imgs


def get_exp( model, img):
    """
    :param img:  等式区域图像
    :param model: 预测模型
    :return: 等式
    """
    bin_img = binarization(img)
    #bin_img.show()
    hor_imgs = partition(bin_img, 1)  # 0为等式，1为结果
    expr = []
    for hor in hor_imgs:  # 列出等式与结果
        ver_imgs = partition(hor)  # 获取每个字符
        for ver in ver_imgs:  # 遍历每个字符
            sample = np.array(ver).reshape(1, -1).tolist()[0]  # 样本
           # a = np.array(ver)
            #b = np.linalg.eig(a)
            pre_value = model.predict([sample])[0]
            if pre_value == "=":
                expr.append(pre_value)
            expr.append(pre_value)
    res = "".join(expr)
    return res

