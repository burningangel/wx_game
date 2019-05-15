#!/usr/bin/env python3
# encoding: utf-8
"""
@author: burning
@software: pycharm
@file: main.py
@time: 2019/4/26 14:29
@desc:
"""
import os
import time
import yaml
import uuid
import model
import argparse
import img_tools
import tools
import win32gui
from sklearn.externals import joblib


def main(mode, n=40):
    count = 1  # 当前处于题目数
    model = joblib.load(config['model'])
    if mode == 0:  # adb
        while count <= n:
            img_tools.adb()
            region = img_tools.intercept(config['expr']['y'], config['expr']['height'])
            expr = img_tools.get_exp( model, region)
            print(f"第{count}题：{expr}\t", end="")
            if eval(expr):
                tools.adb_click(config['adb']['right']['x'], config['adb']['right']['y'])
                print("True")
            else:
                tools.adb_click(config['adb']['error']['x'], config['adb']['error']['y'])
                print("False")
            count += 1
    else:
        hd = tools.find_win(mode)
        left, top, width, height = win32gui.GetWindowRect(hd)
        box = (config['expr']['x']*left, config['expr']['y']*height, config['expr']['width']*width, config['expr']['height']*height)
        old_expr = ""
        while count <= n:
            region = img_tools.py_img(box)
            expr = img_tools.get_exp(model, region)
            y = int(config['win']['right']['y']*height)
            if expr == old_expr or expr == "":
                continue
            else:
                print(f"第{count}题：{expr}\t", end="")
                if eval(expr):
                    x = int(config['win']['right']['x'] * width)
                    tools.win_click(x, y)
                    print("True")
                else:
                    x = int(config['win']['error']['x'] * width)
                    tools.win_click(x, y)
                    print("False")
            old_expr = expr
            count += 1
            if count <= 270:
                time.sleep(0.5)


def debug(mode):
    """
    debug 模式，获取单个字符并保存
    :return:
    """
    while True:
        name = "screenshot/" + str(uuid.uuid1()) + ".png"
        if mode == 0:  # adb
            img_tools.adb(name)
            region = img_tools.intercept(name)
        else:  # 投屏
            hd = tools.find_win(mode)
            left, top, width, height = win32gui.GetWindowRect(hd)
            box = (config['expr']['x'] * left, config['expr']['y'] * height, config['expr']['width'] * width,
                   config['expr']['height'] * height)
            region = img_tools.py_img(box)
            region.save(name)
        save_dir = "singleChar"
        bin_img = img_tools.binarization(region)
        hor_imgs = img_tools.partition(bin_img, 1)  # 0为等式，1为结果
        for hor in hor_imgs:  # 列出等式与结果
            ver_imgs = img_tools.partition(hor)  # 获取每个字符
            for ver in ver_imgs:  # 遍历每个字符
                name = f"{save_dir}\{str(uuid.uuid1())}.png"
                ver.save(name)
                print(f"保存文件{name}")
        print("保存完毕！")
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.description = "加减王者自动答题"
    parser.add_argument('-d', "--debug", action='store_true', help='开启DEBUG模式')
    parser.add_argument('-m', "--model", action='store_true', help='训练模型')
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    config = yaml.load(open("config.yaml",encoding="UTF-8"), Loader=yaml.FullLoader)
    iphone_name = config['name']

    if args.debug:
        name = "singleChar"
        if not os.path.exists(name):
            os.mkdir(name)
        input("DEBUG模式：准备开始答题，按ENTER键开始\n")
        debug(iphone_name)
    elif args.model:
        name = "trainData"
        if not os.path.exists(name):
            os.mkdir(name)
        model.train_model()
    else:
        input("准备开始答题，按ENTER键开始\n")
        main(iphone_name, config['times'])
