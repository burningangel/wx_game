#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/23 20:59
# @Author  : Burning
# @File    : model.py
# @Software: PyCharm
from sklearn import tree
from sklearn.externals import joblib
import numpy as np
from PIL import Image
import os


def load_data():
    train_data = []
    train_target = []
    for root, dirs, files in os.walk("trainData"):
        if len(files) == 0:
            continue
        var = root.split(os.sep)[-1]
        for file in files:
            img_path = os.path.join(root, file)
            img = Image.open(img_path)
            sample = np.array(img).reshape(1, -1).tolist()[0]  # 样本
            train_data.append(sample)
            train_target.append(var)
    return train_data, train_target


def train_model():
    train_data, train_target = load_data()
    #from sklearn.model_selection import train_test_split
    #X_train, X_test, y_train, y_test = train_test_split(train_data, train_target, test_size =0.3, random_state = 0)
    #model = tree.DecisionTreeClassifier()
    #model = model.fit(X_train, y_train)
    #print(model.score(X_test, y_test))
    model = tree.DecisionTreeClassifier()
    model = model.fit(train_data, train_target)
    joblib.dump(model, 'model.pkl')
    print("模型训练保存完毕！")


if __name__=="__main__":
    train_model()

