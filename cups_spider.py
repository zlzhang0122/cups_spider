#!/usr/bin/python
#-*- encoding:UTF-8 -*-

import csv
import json
from pprint import pprint
import requests
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

class Cups():
    def __init__(self, url, page, path):
        self._url = url
        self._page = page
        self._path = path
        self._result = set()
        self.run()

    def run(self):
        """启动爬虫"""
        headers = {'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        urls = []
        urls.extend([self._url.format(1, p, 0) for p in range(1, self._page)])
        urls.extend([self._url.format(1, p, 1) for p in range(1, self._page)])
        urls.extend([self._url.format(3, p, 0) for p in range(1, self._page)])
        urls.extend([self._url.format(3, p, 1) for p in range(1, self._page)])
        for i,u in enumerate(urls):
            try:
                j = json.loads(requests.get(u, headers = headers, timeout = 2).text[15:])
                for i, v in enumerate(j['rateList']):
                    goods = (v['rateDate'], v['auctionSku'], v['rateContent'].replace("<b>", "").replace("</b>", "").replace("&hellip", ""))
                    self._result.add(goods)
                    print(i)
            except Exception as e:
                print(e)
        pprint(self._result)
        print(len(self._result))
        self.save()
        self.clear()

    def save(self):
        """保存数据到本地"""
        with open(self._path, "w+", encoding="gbk") as f:
            f_csv = csv.writer(f)
            f_csv.writerows(self._result)

    def clear(self):
        """数据去重"""
        s = set()
        with open(self._path, "r", encoding="gbk") as f:
            fin_csv = csv.reader(f)
            for row in fin_csv:
                s.add(tuple(row))
        with open("cup_all.csv", "w+", encoding="gbk") as f:
            fout_csv = csv.writer(f)
            fout_csv.writerows(s)
        print(len(s))

    @staticmethod
    def extract():
        """提取数据"""
        colorset = set();sizeset = set();colormap = {};sizemap = {};
        color_name_list_res = [];color_value_list_res=[];size_name_list_res=[];size_value_list_res=[];
        with open("cup_all.csv", "r", encoding="gbk") as f:
            fin_csv = csv.reader(f)
            for row in fin_csv:
                if row != '' and len(row) > 1:
                    color_size = row[1]
                    colors = color_size.split(";")[0]
                    sizes = color_size.split(";")[1]
                    if colors != "":
                        color_name_list = colors.split(":")
                        if len(color_name_list) > 1:
                            color_name = color_name_list[1]
                            if color_name != "":
                                colorset.add(color_name)
                                try:
                                    if (colormap[color_name] != ''):
                                        colormap[color_name] = colormap[color_name] + 1
                                except KeyError:
                                    colormap[color_name] = 1
                    if sizes != "":
                        size_name_list = sizes.split(":")
                        if len(size_name_list) > 1:
                            size_name = size_name_list[1]
                            if size_name != "":
                                sizeset.add(size_name)
                                try:
                                    if (sizemap[size_name] != ''):
                                        sizemap[size_name] = sizemap[size_name] + 1
                                except KeyError:
                                    sizemap[size_name] = 1
        with open("data_/cup_color.text", "w+", encoding="gbk") as fout:
            for key in colorset:
                fout.write(key + "\n")
        with open("data_/cup_size.text", "w+", encoding="gbk") as fout:
            for key in sizeset:
                fout.write(key + "\n")
        with open("data_/cup_color_count.text", "w+", encoding="gbk") as fout:
            for key in colormap:
                fout.write(key + ":" + str(colormap[key]) + "\n")
        with open("data_/cup_size_count.text", "w+", encoding="gbk") as fout:
            for key in sizemap:
                fout.write(key + ":" + str(sizemap[key]) + "\n")

        color_key_list = []
        for key in colormap.keys():
            color_key_list.append(key)
        color_key_list.sort()
        for key in color_key_list:
            color_name_list_res.append(key)
            color_value_list_res.append(colormap[key])

        size_key_list = []
        for key in sizemap.keys():
            size_key_list.append(key)
        size_key_list.sort()
        for key in size_key_list:
            size_name_list_res.append(key)
            size_value_list_res.append(sizemap[key])

        # for key in colormap:
        #     color_name_list_res.append(key)
        #     color_value_list_res.append(colormap[key])

        # for key in sizemap:
        #     size_name_list_res.append(key)
        #     size_value_list_res.append(sizemap[key])

        plt.figure(1)  # 创建颜色图表

        ax1 = plt.subplot(211)  # 在颜色图表中创建子图1
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.plot(color_name_list_res, color_value_list_res)
        plt.title(u'颜色分布', fontproperties=font)
        plt.xlabel(u'x轴', fontproperties=font)
        plt.ylabel(u'y轴', fontproperties=font)
        plt.grid(True)

        plt.figure(1)  # 创建大小图表
        ax2 = plt.subplot(212)  # 在大小图表2中创建子图2
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.plot(size_name_list_res, size_value_list_res)
        plt.title(u'大小分布', fontproperties=font)
        plt.xlabel(u'x轴', fontproperties=font)
        plt.ylabel(u'y轴', fontproperties=font)
        plt.grid(True)

        plt.sca(ax1)
        plt.sca(ax2)

        plt.show()

if __name__ == "__main__":
    url = "https://rate.tmall.com/list_detail_rate.htm?itemId=37457670144&spuId=249827344&" \
          "sellerId=470355944&order={}&currentPage={}&append=0&content={}"
    cups = Cups(url, 201, "cup_all.csv")
    cups.extract()