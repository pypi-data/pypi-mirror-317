# Author: Yu-Xin Tian, 2024-12-23 Version 1.0.5

import sympy
sympy_names = dir(sympy)
from sympy import *
import numpy as np
import os, pickle
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import copy
import matplotlib.ticker as ticker
from matplotlib import rcParams

from IPython.display import display
from IPython.display import Math
from sympy.printing import latex

import string
import re
import platform
import ast
# from pkg_resources import resource_string

def set_font(label):
    """根据标签内容判断使用合适的字体，不影响 LaTeX 解析"""
    system = platform.system()
    if re.search(r'[\u4e00-\u9fff]', label):
        return 'SimSun'  # Windows 系统使用SimSun
    else:
        return 'Times New Roman'


# 设置 matplotlib 字体为支持中英文的字体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


def gen_letters(nums):
    # 生成大写字母
    uppercase_letters = string.ascii_uppercase

    # 列出36个大写字母
    letters = []
    for i in range(nums):
        if i < 26:
            letters.append(uppercase_letters[i])
        else:
            div, mod = divmod(i - 26, 26)
            letters.append(uppercase_letters[div] + uppercase_letters[mod])
    return letters


def gen_romans(nums):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_lists = []
    for num in range(1, nums+1):
        roman_num = ''
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i]
                num -= val[i]
            i += 1
        roman_lists.append(roman_num)
    return roman_lists


def mathshow(latex_code):
    display(Math(latex_code) )


def showlatex(sym):
    print(latex(sym, mode='inline'))


def mathprint(sym):
    mathshow(latex(sym))


config = {
    "font.family":'serif',
    "font.size": 12,
    "mathtext.fontset":'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
          'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']
m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']
ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]
locations = {
    'best': 0,
    'northeast': 1,
    'northwest': 2,
    'southwest':3,
    'southeast':4,
    'east':7,
    'west':6,
    'south':8,
    'north':9,
    'center':10
}

def exist_file(file_dir):
    return os.path.exists(file_dir)


def save_var(the_var, file_dir):
    with open(file_dir, 'wb') as f:
        pickle.dump(the_var, f)


def get_var(file_dir):
    if not exist_file(file_dir):
        print('文件不存在！')
        return
    else:
        with open(file_dir, 'rb') as f:
            loaded_var = pickle.load(f)
        return loaded_var


def data_lines(data,
               label_x=None,
               x_name=None,
               y_name=None,
               save_dir=None,
               location='best',
               ncol=1,
               fsize=14,
               figsize=[5, 4],
               xt_rotation=0,
               xrotation=0,
               yrotation=90,
               linestyles=None,
               linewidth=1,
               markers=m_list,
               markersize=3.5,
               colors=c_list,
               isgrid=False,
               xpad=3,
               ypad=3,
               xlabelpad=3,
               ylabelpad=3,

               xlabelsize='auto',
               ylabelsize = 'auto',
               legendsize = 'auto'
               ):
    """
    - data: 传入的数据，列表或np.array均可。（必须）
    - label_x: 横轴刻度标签，默认连续数字。
    - x_name: 横轴名称标签，默认'$x$'。
    - y_name: 纵轴名称标签，默认'$y$'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
    - xt_rotation: 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
    - xrotation: 横轴名字标签旋转角度，默认值0，基本不需要动。
    - yrotation: 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
         https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles

    - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
    - markers: 一组标记符号，`[]`列表形式去写，在多线图中用于按顺序制定每个线的标记符号。工具内的标记符号列表`m_list`。如果只有一条线，就取`m_list`中的第一个，即圆点'o'。
      本工具中提供的标记符号列表如下：
      ``m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']``
      关于标记符号的详细说明：
          https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers

    - markersize: 标记符号的大小，默认3.5。
    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一条线，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
        https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors
    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
    """
    fig, ax = plt.subplots(figsize=figsize)
    plt.xticks(fontsize=fsize, fontname='times new roman', rotation = xt_rotation)
    plt.yticks(fontsize=fsize, fontname='times new roman')

    data_names = list(data.keys())
    data_num = len(data_names)

    the_x = [i+1 for i in range(len(data[data_names[0]]))]

    plt.xlim(the_x[0], the_x[1])

    if len(the_x) > 10:
        labelevery = int(len(the_x)/10)
    else:
        labelevery = 1

    if label_x is None:
        label_x = []

        for i_, x_ in enumerate(the_x):
            if i_ % labelevery == 0:
                label_x.append(str(x_))
            else:
                label_x.append('')
    else:
        for i_, _ in enumerate(the_x):
            if i_ % labelevery != 0:
                label_x[i_] = ''
            else:
                label_x[i_] = str(label_x[i_])

    ax.set_xticks(the_x)
    ax.set_xticklabels(label_x, fontsize=fsize, fontname = 'times new roman')

    if data_num == 1:
        if y_name is None:
            y_name = data_names[0]
        ys = data[data_names[0]]
        ax.plot(the_x, ys, linestyle='-', c='k', linewidth=linewidth, marker='o', markersize=markersize)
        y_min = np.min(ys)
        y_max = np.max(ys)
    else:
        for j, em in enumerate(data_names):
            if linestyles is None:
                the_ls = '-'
            else:
                the_ls = linestyles[j]

            ys = data[em]

            if len(the_x) > 10:
                markevery = int(len(the_x)/10)
                ax.plot(the_x, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize, markevery = markevery, label=em)
            else:
                ax.plot(the_x, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize,label=em)

            y_min_now = np.min(ys)
            y_max_now = np.max(ys)
            if j ==0:
                y_max = y_max_now
                y_min = y_min_now
            else:
                if y_max_now > y_max:
                    y_max = y_max_now
                if y_min_now < y_min:
                    y_min = y_min_now

    judge_y = max(abs(y_max),abs(y_min))
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0),useMathText=True)


    if legendsize == 'auto':
        legendsize = fsize

    if data_num >1:
        ax.legend(loc=locations[location], fontsize=legendsize, ncol=ncol)

    # 设置 x 和 y 标签字体
    x_font = set_font(x_name)
    y_font = set_font(y_name)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad, fontname=y_font)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad, fontname=x_font)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    ax.grid(isgrid)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_lines(expressions,
               assigns,
               the_var,
               ranges,
               x_name='x',
               y_name='y',
               save_dir=None,
               location='best',
               ncol=1,
               fsize=14,
               figsize=[5, 4],
               xt_rotation=0,
               xrotation=0,
               yrotation=90,
               linestyles=None,
               linewidth=1,
               markers=m_list,
               markersize=3.5,
               colors=c_list,
               isgrid=False,
               x_lim=None,
               y_lim=None,
               xpad=3,
               ypad=3,
               xlabelpad=3,
               ylabelpad=3,
               xlabelsize='auto',
               ylabelsize='auto',
               legendsize='auto'
               ):
    """
    - expressions: Symbol表达式，字典形式传入。（必须）
    - assigns: 表达式参数赋值，字典形式。
    - the_var: 要分析的参数；
    - ranges: 要分析的参数的取值。[初始,结束,间隔]
    - x_name: 横轴名称标签，默认'x'。
    - y_name: 纵轴名称标签，默认'y'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
    - xt_rotation: 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
    - xrotation: 横轴名字标签旋转角度，默认值0，基本不需要动。
    - yrotation: 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
         https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles
    - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
    - markers: 一组标记符号，`[]`列表形式去写，在多线图中用于按顺序制定每个线的标记符号。工具内的标记符号列表`m_list`。如果只有一条线，就取`m_list`中的第一个，即圆点'o'。
      本工具中提供的标记符号列表如下：
      ``m_list = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']``
      关于标记符号的详细说明
           https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers

    - markersize: 标记符号的大小，默认3.5。
    - colors: 一组颜色，`[]`列表形式去写，在多线图中用于按顺序制定每个线的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一条线，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
         https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors

    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - x_lim: 横轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。
    - y_lim: 纵轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。举个例子，“2.2 画单条曲线图”部分不太好看.
    - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。
    """

    if expressions is None:
        print('注意：请输入表达式！ Note: Please enter expressions!')
        return None

    if the_var is None or ranges is None:
        print(
            '注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!')
        return None

    fig, ax = plt.subplots(figsize=figsize)
    # 设置 x 和 y 标签字体
    x_font = set_font(x_name)
    y_font = set_font(y_name)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad, fontname=y_font)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad, fontname=x_font)

    plt.xticks(fontsize=fsize, fontname='times new roman', rotation = xt_rotation)
    plt.yticks(fontsize=fsize, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    ranges_ = [ranges[0], ranges[1]+ranges[2], ranges[2]]
    if x_lim is None:
        plt.xlim(ranges[0], ranges[1])
    else:
        plt.xlim(x_lim[0], x_lim[1])

    if y_lim is not None:
        plt.ylim(y_lim[0], y_lim[1])

    if exp_num == 1:
        xs = []
        ys = []
        the_exp = expressions[exp_names[0]]
        if assigns is None:
            assigned_exp = the_exp
        else:
            assigned_exp = the_exp.subs(assigns)
        for i in np.arange(*ranges_):
            xs.append(i)
            ys.append(assigned_exp.subs({the_var:i}).evalf())
        ax.plot(xs, ys, linestyle='-', c='k', linewidth=linewidth, marker=None)
        y_min = np.min(ys)
        y_max = np.max(ys)
    else:
        for j, em in enumerate(exp_names):
            xs = []
            ys = []
            the_exp = expressions[exp_names[j]]
            if assigns is None:
                assigned_exp = the_exp
            else:
                assigned_exp = the_exp.subs(assigns)
            for i in np.arange(*ranges_):
                xs.append(i)
                ys.append(assigned_exp.subs({the_var: i}).evalf())

            if linestyles is None:
                the_ls = '-'
            else:
                the_ls = linestyles[j]

            if len(xs) > 10:
                markevery = int(len(xs)/10)
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize, markevery = markevery, label=em)
            else:
                ax.plot(xs, ys, linestyle=the_ls, c=colors[j], linewidth=linewidth, marker=markers[j], markersize=markersize,label=em)


            y_min_now = np.min(ys)
            y_max_now = np.max(ys)
            if j ==0:
                y_max = y_max_now
                y_min = y_min_now
            else:
                if y_max_now > y_max:
                    y_max = y_max_now
                if y_min_now < y_min:
                    y_min = y_min_now

    judge_y = max(abs(y_max),abs(y_min))
    judge_x = max(abs(np.max(xs)),abs(np.min(xs)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    if legendsize == 'auto':
        legendsize = fsize

    if exp_num >1:
        ax.legend(loc=locations[location], fontsize=legendsize, ncol=ncol)
    ax.grid(isgrid)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_3D(expressions,
            assigns,
            the_var_x,
            start_end_x,
            the_var_y,
            start_end_y,
            x_name='x',
            y_name='y',
            z_name='z',
            save_dir=None,
            color_alpha=0.8,
            linestyles=ls_list,
            linewidth=0.2,
            location='best',
            ncol=1,
            fsize=14,
            figsize=[7, 5],
            precision=1000,
            xrotation=0,
            yrotation=0,
            zrotation=90,
            isgrid=True,
            density=100,
            colors=c_list,
            edgecolor=None,
            x_lim=None,
            y_lim=None,
            z_lim=None,
            elevation=15,
            azimuth=45,
            roll=0,
            left_margin=0,
            bottom_margin=0,
            right_margin=1,
            top_margin=1,
            xpad=1,
            ypad=1,
            zpad=5,
            xlabelpad=2,
            ylabelpad=2,
            zlabelpad=12,
            xlabelsize='auto',
            ylabelsize='auto',
            zlabelsize='auto',
            legendsize='auto'
            ):
    """
    - expressions: Symbol表达式，字典形式传入。（必须）
    - assigns: 表达式参数赋值，字典形式。
    - the_var_x/the_var_y: 要分析的参数1/2；
    - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
    - x_name: x轴名称标签，默认'x'。
    - y_name: y轴名称标签，默认'y'。
    - z_name: z轴名称标签，默认'z'。
    - save_dir=None: 图片保存路径，字符串。默认None，不保存。
    - color_alpha: 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。默认取0.8。
    - linestyles: 一组线的形状，`[]`列表形式去写，在多线图中用于按顺序制定每个线的形状。如实线'-'，点横线'-.'，虚线'--'，点线':'。默认值为None，表示取工具内的线型列表`ls_list`得第一个，即实线'-'。
      本工具中提供的线型列表如下：
      ``ls_list = ['-', (0, (1, 10)), (0, (5, 10)),'-.','--', ':', (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]``
      关于线型的详细说明：
          https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html#linestyles

    - linewidth: 线粗。字面意思，没啥好说的，默认值为0.2。
    - location: 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。默认值为'best'，表示自动安排至合适的位置。
    - ncol: 图例的列数，默认为1列，即竖着排布。
    - fsize: 图片中字号的大小，默认值为14。
    - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[7, 5]`。
    - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
    - xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。
    - zrotation: Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴，但看的话需要歪脖子，专治脊椎不好使哈。
    - isgrid: 是否要网格。要就填True，不要就是False，默认不要。
    - density: 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。
    - colors: 一组颜色，`[]`列表形式去写，在多面图中用于按顺序制定每个面的颜色（包含标记符号的颜色）。工具内的颜色列表`c_list`。如果只有一张面，就取`c_list`中的第一个，即蓝色'blue'。
      本工具中提供的颜色列表如下：
      ``c_list = ['blue', 'gold', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo',
              'chocolate', 'olivedrab', 'teal', 'navy', 'firebrick','darkgreen', 'purple', 'cadetblue']``
      关于颜色的详细说明：
          https://matplotlib.org/stable/gallery/color/named_colors.html#base-colors

    - edgecolor: 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。
    - x_lim,y_lim,z_lim: x/y/z轴显示的范围，以`[起始值,结束值]`的形式去写。默认None，根据数据自动安排。除非不好看再调，一般不动该参数。
    - elevation: 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。当elevation为正值时，观察者向上倾斜，负值则表示向下倾斜。默认15度。可根据美观与否微调。
    - azimuth: 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。azim 的角度范围是 −180 到 180 度，其中正值表示逆时针旋转，负值表示顺时针。默认45度。可根据美观与否微调。
    - roll: 滚动角 (roll)。 定义了绕观察者视线方向旋转的角度。它决定了观察者的头部倾斜程。默认0度，不需要动。
    - left_margin=0, bottom_margin=0, right_margin=1, top_margin=1: 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。
    - xpad=1, ypad=1, zpad=5, xlabelpad=2, ylabelpad=2, ylabelpad=12: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。如果挤了不好看了，再微调此参数，一般不用动。
    """

    if expressions is None:
        print('注意：请输入表达式！ Note: Please enter expressions!')
        return None
    if assigns is None:
        print('注意：请输入参数及赋值！ Note: Please input parameters and assign values!')
        return None
    if the_var_x is None or the_var_y is None or start_end_x is None or start_end_y is None:
        print(
            '注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!')
        return None

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=left_margin, bottom=bottom_margin, right=right_margin, top=top_margin)
    plt.xticks(fontsize=fsize, fontname='times new roman')
    plt.yticks(fontsize=fsize, fontname='times new roman')

    ax.yaxis.set_rotate_label(False)
    ax.xaxis.set_rotate_label(False)
    ax.zaxis.set_rotate_label(False)

    # 设置 x 和 y 标签字体
    x_font = set_font(x_name)
    y_font = set_font(y_name)
    z_font = set_font(z_name)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize
    if zlabelsize == 'auto':
        zlabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad, fontname=y_font)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad, fontname=x_font)
    ax.set_zlabel(z_name, fontsize=zlabelsize, fontweight='bold', rotation=zrotation, labelpad=zlabelpad, fontname=z_font)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)
    ax.tick_params(axis='z', direction='in', pad=zpad)

    # Define the range for x and y
    x_ = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_ = np.linspace(start_end_y[0], start_end_y[1], precision)
    x, y = np.meshgrid(x_, y_)

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if len(x_) > density:
        rstride = int(len(x_) / density)
    else:
        rstride = 1

    if len(y_) > density:
        cstride = int(len(y_) / density)
    else:
        cstride = 1

    if exp_num == 1:
        the_exp = expressions[exp_names[0]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
        z = the_func(x, y)
        if isinstance(z, float):
            z = np.ones(x.shape, dtype=float) * z
        ax.plot_surface(x, y, z, color=colors[0], edgecolor=None, alpha=color_alpha)
        z_min = np.min(z)
        z_max = np.max(z)
    else:
        legend_elements = []
        his_zs = []

        get_order_func = lambda x_, y_: covert_orders(expressions=expressions, assigns=assigns,
                                              the_var1=the_var_x, the_var2=the_var_y,
                                              X=x_, Y=y_, reverse=False) # 越来越大
        Z_judge, _, map_order = get_order_func(x, y)  # value: relationship

        remove_values = []
        use_values = []
        dropout = 0.01
        for em in map_order.keys():
            count = np.count_nonzero(Z_judge == em)
            if count / (precision ** 2) <= dropout:
                remove_values.append(em)
            else:
                use_values.append(em)

        for em in remove_values:
            indices = np.where(Z_judge == em)
            rows, cols = indices
            for row, col in zip(rows, cols):
                if (col < precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, precision - col):
                        try_value = Z_judge[row, col + c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (col >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for c_add in range(1, col):
                        try_value = Z_judge[row, col - c_add]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row < precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, precision - row):
                        try_value = Z_judge[row + r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break
                if (row >= precision - 1) and (Z_judge[row, col] in remove_values):
                    for r_add in range(1, row):
                        try_value = Z_judge[row - r_add, col]
                        if try_value not in remove_values:
                            Z_judge[row, col] = try_value
                            break


        for j, em in enumerate(exp_names):
            the_exp = expressions[exp_names[j]]
            assigned_exp = the_exp.subs(assigns)
            the_func = lambdify((the_var_x, the_var_y), assigned_exp, 'numpy')
            z = the_func(x, y)
            if isinstance(z, float):
                z = np.ones(x.shape, dtype=float) * z

            legend_elements.append(Patch(facecolor=colors[j], edgecolor=edgecolor, alpha=color_alpha,
                                         label=em, linestyle=linestyles[j], linewidth = linewidth))
            his_zs.append(z)

            z_min_now = np.min(z)
            z_max_now = np.max(z)
            if j == 0:
                z_max = z_max_now
                z_min = z_min_now
            else:
                if z_max_now > z_max:
                    z_max = z_max_now
                if z_min_now < z_min:
                    z_min = z_min_now

        for key_ in use_values:
            value_ = map_order[key_]
            #print(key_, value_)
            # 画图区域
            mask = (Z_judge==key_)
            for the_order in value_:
                # 按顺序画
                the_z = copy.deepcopy(his_zs[the_order])
                the_z = the_z.astype(float)
                the_z[~mask] = np.nan

                ax.plot_surface(x, y, the_z, color=colors[the_order], alpha=color_alpha, edgecolor=edgecolor,
                                linestyle=ls_list[the_order], linewidth=linewidth, rstride=rstride, cstride=cstride)
                del the_z

    ax.view_init(elev=elevation, azim=azimuth, roll=roll)

    ax.set_zticks(np.linspace(z_min, z_max, 10))
    for label in ax.get_zticklabels():
        label.set_fontname('Times New Roman')
        label.set_fontsize(fsize)

    judge = abs(z_max - z_min)
    if judge < 0.0001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.5f'))
    elif judge < 0.001:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.4f'))
    elif judge < 0.01:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
    elif judge < 1:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    elif judge >= 1 and judge < 10:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    else:
        ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))

    if exp_num > 1:
        if legendsize == 'auto':
            legendsize = fsize
        ax.legend(handles=legend_elements, loc=locations[location], fontsize=legendsize, ncol=ncol)

    ax.grid(isgrid)

    if x_lim is None:
        ax.set_xlim(start_end_x[1], start_end_x[0])
    else:
        ax.set_xlim(x_lim[0], x_lim[1])

    if y_lim is None:
        ax.set_ylim(start_end_y[0], start_end_y[1])
    else:
        ax.set_ylim(y_lim[0], y_lim[1])

    if z_lim is not None:
        ax.set_zlim(z_lim[0], z_lim[1])

    # fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def who_max(expressions, assigns, the_var1, the_var2, X, Y):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    res_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var1, the_var2), assigned_exp, 'numpy')
        exp_value = the_func(X, Y)
        if isinstance(exp_value, float):
            exp_value = np.ones(X.shape, dtype=float)*exp_value
        res_list.append(exp_value)

    Z_list = []
    for ii in range(len(res_list[0])):
        tmp = []
        for jj in range(len(res_list[0][0])):
            _index = np.argmax([em[ii][jj] for em in res_list])
            tmp.append(_index)
        Z_list.append(tmp)

    return np.array(Z_list)


def who_max_point(expressions, assigns, the_var1, the_var2, _x, _y):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    Z_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        exp_value = assigned_exp.subs({the_var1: _x, the_var2: _y})
        Z_list.append(exp_value.evalf())
    Z_index = np.argmax(Z_list)
    return Z_index


def order_types(exp_names, values, reverse=True):
    return_val = ""
    # 获取排序后元素的索引 reverse=True默认降序
    sorted_indices = sorted(range(len(values)), key=lambda x: values[x], reverse=reverse)
    for _i, em in enumerate(sorted_indices):
        if reverse:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" > " + exp_names[em][1:-1]
                last_value = cur_value
        else:
            if _i == 0:
                last_value = values[em]
                return_val += r"$" + exp_names[em][1:-1]
            else:
                cur_value = values[em]
                if cur_value == last_value:
                    return_val += r" = " + exp_names[em][1:-1]
                else:
                    return_val += r" < " + exp_names[em][1:-1]
                last_value = cur_value
    return return_val + r"$", sorted_indices


def covert_orders(expressions, assigns, the_var1, the_var2, X, Y, reverse=True):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)
    map_dict = {}  # value: relationship
    map_order = {}  # value: order

    res_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        the_func = lambdify((the_var1, the_var2), assigned_exp, 'numpy')
        exp_value = the_func(X, Y)
        if isinstance(exp_value, float):
            exp_value = np.ones(X.shape, dtype=float) * exp_value
        res_list.append(exp_value)

    value_ldata = []
    index_point = 0
    for ii in range(len(res_list[0])):
        tmp = []
        for jj in range(len(res_list[0][0])):
            compare_list = [em[ii][jj] for em in res_list]
            latex_res, the_order = order_types(exp_names, compare_list, reverse=reverse)
            if latex_res not in map_dict.values():
                map_dict[index_point] = latex_res
                map_order[index_point] = the_order
                tmp.append(index_point)
                index_point += 1
            else:
                reversed_dict = {v: k for k, v in map_dict.items()}
                tmp.append(reversed_dict[latex_res])
        value_ldata.append(tmp)

    return np.array(value_ldata), map_dict, map_order  # value: relationship


def covert_orders_point(expressions, assigns, the_var1, the_var2, _x, _y, reverse=True):
    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    Z_list = []
    for i in range(exp_num):
        the_exp = expressions[exp_names[i]]
        assigned_exp = the_exp.subs(assigns)
        exp_value = assigned_exp.subs({the_var1: _x, the_var2: _y})
        Z_list.append(exp_value.evalf())
    latex_res, _ = order_types(exp_names, Z_list, reverse=reverse)
    return latex_res

def get_contour_centers(contourf_set):
    centers = []
    if 'collections' in dir(contourf_set):
        contourf_collections = contourf_set.collections
        for collection in contourf_collections:
            for path in collection.get_paths():
                # 获取路径的顶点
                vertices = path.vertices
                # 计算路径的质心
                centroid = np.mean(vertices, axis=0)
                centers.append(centroid)

    else:
        paths = contourf_set.allsegs
        for path in paths:
            vertices = list(path[0])
            centroid = np.mean(vertices, axis=0)
            centers.append(centroid)

    return centers


def draw_max_area(expressions=None,
                  assigns=None,
                  the_var_x=None,
                  start_end_x=None,
                  the_var_y=None,
                  start_end_y=None,
                  x_name='x',
                  y_name='y',
                  fsize=14,
                  texts=None,
                  text_fsize_add=0,
                  save_dir=None,
                  precision=1000,
                  figsize=[5, 4],
                  colors='sci',
                  patterns='sci',
                  xrotation=0,
                  yrotation=90,
                  linewidths=0.1,
                  xpad=3,
                  ypad=3,
                  xlabelpad=3,
                  ylabelpad=5,

                  xlabelsize='auto',
                  ylabelsize='auto',
                  pattern_colors = 'auto',
                  pattern_moves = 'auto'
                  ):
    """
        - expressions: Symbol表达式，字典形式传入。
        - assigns: 表达式参数赋值，字典形式。
        - the_var_x/the_var_y: 要分析的参数1/2；
        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
        - x_name: x轴名称标签，默认'x。
        - y_name: y轴名称标签，默认'y'。
        - fsize: 图片中字号的大小，默认值为14。
        - texts: 表达式expressions中的函数值若分别达到最大，则相应区域应分别标记的文本，以`[]`形式写。默认None，按照expressions提供的名字标记。注意：标签个数和expressions中的函数顺序要对应。
        - text_fsize_add: 区域标记文本字体大小相对于其他部分字体字号增加量，默认0，范围[-fsize+1, oo]。
        - save_dir=None: 图片保存路径，字符串。默认None，不保存。
        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
        - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[5, 4]`。
        - colors: 各区域的配色。一般sci论文要保证黑白打印出来能看清，因此，默认值为'sci'，表示符合学术论文美感的灰度配色方案。若``colors=None``，则表示全白色。
        - patterns: 为每个区域设置填充图案（例如斜线、网格等），以列表形式提供，例如['/', '\\', 'x', 'o']，默认[' ', '-', '|', '\\\\', '//', '+', 'x', 'o', '.', '*']。
          这样可以设置不同的密度，使用更多的斜线或交叉线条使得填充更密集：
            patterns = ['/', '//', '///', '\\', '\\\\', '\\\\\\', 'x', 'xx', 'xxx']
        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。
        - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。

    """

    if expressions is None:
        print('注意：请输入表达式！ Note: Please enter expressions!')
        return None
    if assigns is None:
        print('注意：请输入参数及赋值！ Note: Please input parameters and assign values!')
        return None
    if the_var_x is None or the_var_y is None or start_end_x is None or start_end_y is None:
        print('注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!')
        return None

    fig, ax = plt.subplots(figsize=figsize)

    # 设置 x 和 y 标签字体
    x_font = set_font(x_name)
    y_font = set_font(y_name)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad, fontname=y_font)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad, fontname=x_font)

    plt.xticks(fontsize=fsize, fontname='times new roman')
    plt.yticks(fontsize=fsize, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if exp_num <= 1:
        print('表达式个数必须大于2！ The number of expressions must be greater than 2!')
        return None

    x_points = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_points = np.linspace(start_end_y[0], start_end_y[1], precision)
    X, Y = np.meshgrid(x_points, y_points)

    Z_func = lambda x_, y_: who_max(expressions=expressions, assigns=assigns,
                                          the_var1=the_var_x, the_var2=the_var_y, X=x_, Y=y_)

    Z = Z_func(X,Y)
    contourf_set = ax.contourf(X, Y, Z, levels=exp_num, colors='w', alpha=1)  # 可能改
    ax.contour(X, Y, Z, levels=exp_num, colors='k', linewidths=linewidths)

    centers = get_contour_centers(contourf_set)

    # 打印结果
    record_centers = {}
    for center in centers:
        value = who_max_point(expressions, assigns, the_var_x, the_var_y, center[0], center[1])
        if value in record_centers.keys():
            new_center = [(record_centers[value][0] + center[0]) / 2, (record_centers[value][1] + center[1]) / 2]
            record_centers[value] = new_center
        else:
            record_centers[value] =center

    # 区域颜色列表：
    if colors == 'sci':
        colors = ['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#BEBEBE', '#B4B4B4', '#AAAAAA',
                 '#A0A0A0', '#969696', '#919191', '#8C8C8C', '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464']
    # 区域图案列表：
    if patterns == 'sci':
        patterns = [' ', '-', '|', '\\\\', '//', '+', 'x', 'o', '.', '*']

    # 确保颜色和图案的数量足够
    if len(colors) < exp_num:
        colors = colors * ((exp_num // len(colors)) + 1)
    if len(patterns) < exp_num:
        patterns = patterns * ((exp_num // len(patterns)) + 1)


    for i_, (k_, c_) in enumerate(record_centers.items()):
        print(f"区域 {k_}: 中心坐标 = {c_}")
        if texts is None:
            the_text = exp_names[int(k_)]
        else:
            the_text = texts[int(k_)]

        the_color = colors[i_]
        the_pattern = patterns[i_]

        # 在此处补充设置每个显示出来的区域的颜色，以此按照the_color提供的涂抹：
        # 在此处补充设置每个区域的hatch图案，按照the_pattern提供的绘制：
        ax.contourf(X, Y, Z, levels=[i_ - 0.5, i_ + 0.5], colors=[the_color], hatches=[the_pattern], alpha=1.0) #
        # 设置文本字体
        text_font = set_font(the_text)

        if pattern_colors != 'auto':
            if pattern_colors[i_] != 'auto':
                the_color = pattern_colors[i_]

        if pattern_moves != 'auto':

            ax.text(c_[0]+pattern_moves[i_][0], c_[1]+pattern_moves[i_][1], the_text, fontsize= fsize + text_fsize_add, ha='center', backgroundcolor=the_color, fontname=text_font)
        else:
            ax.text(c_[0], c_[1], the_text, fontsize= fsize + text_fsize_add, ha='center', backgroundcolor=the_color, fontname=text_font)

    ax.grid(False)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    judge_y = max(abs(np.max(y_points)),abs(np.min(y_points)))
    judge_x = max(abs(np.max(x_points)),abs(np.min(x_points)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0), useMathText=True)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def draw_detail_area(expressions=None,
                    assigns=None,
                    the_var_x=None,
                    start_end_x=None,
                    the_var_y=None,
                    start_end_y=None,
                    x_name='x',
                    y_name='y',
                    fsize=14,
                    text_fsize_add=0,
                    save_dir=None,
                    precision=1000,
                    figsize=[7, 4],
                    colors='sci',
                    patterns='sci',
                    xrotation=0,
                    yrotation=90,
                    linewidths=0.1,
                    xpad=3,
                    ypad=3,
                    xlabelpad=3,
                    ylabelpad=5,
                    prefix='Region',
                    numbers='roman',
                    reverse=True,
                    remove_eq=True,
                    dropout=0.01,

                    xlabelsize='auto',
                    ylabelsize = 'auto',
                    legendsize = 'auto',
                    pattern_colors = 'auto',
                    pattern_moves = 'auto'
                     ):
    """
        - expressions: Symbol表达式，字典形式传入。
        - assigns: 表达式参数赋值，字典形式。
        - the_var_x/the_var_y: 要分析的参数1/2；
        - start_end_x/start_end_y: 要分析的参数1/2的取值。[初始,结束]
        - x_name: x轴名称标签。
        - y_name: y轴名称标签。

        - fsize: 图片中字号的大小，默认值为14。
        - text_fsize_add: 区域标记文本字体大小相对于其他部分字体字号增加量，默认0，范围[-fsize+1, oo]。

        - save_dir=None: 图片保存路径，字符串。默认None，不保存。
        - precision: 绘画的精细程度。默认取1000，表示画 $1000 \times 1000$ 个点。该值越大，运行速度越慢，太大没必要，根据个人情况权衡。
        - figsize: 图片的大小，写成`[宽, 高]`的形式。默认为`[7, 4]`。

        - colors: 各区域的配色。一般sci论文要保证黑白打印出来能看清，因此，默认值为'sci'，表示符合学术论文美感的灰度配色方案。若``colors=None``，则表示全白色。
        - patterns: 为每个区域设置填充图案（例如斜线、网格等），以列表形式提供，例如['/', '\\', 'x', 'o']，默认[' ', '-', '|', '\\\\', '//', '+', 'x', 'o', '.', '*']。
          这样可以设置不同的密度，使用更多的斜线或交叉线条使得填充更密集：
            patterns = ['/', '//', '///', '\\', '\\\\', '\\\\\\', 'x', 'xx', 'xxx']

        - xrotation/yrotation: x/y轴名字标签旋转角度，基本不需要动。
        - linewidth: 线粗。字面意思，没啥好说的，默认值为1。
        - xpad=3, ypad=3, xlabelpad=3, ylabelpad=3: 分别为横轴刻度值距离横轴的距离、纵轴刻度值距离纵轴的距离、横轴名字标签距离横轴刻度的距离、纵轴名字标签距离纵轴刻度的距离。默认值3,3,3,3。如果挤了不好看了，再微调此参数，一般不用动。

        - prefix: 前缀。可以是"区域"也可以是"Region"，默认"Region"。
        - numbers: 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。默认"roman"。
        - reverse: 默认True，表示降序排布，即$A>B>C...$的形式。若为False，则升序排布$A<B<C...$。
        - remove_eq: 是否不考虑等式？默认True，不带等式。若为False，则带等式，如$A>B=C>D..$。
        - dropout: 点数占比小于多少不考虑？用于排除一些边界部分十分微小的区域。默认0.01。这个参数不要去动。
    """

    if expressions is None:
        print('注意：请输入表达式！ Note: Please enter expressions!')
        return None
    if assigns is None:
        print('注意：请输入参数及赋值！ Note: Please input parameters and assign values!')
        return None
    if the_var_x is None or the_var_y is None or start_end_x is None or start_end_y is None:
        print(
            '注意：请输入要分析的变量及范围！Note: Please enter the variable(s) to be analyzed and its (their) range(s)!')
        return None


    if colors == 'sci':
        colors = ['#ffffff', '#F0F0F0', '#E6E6E6', '#DCDCDC', '#D2D2D2', '#C8C8C8', '#C3C3C3', '#BEBEBE', '#B9B9B9',
                 '#B4B4B4', '#AFAFAF', '#AAAAAA', '#A5A5A5', '#A0A0A0', '#9B9B9B', '#969696', '#919191', '#8C8C8C',
                 '#878787', '#828282', '#7D7D7D', '#787878', '#6E6E6E', '#646464', '#646464', '#5F5F5F', '#5A5A5A',
                 '#5A5A5A', '#565656', '#525252', '#4E4E4E', '#4A4A4A', '#464646', '#424242', '#3E3E3E', '#3A3A64'] # 36

    if numbers == 'roman':
        # 列出前36个罗马数字
        numerals = gen_romans(36)
    elif numbers == 'letter':
        numerals = gen_letters(36)
    else:
        numerals = [str(i+1) for i in range(36)]

    fig, ax = plt.subplots(figsize=figsize)

    # 设置 x 和 y 标签字体
    x_font = set_font(x_name)
    y_font = set_font(y_name)

    if xlabelsize == 'auto':
        xlabelsize = fsize
    if ylabelsize == 'auto':
        ylabelsize = fsize

    ax.set_ylabel(y_name, fontsize=ylabelsize, fontweight='bold', rotation=yrotation, labelpad=ylabelpad, fontname=y_font)
    ax.set_xlabel(x_name, fontsize=xlabelsize, fontweight='bold', rotation=xrotation, labelpad=xlabelpad, fontname=x_font)

    plt.xticks(fontsize=fsize, fontname='times new roman')
    plt.yticks(fontsize=fsize, fontname='times new roman')

    exp_names = list(expressions.keys())
    exp_num = len(exp_names)

    if exp_num <= 1:
        print('表达式个数必须大于2！ The number of expressions must be greater than 2!')
        return None

    x_points = np.linspace(start_end_x[0], start_end_x[1], precision)
    y_points = np.linspace(start_end_y[0], start_end_y[1], precision)
    X, Y = np.meshgrid(x_points, y_points)

    Z_func = lambda x_, y_: covert_orders(expressions=expressions, assigns=assigns,
                                          the_var1=the_var_x, the_var2=the_var_y,
                                          X=x_, Y=y_, reverse=reverse)
    Z, map_dict, map_order = Z_func(X, Y)  # value: relationship

    remove_values = []
    if remove_eq:
        map_dict_new = {}
        for _i, value in enumerate(map_dict.values()):
            if '=' not in value:
                map_dict_new[list(map_dict.keys())[_i]] = value
            else:
                # 添加踢出列表
                remove_values.append(list(map_dict.keys())[_i])
    else:
        map_dict_new = map_dict

    final_map_dict = {}
    for em in map_dict_new.keys():
        count = np.count_nonzero(Z==em)
        if count/(precision**2) > dropout:
            final_map_dict[em] = map_dict_new[em]
        else:
            # 添加踢出列表
            remove_values.append(em)

    for em in remove_values:
        indices = np.where(Z==em)
        # 获取索引的行和列
        rows, cols = indices
        # 循环遍历索引，将值替换为附近的值
        for row, col in zip(rows, cols):
            # 找到附近的值，这里优先选择下边的值，若到头了，则选择上面的值。一点点看，直到那个值不在 `剔除列表中`,若选不着，就换个方向来。
            if (col < precision - 1) and (Z[row, col] in remove_values):
                for c_add in range(1, precision - col):
                    try_value = Z[row,col+c_add]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (col >= precision - 1) and (Z[row, col] in remove_values):
                for c_add in range(1, col):
                    try_value = Z[row,col-c_add]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (row < precision - 1) and (Z[row, col] in remove_values):
                for r_add in range(1, precision - row):
                    try_value = Z[row+r_add,col]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break
            if (row >= precision - 1) and (Z[row, col] in remove_values):
                for r_add in range(1, row):
                    try_value = Z[row-r_add,col]
                    if try_value not in remove_values:
                        Z[row, col] = try_value
                        break

    case_num = len(final_map_dict.keys())

    # 更新Z内的数据成连续数值
    for _jj, k in enumerate(final_map_dict.keys()):
        mask = (Z == k)
        Z[mask] = _jj


    contourf_set = ax.contourf(X, Y, Z, levels=case_num, colors='w', alpha=1)

    ax.contour(X, Y, Z, levels=case_num, colors='k', linewidths=linewidths)

    centers = get_contour_centers(contourf_set)

    # 打印结果
    record_centers = {}
    for center in centers:
        latex_value = covert_orders_point(expressions, assigns, the_var_x, the_var_y,
                                          center[0], center[1], reverse=reverse)
        if latex_value in record_centers.keys():
            new_center = [(record_centers[latex_value][0] + center[0]) / 2, (record_centers[latex_value][1] + center[1]) / 2]
            record_centers[latex_value] = new_center
        else:
            record_centers[latex_value] = center

    # 区域图案列表：
    if patterns == 'sci':
        patterns = [' ', '-', '|', '\\\\', '//', '+', 'x', 'o', '.', '*']

    # 确保颜色和图案的数量足够
    if len(colors) < case_num:
        colors = colors * ((case_num // len(colors)) + 1)
    if len(patterns) < case_num:
        patterns = patterns * ((case_num // len(patterns)) + 1)

    ii = 0
    legend_texts = ""
    for i_, (k_, c_) in enumerate(record_centers.items()):
        print(f"区域 {k_}: 中心坐标 = {c_}")
        the_text = prefix + r' $\rm{' + numerals[ii] + r'}$'
        if k_ == 0:
            legend_texts = prefix + r' $\rm{' + numerals[ii] + r'}$: ' + k_
        else:
            legend_texts += '\n' + prefix + r' $\rm{' + numerals[ii] + r'}$: ' + k_

        the_color = colors[i_]
        the_pattern = patterns[i_]

        # 在此处补充设置每个显示出来的区域的颜色，以此按照the_color提供的涂抹：
        # 在此处补充设置每个区域的hatch图案，按照the_pattern提供的绘制：
        ax.contourf(X, Y, Z, levels=[i_ - 0.5, i_ + 0.5], colors=[the_color], hatches=[the_pattern], alpha=1.0)
        # 设置文本字体
        text_font = set_font(the_text)

        if pattern_colors != 'auto':
            if pattern_colors[i_] != 'auto':
                the_color = pattern_colors[i_]

        if pattern_moves != 'auto':
            ax.text(c_[0]+pattern_moves[i_][0], c_[1]+pattern_moves[i_][1], the_text, fontsize=fsize + text_fsize_add, ha='center', backgroundcolor=the_color, fontname=text_font)
        else:
            ax.text(c_[0], c_[1], the_text, fontsize = fsize +text_fsize_add, ha='center', backgroundcolor=the_color, fontname=text_font)
        ii += 1

    legend_text_font = set_font(legend_texts)
    if legendsize == 'auto':
        legendsize = fsize
    plt.text(1.05, 0.5, legend_texts, fontsize=legendsize, ha='left', va='center', transform=plt.gca().transAxes, fontname=legend_text_font)

    ax.grid(False)

    # 设置刻度
    ax.tick_params(axis='x', direction='in', pad=xpad)
    ax.tick_params(axis='y', direction='in', pad=ypad)

    judge_y = max(abs(np.max(y_points)), abs(np.min(y_points)))
    judge_x = max(abs(np.max(x_points)), abs(np.min(x_points)))
    if judge_y >= 5000:
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useMathText=True)
    if judge_x >= 5000:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0), useMathText=True)

    fig.tight_layout()
    if save_dir is not None:
        if save_dir[-4:] == '.svg':
            plt.savefig(save_dir)
        else:
            plt.savefig(save_dir, dpi=600)
    return plt


def convert_pycode(str_exps, sym_name=True):
    # 将=...,之间的^替换成**
    pattern = r"(?<==).*?(?=\n|$)"
    new_str_exps = re.sub(pattern, lambda x: x.group(0).replace('^', '**'), str_exps)

    # 写成python代码形式
    # 按换行符分割表达式字符串为列表
    expressions_list = new_str_exps.split('\n')
    expressions_list = [expr.strip() for expr in expressions_list if expr.strip()]

    # 用于存储所有出现的变量（去重）
    all_variables = set()

    # 遍历每个表达式字符串
    for expression_str in expressions_list:
        # 提取等号左边的部分（去除两端空白字符）
        #left_side = re.search(r"^.*?(?==)", expression_str).group(0).strip()
        # 提取等号右边的部分（去除两端空白字符）
        right_side = re.search(r"(?<==).*?(?=\n|$)", expression_str).group(0).strip()
        # 使用正则表达式找出等号右边表达式中所有符合变量命名规则的内容（纯数字不算，前面有#的不算）
        variables_in_expression = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", right_side)
        all_variables.update(variables_in_expression)

    # 按照要求的格式生成最终字符串
    code_str = f"""from easyfig import *\n\n"""

    if sym_name:
        var_list = list(all_variables)
        for em in var_list:
            if em in sympy_names:
                all_variables.remove(em)

    # 将变量集合转换为以逗号分隔的字符串，用于symbols函数和后续格式化
    if len(all_variables)>=1:
        variables_str = ", ".join(sorted(all_variables))
        code_str += f"""# 定义符号\n{variables_str} = symbols('{variables_str}')\n\n# 表达式\nexpressions = {{\n"""
    else:
        variables_str = ''
        code_str += f"""# 表达式\nexpressions = {{\n"""

    for expression_str in expressions_list:
        left_side = re.search(r"^.*?(?==)", expression_str).group(0).strip()
        right_side = re.search(r"(?<==).*$", expression_str).group(0).strip()
        code_str += f"\tr'${left_side}$': {right_side},\n"
    code_str += "}"

    try:
        ast.parse(code_str)
        print("语法正确")
        return code_str, variables_str
    except SyntaxError as e:
        print(f"语法错误: {e}\n\n{code_str}")
        return None, f"语法错误: {e}\n\n{code_str}"


def makefig():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from tkinter.scrolledtext import ScrolledText
    #from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # 初始化主窗口
    root = tk.Tk()
    root.title("EasyFig仿真绘图向导 - 作者：东北大学 田雨鑫 - 让天下没有难用的工具！")
    root.state('zoomed')  # 最大化

    # 设置全局字体
    default_font = ("Times New Roman", 16)

    # 创建样式对象
    style = ttk.Style(root)

    # 设置标签页字体大小
    style.theme_use('clam')  # 使用 'clam' 主题以支持背景色修改
    style.configure("Custom.TButton",
                    font=("宋体", 15),
                    #foreground="black",
                    background="#cceeff")
    style.configure('TNotebook.Tab', font=('宋体', 16))

    # 创建Notebook（标签页）
    notebook = ttk.Notebook(root, style='TNotebook')
    notebook.pack(expand=True, fill='both')

    # 创建四个标签页
    tabs = []
    for i in range(1, 5):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=f"Tab {i}")  # 临时名称，后面会替换
        tabs.append(tab)

    # 设置Tab名称
    notebook.tab(0, text="绘制仿真折线图")
    notebook.tab(1, text="绘制模式比较图")
    notebook.tab(2, text="绘制关系区域图")
    notebook.tab(3, text="绘制仿真三维图")

    # 定义一个函数来创建每个Tab的内容，减少重复代码
    def create_tab(tab, tab_type):
        # 左右分割，比例8:2
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=3, pady=3)

        # 左半部分，上中下分割，比例2:3:1
        main_frame.grid_rowconfigure(0, weight=2)
        main_frame.grid_rowconfigure(1, weight=3)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        _top = ttk.Frame(main_frame)
        _middle = ttk.Frame(main_frame)
        _bottom = ttk.Frame(main_frame)
        _top.pack(side='top', fill='both', expand=True, pady=(0, 5))
        _middle.pack(fill='both', expand=True, pady=5)
        _bottom.pack(side='bottom', fill='both', expand=True, pady=(5, 0))

        # 1.1 上部分
        lbl_exp = ttk.Label(_top, text="表达式输入：", font=default_font)
        lbl_exp.pack(anchor='w')
        exp_input = ScrolledText(_top, font=("Times New Roman", 16), wrap='word', height=9)
        exp_input.pack(fill='both', expand=True)
        exp_input.insert('1.0', "请按照“表达式名称（支持LaTex写法）=表达式”的格式书写，一行是一个表达式。\n填写完表达式后，点击“公式识别”，即检查公式并可提取符号参数，供分析参数的选择和其他参数的赋值。\n如果第一次用，请点击“加载案例”，在已有例子的基础上改写，更方便快捷。" + \
                                "\n支持数学常数和函数，例如：E, pi, exp(x), log(x), sqrt(x), Abs(x), sin(x), cos(x), root(x,n), Rational(a,b)等，详情见：\nhttps://docs.sympy.org/latest/modules/functions/elementary.html#")

        # 1.2 中部分
        if tab_type == "绘制仿真三维图":
            num_middle_rows = 9
        else:
            num_middle_rows = 8

        middle_rows = []
        for _ in range(num_middle_rows):
            frame = ttk.Frame(_middle)
            frame.pack(fill='x', pady=2)
            middle_rows.append(frame)

        # 第1行：“公式识别”按钮
        btn_convert = ttk.Button(middle_rows[0], text="公式识别", command=lambda: on_convert(), width=27, style="Custom.TButton")
        btn_convert.pack(side='left')
        btn_clear = ttk.Button(middle_rows[0], text="清空", command=lambda: on_clear(), width=10,
                                 style="Custom.TButton")
        btn_clear.pack(padx=2)

        # 第2行：分析参数选择（x轴参数 + y轴参数）
        if tab_type == "绘制仿真折线图":
            lbl_param = ttk.Label(middle_rows[1], text="分析参数选择：", font=default_font)
            lbl_param.pack(side='left')
            lbl_x = ttk.Label(middle_rows[1], text="x轴参数", font=default_font)
            lbl_x.pack(side='left', padx=(10, 0))
            x_list = ttk.Combobox(middle_rows[1], state='readonly', font=default_font)
            x_list.pack(side='left', padx=(5, 10))
            y_list = None
            x_list.bind("<<ComboboxSelected>>", lambda event: update_var_list())

            # 第3行
            lbl_x_range = ttk.Label(middle_rows[2], text="x轴变化范围：", font=default_font)
            lbl_x_range.pack(side='left')
            lbl_x_start = ttk.Label(middle_rows[2], text="起始值", font=default_font)
            lbl_x_start.pack(side='left', padx=(10, 0))
            x_start = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            x_start.pack(side='left', padx=(5, 10))
            lbl_x_end = ttk.Label(middle_rows[2], text="终止值", font=default_font)
            lbl_x_end.pack(side='left')
            x_end = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            x_end.pack(side='left', padx=(5, 10))
            lbl_x_interval = ttk.Label(middle_rows[2], text="间隔", font=default_font)
            lbl_x_interval.pack(side='left')
            x_interval = ttk.Entry(middle_rows[2], font=default_font, width=7, validate="key")
            x_interval.pack(side='left', padx=(5, 10))

            y_start = None
            y_end = None

        else:
            lbl_param = ttk.Label(middle_rows[1], text="分析参数选择：", font=default_font)
            lbl_param.pack(side='left')
            lbl_x = ttk.Label(middle_rows[1], text="x轴参数", font=default_font)
            lbl_x.pack(side='left', padx=(10, 0))
            x_list = ttk.Combobox(middle_rows[1], state='readonly', font=default_font)
            x_list.pack(side='left', padx=(5, 10))
            lbl_y = ttk.Label(middle_rows[1], text="y轴参数", font=default_font)
            lbl_y.pack(side='left', padx=(10, 0))
            y_list = ttk.Combobox(middle_rows[1], state='readonly', font=default_font)
            y_list.pack(side='left', padx=(5, 0))
            x_list.bind("<<ComboboxSelected>>", lambda event: update_var_list())
            # y_list 选择后验证
            y_list.bind("<<ComboboxSelected>>", lambda event: validate_y_selection(x_list, y_list))

            # 第3行：x轴和y轴变化范围
            lbl_x_range = ttk.Label(middle_rows[2], text="x轴变化范围：", font=default_font)
            lbl_x_range.pack(side='left')
            lbl_x_start = ttk.Label(middle_rows[2], text="起始值", font=default_font)
            lbl_x_start.pack(side='left', padx=(10, 0))
            x_start = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            x_start.pack(side='left', padx=(5, 10))
            lbl_x_end = ttk.Label(middle_rows[2], text="终止值", font=default_font)
            lbl_x_end.pack(side='left')
            x_end = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            x_end.pack(side='left', padx=(5, 10))

            lbl_y_range = ttk.Label(middle_rows[2], text="y轴变化范围：", font=default_font)
            lbl_y_range.pack(side='left', padx=(10, 0))
            lbl_y_start = ttk.Label(middle_rows[2], text="起始值", font=default_font)
            lbl_y_start.pack(side='left', padx=(10, 0))
            y_start = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            y_start.pack(side='left', padx=(5, 10))
            lbl_y_end = ttk.Label(middle_rows[2], text="终止值", font=default_font)
            lbl_y_end.pack(side='left')
            y_end = ttk.Entry(middle_rows[2], font=default_font, width=10, validate="key")
            y_end.pack(side='left', padx=(5, 0))

            x_interval = None

        # 第4行：其他参数赋值
        lbl_assign = ttk.Label(middle_rows[3], text="其他参数赋值：", font=default_font, )
        lbl_assign.pack(anchor='w')
        # 第5行：Assigns_input
        assigns_input = ScrolledText(middle_rows[4], font=("Times New Roman", 14), wrap='word', height=2)
        assigns_input.pack(fill='both', expand=True)

        # 根据tab_type调整中间部分的布局
        if tab_type == "绘制仿真三维图":
            # 中间部分包含 9 行

            # 第6行：x轴名称、y轴名称、z轴名称
            lbl_x_name = ttk.Label(middle_rows[5], text="x轴名称", font=default_font)
            lbl_x_name.pack(side='left')
            x_name = ttk.Entry(middle_rows[5], font=default_font, width=30)
            x_name.pack(side='left', padx=(5, 10))
            lbl_y_name = ttk.Label(middle_rows[5], text="y轴名称", font=default_font)
            lbl_y_name.pack(side='left')
            y_name = ttk.Entry(middle_rows[5], font=default_font, width=30)
            y_name.pack(side='left', padx=(5, 10))
            lbl_z_name = ttk.Label(middle_rows[5], text="z轴名称", font=default_font)
            lbl_z_name.pack(side='left')
            z_name = ttk.Entry(middle_rows[5], font=default_font, width=30)
            z_name.pack(side='left', padx=(5, 0))
        else:
            lbl_x_name = ttk.Label(middle_rows[5], text="x轴名称", font=default_font)
            lbl_x_name.pack(side='left')
            x_name = ttk.Entry(middle_rows[5], font=default_font, width=50)
            x_name.pack(side='left', padx=(5, 10))
            lbl_y_name = ttk.Label(middle_rows[5], text="y轴名称", font=default_font)
            lbl_y_name.pack(side='left')
            y_name = ttk.Entry(middle_rows[5], font=default_font, width=50)
            y_name.pack(side='left', padx=(5, 0))
            z_name = None


        # 根据tab_type调整中间部分的布局
        if tab_type in ["绘制仿真三维图","绘制仿真折线图"]:
            # 第7行：图例设置
            lbl_legend = ttk.Label(middle_rows[6], text="图例设置：", font=default_font)
            lbl_legend.pack(side='left')
            lbl_location = ttk.Label(middle_rows[6], text="位置", font=default_font)
            lbl_location.pack(side='left', padx=(10, 0))
            location = ttk.Combobox(middle_rows[6], state='readonly',
                                    values=['best', 'northeast', 'northwest', 'southwest', 'southeast', 'east', 'west',
                                            'south', 'north', 'center'], font=default_font)
            location.current(0)
            location.pack(side='left', padx=(5, 10))
            lbl_ncol = ttk.Label(middle_rows[6], text="列数", font=default_font)
            lbl_ncol.pack(side='left')
            ncol = tk.Spinbox(middle_rows[6], from_=1, to=100, font=default_font, width=5)
            ncol.delete(0, 'end')
            ncol.insert(0, "1")
            ncol.pack(side='left', padx=(5, 0))
            the_marker = None
            marker_way = None
            the_pref = None

        elif tab_type == "绘制模式比较图":
            # 第7行：标签“标注设置：”+单行输入框texts，充满其余空间；
            lbl_marker = ttk.Label(middle_rows[6], text="标注设置：", font=default_font)
            lbl_marker.pack(side='left')
            the_marker = ttk.Entry(middle_rows[6], font=default_font, width=65)
            the_marker.pack(side='left', padx=(5, 0))

            location = None
            ncol = None
            the_pref = None
            marker_way = None

        else:
            # 绘制关系区域图
            # 第7行：左右排布：标签“标注设置：”+标签“前缀”+单行输入框 pref，默认"Region"+标签“标记方式”+下拉列表numbers，选项有"罗马数字", "字母" 和"阿拉伯数字"，默认"罗马数字"；
            lbl_marker = ttk.Label(middle_rows[6], text="标注设置：", font=default_font)
            lbl_marker.pack(side='left')
            lbl_pref = ttk.Label(middle_rows[6], text="前缀", font=default_font)
            lbl_pref.pack(side='left', padx=(10, 0))
            the_pref = ttk.Entry(middle_rows[6], font=default_font, width=25)
            the_pref.delete(0, 'end')
            the_pref.insert(0, "Region")
            the_pref.pack(side='left', padx=(5, 0))
            lbl_way = ttk.Label(middle_rows[6], text="标记方式", font=default_font)
            lbl_way.pack(side='left')

            marker_way = ttk.Combobox(middle_rows[6], state='readonly', values=["roman", "letter", "number"], font=default_font)
            marker_way.current(0)
            marker_way.pack(side='left', padx=(5, 10))

            lbl_tip = ttk.Label(middle_rows[6], text=" (提示：roman=罗马数字；letter=字母；number=阿拉伯数字)", font=default_font)
            lbl_tip.pack(side='left')

            location = None
            ncol = None
            the_marker = None


        if tab_type == "绘制仿真三维图":
            # 第8行：视图设置
            lbl_view = ttk.Label(middle_rows[7], text="视图设置：", font=default_font)
            lbl_view.pack(side='left')
            lbl_elevation = ttk.Label(middle_rows[7], text="仰角", font=default_font)
            lbl_elevation.pack(side='left', padx=(10, 0))
            elevation = tk.Spinbox(middle_rows[7], from_=-360, to=360, font=default_font, width=5)
            elevation.delete(0, 'end')
            elevation.insert(0, "15")
            elevation.pack(side='left', padx=(5, 10))
            lbl_azimuth = ttk.Label(middle_rows[7], text="方位角", font=default_font)
            lbl_azimuth.pack(side='left')
            azimuth = tk.Spinbox(middle_rows[7], from_=-360, to=360, font=default_font, width=5)
            azimuth.delete(0, 'end')
            azimuth.insert(0, "45")
            azimuth.pack(side='left', padx=(5, 0))

            # 第9行：其他设置
            lbl_other = ttk.Label(middle_rows[8], text="其他设置：", font=default_font)
            lbl_other.pack(side='left')
            lbl_fsize = ttk.Label(middle_rows[8], text="字号", font=default_font)
            lbl_fsize.pack(side='left', padx=(10, 0))
            fsize = tk.Spinbox(middle_rows[8], from_=1, to=100, font=default_font, width=5)
            fsize.delete(0, 'end')
            fsize.insert(0, "14")
            fsize.pack(side='left', padx=(5, 10))
            lbl_fig_w = ttk.Label(middle_rows[8], text="图片宽", font=default_font)
            lbl_fig_w.pack(side='left')
            figsizeW = tk.Spinbox(middle_rows[8], from_=1, to=100, font=default_font, width=5)
            figsizeW.delete(0, 'end')
            figsizeW.insert(0, "7")
            figsizeW.pack(side='left', padx=(5, 10))
            lbl_fig_h = ttk.Label(middle_rows[8], text="图片高", font=default_font)
            lbl_fig_h.pack(side='left')
            figsizeH = tk.Spinbox(middle_rows[8], from_=1, to=100, font=default_font, width=5)
            figsizeH.delete(0, 'end')
            figsizeH.insert(0, "5")
            figsizeH.pack(side='left', padx=(5, 10))
            lbl_x_rot = ttk.Label(middle_rows[8], text="x轴标旋转", font=default_font)
            lbl_x_rot.pack(side='left')
            xrotation = tk.Spinbox(middle_rows[8], from_=0, to=360, font=default_font, width=5)
            xrotation.delete(0, 'end')
            xrotation.insert(0, "0")
            xrotation.pack(side='left', padx=(5, 10))
            lbl_y_rot = ttk.Label(middle_rows[8], text="y轴标旋转", font=default_font)
            lbl_y_rot.pack(side='left')
            yrotation = tk.Spinbox(middle_rows[8], from_=0, to=360, font=default_font, width=5)
            yrotation.delete(0, 'end')
            yrotation.insert(0, "0")
            yrotation.pack(side='left', padx=(5, 0))
            lbl_z_rot = ttk.Label(middle_rows[8], text="z轴标旋转", font=default_font)
            lbl_z_rot.pack(side='left')
            zrotation = tk.Spinbox(middle_rows[8], from_=0, to=360, font=default_font, width=5)
            zrotation.delete(0, 'end')
            zrotation.insert(0, "90")
            zrotation.pack(side='left', padx=(5, 0))
        else:
            # 中间部分包含 8 行
            # 第8行：其他设置
            lbl_other = ttk.Label(middle_rows[7], text="其他设置：", font=default_font)
            lbl_other.pack(side='left')
            lbl_fsize = ttk.Label(middle_rows[7], text="字号", font=default_font)
            lbl_fsize.pack(side='left', padx=(10, 0))
            fsize = tk.Spinbox(middle_rows[7], from_=1, to=100, font=default_font, width=5)
            fsize.delete(0, 'end')
            fsize.insert(0, "14")
            fsize.pack(side='left', padx=(5, 10))
            lbl_fig_w = ttk.Label(middle_rows[7], text="图片宽", font=default_font)
            lbl_fig_w.pack(side='left')
            figsizeW = tk.Spinbox(middle_rows[7], from_=1, to=100, font=default_font, width=5)
            figsizeW.delete(0, 'end')
            if tab_type == "绘制关系区域图":
                figsizeW.insert(0, "7")
            else:
                figsizeW.insert(0, "5")
            figsizeW.pack(side='left', padx=(5, 10))
            lbl_fig_h = ttk.Label(middle_rows[7], text="图片高", font=default_font)
            lbl_fig_h.pack(side='left')
            figsizeH = tk.Spinbox(middle_rows[7], from_=1, to=100, font=default_font, width=5)
            figsizeH.delete(0, 'end')
            figsizeH.insert(0, "4")
            figsizeH.pack(side='left', padx=(5, 10))
            lbl_x_rot = ttk.Label(middle_rows[7], text="x轴标旋转", font=default_font)
            lbl_x_rot.pack(side='left')
            xrotation = tk.Spinbox(middle_rows[7], from_=0, to=360, font=default_font, width=5)
            xrotation.delete(0, 'end')
            xrotation.insert(0, "0")
            xrotation.pack(side='left', padx=(5, 10))
            lbl_y_rot = ttk.Label(middle_rows[7], text="y轴标旋转", font=default_font)
            lbl_y_rot.pack(side='left')
            yrotation = tk.Spinbox(middle_rows[7], from_=0, to=360, font=default_font, width=5)
            yrotation.delete(0, 'end')
            yrotation.insert(0, "90")
            yrotation.pack(side='left', padx=(5, 0))
            zrotation = None


        # 1.3 下部分：运行信息
        left_frame = ttk.Frame(_bottom)
        right_frame = ttk.Frame(_bottom)
        left_frame.pack(side='left', fill='both', expand=True, padx=3, pady=3)
        right_frame.pack(side='right', fill='both', expand=True, padx=3, pady=3)

        lbl_log = ttk.Label(left_frame, text="运行信息：", font=default_font)
        lbl_log.pack(anchor='w')
        print_log = ScrolledText(left_frame, font=("Times New Roman", 15), wrap='word', state='disabled')
        print_log.pack(fill='both', expand=True)
        print_log.configure(state='normal')
        print_log.insert('1.0', "欢迎使用EasyFig向导！")
        print_log.configure(state='disabled')

        # 2.2 下部分：按钮
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(expand=True)
        btn_draw_image = ttk.Button(btn_frame, text="出图...", command=lambda: draw_image(), width=20, style="Custom.TButton")
        btn_draw_image.pack(pady=2, fill='both')
        btn_save_code = ttk.Button(btn_frame, text="保存...", command=lambda: save_code(), width=20, style="Custom.TButton")
        btn_save_code.pack(pady=2, fill='both')
        btn_import_code = ttk.Button(btn_frame, text="打开...", command=lambda: import_code(), width=20, style="Custom.TButton")
        btn_import_code.pack(pady=2, fill='both')
        btn_import_case = ttk.Button(btn_frame, text="加载案例", command=lambda: import_case(), width=20,style="Custom.TButton")
        btn_import_case.pack(pady=2, fill='both')

        # 存储控件以便后续使用
        tab.controls = {
            'Exp_input': exp_input,
            'convert_button': btn_convert,
            'x_list': x_list,
            'y_list': y_list,
            'x_start': x_start,
            'x_end': x_end,
            'x_interval': x_interval,
            'y_start': y_start,
            'y_end': y_end,
            'Assigns_input': assigns_input,
            'x_name': x_name,
            'y_name': y_name,
            'z_name': z_name,
            'location': location,
            'ncol': ncol,
            'the_marker': the_marker,
            'marker_way': marker_way,
            'the_pref': the_pref,
            'fsize': fsize,
            'figsizeW': figsizeW,
            'figsizeH': figsizeH,
            'xrotation': xrotation,
            'yrotation': yrotation,
            'zrotation': zrotation,
            'print_log': print_log,
            #'play_main': play_main,
            'buttons': {
                'import_case': btn_import_case,
                'import_code': btn_import_code,
                'draw_image': btn_draw_image,
                'save_code': btn_save_code,
            },
            #'fig': fig,
            #'tab_type': tab_type,
            'elevation': elevation if tab_type == "绘制仿真三维图" else None,
            'azimuth': azimuth if tab_type == "绘制仿真三维图" else None,
        }

    # 创建所有标签页
    create_tab(tabs[0], "绘制仿真折线图")
    create_tab(tabs[1], "绘制模式比较图")
    create_tab(tabs[2], "绘制关系区域图")
    create_tab(tabs[3], "绘制仿真三维图")

    # 定义按钮回调函数（需要根据实际功能完善）
    def on_convert():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        exp_text = tab.controls['Exp_input'].get("1.0", tk.END)
        code_str, variables_str = convert_pycode(exp_text)
        if code_str:
            # 更新x_list和y_list
            variables = variables_str.split(", ")
            tab.controls['x_list']['values'] = variables
            if tab.controls['y_list']:
                tab.controls['y_list']['values'] = variables
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, "公式识别成功！")
            tab.controls['print_log'].configure(state='disabled')
        else:
            # 识别失败，显示错误信息
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, variables_str)
            tab.controls['print_log'].configure(state='disabled')

    def validate_y_selection(x_list, y_list):
        x_val = x_list.get()
        y_val = y_list.get()
        if x_val == y_val:
            messagebox.showerror("选择错误", "y轴和x轴参数名应不同，请重新选择")
            y_list.set('')
        else:
            update_var_list()

    def update_var_list():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        exp_text = tab.controls['Exp_input'].get("1.0", tk.END)
        code_str, variables_str = convert_pycode(exp_text)
        variables = variables_str.split(", ")

        # 更新Assigns_input
        selected_x = tab.controls['x_list'].get()
        selected_y = tab.controls['y_list'].get() if tab.controls['y_list'] else None
        assigns = ""
        for var in variables:
            if var != selected_x and var != selected_y:
                assigns += f"{var} = 0.0, "
        tab.controls['Assigns_input'].delete("1.0", tk.END)
        tab.controls['Assigns_input'].insert(tk.END, assigns.rstrip(", "))

    def on_clear():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        tab.controls['Exp_input'].delete("1.0", tk.END)

    def import_case():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        tab_name = notebook.tab(current_tab, "text")

        if tab_name == '绘制仿真折线图':
            content = r"""
from easyfig import *

# 定义符号
E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e = symbols('E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e')

# 表达式
expressions = {
	r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2),
	r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2),
	r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
	r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1, alpha: 0.9}

# 要分析的参数，及其取值范围
the_var = b
ranges = [0, 0.08, 0.01]

# xy轴的名字
x_name = r'$\alpha$ with blockchain'
y_name = r'$b$'

# 图片保存路径、文件名
save_dir = None

# 图例的方位
location = 'best'
# 图例的列数
ncol = 1

# 图片中字号的大小
fsize = 15
# 图片的大小
figsize = [6, 5]

xt_rotation = 0 # 横轴刻度标签旋转角度。
# x/y轴名字标签旋转角度。
xrotation = 0
yrotation = 0

# 线的风格，实线'-'，点横线'-.'，虚线'--'，点线':'等。
linestyles = ['-','-.','--', ':', (0, (1, 10)), (0, (5, 10)), (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]
linewidth = 1.0 # 线粗。
# 线上的标记符号,关于标记符号的详细说明 https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
markers = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']
markersize = 3.5 # 标记符号的大小，默认3.5。
# 线的颜色
colors = ['black', 'blue', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo', 'chocolate', 'navy', 'purple']
isgrid = False
# 分别为x/y轴刻度值距离横轴的距离。
xpad = 3
ypad = 3
# 分别为x/y轴名字标签距离纵轴刻度的距离。
xlabelpad = 7
ylabelpad = 7

# 坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小
legendsize = 'auto' # 图例字大小

# 传给draw_lines函数
the_plt = draw_lines(expressions=expressions, assigns=assigns, the_var=the_var, ranges=ranges, x_name=x_name, y_name=y_name, 
    save_dir=save_dir, location=location, ncol=ncol, fsize=fsize, figsize=figsize, xt_rotation=xt_rotation,
    xrotation=xrotation, yrotation=yrotation, linestyles=linestyles, linewidth=linewidth, markers=markers,
    markersize=markersize, colors=colors, isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad,
    xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize)
the_plt.show()
"""
        elif tab_name == '绘制模式比较图':
            content = r"""
from easyfig import *

# 定义符号
E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e = symbols('E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e')

# 表达式
expressions = {
	r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2),
	r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2),
	r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
	r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1}

# 要分析的参数，及其取值范围
the_var_x = alpha
start_end_x = [0.7, 0.8]  # [起始值, 终止值]。 
the_var_y = b
start_end_y = [0, 0.08]  # [起始值, 终止值]。 

# xy轴的名字
x_name = r'$\alpha$ with blockchain' 
y_name = r'$b$'  

# 图片保存路径、文件名
save_dir = None 

# 四个表达式分别达到最大时显示的标签、区域背景颜色和区域图案。
texts = [r'NW', r'BW', r'NS', r'BS'] 
colors = 'sci'
patterns = 'sci'

# 其他设置
fsize = 14
text_fsize_add = 2 # 区域标签字号增量。
# 图片大小。
figsize = [5, 4] 
# x轴标签名旋转角度（0为不旋转）。
xrotation = 0        
# y轴标签名旋转角度（0为不旋转）。 
yrotation = 90    
linewidths = 0.1 # 线粗

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 3

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = 'auto'
pattern_moves = [(0, 0), (0, 0), (0, 0), (0, 0)]  # 区域标签较原来的偏移量，(x方向，y方向)

# 传给draw_max_area函数
the_plt = draw_max_area(expressions=expressions, assigns=assigns, 
              the_var_x=the_var_x, start_end_x=start_end_x, 
              the_var_y=the_var_y, start_end_y=start_end_y, 
              x_name=x_name, y_name=y_name, 
              fsize=fsize, texts=texts, text_fsize_add=text_fsize_add,
              save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
              xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
             xlabelsize=xlabelsize, ylabelsize=ylabelsize, pattern_colors=pattern_colors, 
              pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
the_plt.show()       
"""
        elif tab_name == '绘制关系区域图':
            content = r"""
from easyfig import *

# 定义符号
E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e = symbols('E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e')

# 表达式
expressions = {
	r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2),
	r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2),
	r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
	r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
assigns = {c_n:  0.2, c_r:  0.1, delta:  0.8, e_n:  1, e_r:  0.6, p_e:  0.1, E:  2, k:  1.1}

# 要分析的参数，及其取值范围
the_var_x = alpha
start_end_x = [0.7, 0.8] 
the_var_y = b
start_end_y = [0, 0.08] 

# xy轴的名字
x_name = r'$\alpha$ with blockchain' 
y_name = r'$b$'  

# 图片保存路径、文件名
save_dir = None 

# 每个关系区域的标签前缀、编号样式、背景颜色和图案。
# 前缀。可以是"区域"也可以是"Region"，默认"Region"。
prefix = 'Region'
# 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。
numbers = 'letter' 
colors = 'sci'
patterns = 'sci'

# 其他设置
fsize = 14
text_fsize_add = -2 # 区域标签字号增量。 Increment of regional label font size.
# 图片大小。
figsize = [7, 4] 
# x轴标签名旋转角度（0为不旋转）。
xrotation = 0              
# y轴标签名旋转角度（0为不旋转）。 
yrotation = 90       
linewidths = 0.1 # 线粗

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 3

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 'auto' # 图例字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = 'auto'  # 设置标签背景色，'auto'为自动，'none'为透明
pattern_moves = [(0, 0), (0, 0), (0, 0), (0, 0)]  # 设定区域标签较原来的偏移量，(x方向，y方向)   

# 传给draw_detail_area函数
the_plt = draw_detail_area(expressions=expressions, assigns=assigns, 
        the_var_x=the_var_x, start_end_x=start_end_x, 
        the_var_y=the_var_y, start_end_y=start_end_y, 
        x_name=x_name, y_name=y_name, 
        fsize=fsize, text_fsize_add=text_fsize_add,
        save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
        xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
        prefix=prefix, numbers=numbers, xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize, 
      pattern_colors=pattern_colors, pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
the_plt.show()
"""
        else:
            content = r"""
from easyfig import *

# 定义符号
E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e = symbols('E, alpha, b, c_n, c_r, delta, e_n, e_r, k, p_e')

# 表达式
expressions = {
	r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2),
	r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2),
	r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
	r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
assigns = {c_n:  0.2, c_r:  0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1}

# 要分析的参数，及其取值范围
the_var_x = alpha
start_end_x = [0.7, 0.8] 
the_var_y = b
start_end_y = [0, 0.08] 

# xy轴的名字
x_name = r'$\alpha$' 
y_name = r'$b$'  
z_name = r'$\pi_r$'

# 图片保存路径、文件名
save_dir = None 

# 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。
color_alpha = 0.8 
# 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。
location = 'best' 
# 图例的列数，默认为1列，即竖着排布。
ncol = 4
# 图片中字号的大小
fsize = 14
# 图片的大小，写成`[宽, 高]`的形式。默认为`[7, 5]`。
figsize = [7, 5]
# xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。
xrotation = 0
yrotation = 0
# Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴
zrotation = 90
# 是否要网格。要就填True，不要就是False
isgrid = True

# 在多面图中用于按顺序制定每个面的颜色（包含标记符号的颜色）。
colors = ['yellow','blue','red','green', 'darkgoldenrod', 'darkcyan', 'indigo', 'chocolate', 'navy', 'purple']
# 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。
edgecolor = 'black'
linestyles = ['-','-.','--', ':', (0, (1, 10)), (0, (5, 10)), (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]
linewidth = 0.5 # 线粗。
density = 50 # 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。

# 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。
elevation = 15
# 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。
azimuth = 45

# 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。
left_margin = 0
bottom_margin = 0
right_margin = 1
top_margin = 1

# 分别为/y/z轴刻度值距离横轴的距离。
xpad = 3
ypad = 3
zpad = 3

# 分别为/y/z轴名字标签距离纵轴刻度的距离。
xlabelpad = 7
ylabelpad = 7
zlabelpad = 7

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
zlabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 'auto' # 图例字大小，默认'auto'，自动和fsize一样大

# 传给draw_3D函数 (不要改！)
# Passed to the draw_3D function (Don't change!).
the_plt = draw_3D(expressions=expressions, assigns=assigns, the_var_x=the_var_x, start_end_x=start_end_x, the_var_y=the_var_y, 
        start_end_y=start_end_y, x_name=x_name, y_name=y_name, z_name=z_name, 
        save_dir=save_dir, color_alpha=color_alpha, location=location, ncol=ncol, fsize=fsize, figsize=figsize, 
        xrotation=xrotation, yrotation=yrotation, zrotation=zrotation, isgrid=isgrid, colors=colors, 
        edgecolor=edgecolor, linestyles=linestyles, linewidth=linewidth, density=density, elevation=elevation, azimuth=azimuth, 
        left_margin=left_margin, bottom_margin=bottom_margin, right_margin=right_margin, top_margin=top_margin,
        xpad=xpad, ypad=ypad, zpad=zpad, xlabelpad=xlabelpad, ylabelpad=ylabelpad, zlabelpad=zlabelpad,
       xlabelsize=xlabelsize, ylabelsize=ylabelsize, zlabelsize=zlabelsize, legendsize=legendsize)
the_plt.show()
"""

        if "“加载案例”" not in tab.controls['Exp_input'].get("1.0", tk.END):
            save_choice = messagebox.askyesno("提示", "引入案例会替换之前的信息，是否继续引入案例？")
            if not save_choice:
                return

        decode_codestr(content)



    def decode_codestr(txt):
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        tab_name = notebook.tab(current_tab, "text")

        if 'draw_lines' in txt:
            try_type = '绘制仿真折线图'
        elif 'draw_3D' in txt:
            try_type = '绘制仿真三维图'
        elif 'draw_max_area' in txt:
            try_type = '绘制模式比较图'
        elif 'draw_detail_area' in txt:
            try_type = '绘制关系区域图'
        else:
            try_type = '其他代码'

        if tab_name != try_type:
            messagebox.showerror("选择错误", f"当前代码的绘图类型`{try_type}`与该面板绘图类型`{tab_name}`不一致，请重新选择！")
            return

        pattern = re.compile(r"expressions\s*=\s*\{([\s\S]*?)\}\n", re.MULTILINE)
        match = pattern.search(txt)

        Exp_input_get = match.group(1)
        # 进行替换操作
        Exp_input_get = Exp_input_get.replace("r'$", "").replace("$'", "").replace(",", "").replace(":", "=").replace("**", "^").replace("\t", "")
        # print(Exp_input_get)

        tab.controls['Exp_input'].delete("1.0", tk.END)
        tab.controls['Exp_input'].insert(tk.END, Exp_input_get.strip())

        pattern = re.compile(r"assigns\s*=\s*\{([\s\S]*?)\}", re.MULTILINE)
        match = pattern.search(txt)
        if match:
            Assi_input_get = match.group(1)
            # 进行替换操作
            Assi_input_get = Assi_input_get.replace(":", "=").strip()
            tab.controls['Assigns_input'].delete("1.0", tk.END)
            tab.controls['Assigns_input'].insert(tk.END, Assi_input_get.strip())
        else:
            tab.controls['Assigns_input'].delete("1.0", tk.END)

        pattern = re.compile(r"x_name\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
        match = pattern.search(txt)
        if match:
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['x_name'].delete(0, tk.END)
            tab.controls['x_name'].insert(0, the_get)
        else:
            tab.controls['x_name'].delete(0, tk.END)

        pattern = re.compile(r"y_name\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
        match = pattern.search(txt)
        if match:
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['y_name'].delete(0, tk.END)
            tab.controls['y_name'].insert(0, the_get)
        else:
            tab.controls['y_name'].delete(0, tk.END)

        pattern = re.compile(r"fsize\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
        match = pattern.search(txt)
        the_get = match.group(1)
        tab.controls['fsize'].delete(0, tk.END)
        tab.controls['fsize'].insert(0, the_get)

        pattern = re.compile(r"xrotation\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
        match = pattern.search(txt)
        the_get = match.group(1)
        tab.controls['xrotation'].delete(0, tk.END)
        tab.controls['xrotation'].insert(0, the_get)

        pattern = re.compile(r"yrotation\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
        match = pattern.search(txt)
        the_get = match.group(1)
        tab.controls['yrotation'].delete(0, tk.END)
        tab.controls['yrotation'].insert(0, the_get)

        pattern = re.compile(r"figsize\s*=\s*\[(.*?)\]", re.MULTILINE)
        match = pattern.search(txt)
        the_get = match.group(1)
        number_list = the_get.split(",")
        tab.controls['figsizeW'].delete(0, tk.END)
        tab.controls['figsizeW'].insert(0, number_list[0].strip())
        tab.controls['figsizeH'].delete(0, tk.END)
        tab.controls['figsizeH'].insert(0, number_list[1].strip())


        if tab_name != '绘制仿真折线图':
            pattern = re.compile(r"the_var_x\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            code_str, variables_str = convert_pycode(Exp_input_get)
            if code_str:
                # 更新x_list和y_list
                variables = variables_str.split(", ")
                tab.controls['x_list']['values'] = variables
                tab.controls['y_list']['values'] = variables
                tab.controls['print_log'].configure(state='normal')
                tab.controls['print_log'].delete("1.0", tk.END)
                tab.controls['print_log'].insert(tk.END, "公式识别成功！")
                tab.controls['print_log'].configure(state='disabled')
            else:
                # 识别失败，显示错误信息
                tab.controls['print_log'].configure(state='normal')
                tab.controls['print_log'].delete("1.0", tk.END)
                tab.controls['print_log'].insert(tk.END, variables_str)
                tab.controls['print_log'].configure(state='disabled')
            tab.controls['x_list'].set(the_get)

            pattern = re.compile(r"the_var_y\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            tab.controls['y_list'].set(the_get)


        else:
            pattern = re.compile(r"the_var\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            code_str, variables_str = convert_pycode(Exp_input_get)
            if code_str:
                # 更新x_list和y_list
                variables = variables_str.split(", ")
                tab.controls['x_list']['values'] = variables
                tab.controls['print_log'].configure(state='normal')
                tab.controls['print_log'].delete("1.0", tk.END)
                tab.controls['print_log'].insert(tk.END, "公式识别成功！")
                tab.controls['print_log'].configure(state='disabled')

            else:
                # 识别失败，显示错误信息
                tab.controls['print_log'].configure(state='normal')
                tab.controls['print_log'].delete("1.0", tk.END)
                tab.controls['print_log'].insert(tk.END, variables_str)
                tab.controls['print_log'].configure(state='disabled')
            tab.controls['x_list'].set(the_get)

            pattern = re.compile(r"ranges\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['x_start'].delete(0, tk.END)
            tab.controls['x_start'].insert(0, number_list[0].strip())
            tab.controls['x_end'].delete(0, tk.END)
            tab.controls['x_end'].insert(0, number_list[1].strip())
            tab.controls['x_interval'].delete(0, tk.END)
            tab.controls['x_interval'].insert(0, number_list[2].strip())

        if tab_name == '绘制仿真折线图':
            pattern = re.compile(r"location\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['location'].set(the_get)

            pattern = re.compile(r"ncol\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.strip()
            tab.controls['ncol'].delete(0, tk.END)
            tab.controls['ncol'].insert(0, the_get)

        if tab_name == '绘制模式比较图':
            pattern = re.compile(r"texts\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['the_marker'].delete(0, tk.END)
            tab.controls['the_marker'].insert(0, the_get)

            pattern = re.compile(r"start_end_x\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['x_start'].delete(0, tk.END)
            tab.controls['x_start'].insert(0, number_list[0].strip())
            tab.controls['x_end'].delete(0, tk.END)
            tab.controls['x_end'].insert(0, number_list[1].strip())

            pattern = re.compile(r"start_end_y\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['y_start'].delete(0, tk.END)
            tab.controls['y_start'].insert(0, number_list[0].strip())
            tab.controls['y_end'].delete(0, tk.END)
            tab.controls['y_end'].insert(0, number_list[1].strip())

        if tab_name == '绘制关系区域图':
            pattern = re.compile(r"prefix\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("'", "").strip()
            tab.controls['the_pref'].delete(0, tk.END)
            tab.controls['the_pref'].insert(0, the_get)

            pattern = re.compile(r"numbers\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("'", "").strip()
            tab.controls['marker_way'].set(the_get)

            pattern = re.compile(r"start_end_x\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['x_start'].delete(0, tk.END)
            tab.controls['x_start'].insert(0, number_list[0].strip())
            tab.controls['x_end'].delete(0, tk.END)
            tab.controls['x_end'].insert(0, number_list[1].strip())

            pattern = re.compile(r"start_end_y\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['y_start'].delete(0, tk.END)
            tab.controls['y_start'].insert(0, number_list[0].strip())
            tab.controls['y_end'].delete(0, tk.END)
            tab.controls['y_end'].insert(0, number_list[1].strip())

        if tab_name == '绘制仿真三维图':
            pattern = re.compile(r"start_end_x\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['x_start'].delete(0, tk.END)
            tab.controls['x_start'].insert(0, number_list[0].strip())
            tab.controls['x_end'].delete(0, tk.END)
            tab.controls['x_end'].insert(0, number_list[1].strip())

            pattern = re.compile(r"start_end_y\s*=\s*\[(.*?)\]", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            number_list = the_get.split(",")
            tab.controls['y_start'].delete(0, tk.END)
            tab.controls['y_start'].insert(0, number_list[0].strip())
            tab.controls['y_end'].delete(0, tk.END)
            tab.controls['y_end'].insert(0, number_list[1].strip())

            pattern = re.compile(r"location\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['location'].set(the_get)

            pattern = re.compile(r"ncol\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.strip()
            tab.controls['ncol'].delete(0, tk.END)
            tab.controls['ncol'].insert(0, the_get)

            pattern = re.compile(r"z_name\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.replace("r'", "").replace("'", "").strip()
            tab.controls['z_name'].delete(0, tk.END)
            tab.controls['z_name'].insert(0, the_get)

            pattern = re.compile(r"elevation\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.strip()
            tab.controls['elevation'].delete(0, tk.END)
            tab.controls['elevation'].insert(0, the_get)

            pattern = re.compile(r"azimuth\s*=\s*([\s\S]*?)(\n|$)", re.MULTILINE)
            match = pattern.search(txt)
            the_get = match.group(1)
            the_get = the_get.strip()
            tab.controls['azimuth'].delete(0, tk.END)
            tab.controls['azimuth'].insert(0, the_get)


    def import_code():
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")])
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        decode_codestr(content)


    def combile_code():
        pycode_str = ""
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        exp_text = tab.controls['Exp_input'].get("1.0", tk.END)
        code_str, variables_str = convert_pycode(exp_text)

        if not code_str:
            # 识别失败，显示错误信息
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, variables_str)
            tab.controls['print_log'].configure(state='disabled')
            return

        Assigns_text = tab.controls['Assigns_input'].get("1.0", tk.END).strip()
        assi_str = Assigns_text.replace("=", ": ")

        x_var_name = tab.controls['x_list'].get()
        x_start_val = tab.controls['x_start'].get()
        x_end_val = tab.controls['x_end'].get()

        x_name_str = tab.controls['x_name'].get()
        y_name_str = tab.controls['y_name'].get()

        fsize_str = tab.controls['fsize'].get()
        figsizeW_str = tab.controls['figsizeW'].get()
        figsizeH_str = tab.controls['figsizeH'].get()

        xrotation_str = tab.controls['xrotation'].get()
        yrotation_str = tab.controls['yrotation'].get()

        if tab_index == 0:
            x_interval_val = tab.controls['x_interval'].get()
            location_str = tab.controls['location'].get()
            ncol_str = tab.controls['ncol'].get()

            if assi_str != '':
                pycode_str = f"""\n{code_str}\n\n# 参数赋值\nassigns = {{{assi_str}}}\n\n"""
            else:
                pycode_str = f"""\n{code_str}\n\n# 参数赋值\nassigns = {{ }}\n\n"""

            pycode_str += f"""# 要分析的参数，及其取值范围\nthe_var = {x_var_name}\nranges = [{x_start_val}, {x_end_val}, {x_interval_val}]""" + \
                         f"""\n\n# xy轴的名字\nx_name = r'{x_name_str}'\ny_name = r'{y_name_str}'\n\n# 图片保存路径、文件名\nsave_dir = None\n\n""" + \
                         f"""# 图例的方位\nlocation = '{location_str}'\n# 图例的列数\nncol = {ncol_str}\n\n# 图片中字号的大小\nfsize = {fsize_str}\n# 图片的大小\n""" + \
                         f"""figsize = [{figsizeW_str}, {figsizeH_str}]\n\nxt_rotation = 0 # 横轴刻度标签旋转角度。\n# x/y轴名字标签旋转角度。\nxrotation = {xrotation_str}\nyrotation = {yrotation_str}""" + \
                         f"""\n\n# 线的风格，实线'-'，点横线'-.'，虚线'--'，点线':'等。\nlinestyles = ['-','-.','--', ':', (0, (1, 10)), (0, (5, 10)), (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]""" + \
                f"""\nlinewidth = 1.0 # 线粗。\n# 线上的标记符号,关于标记符号的详细说明 https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers\n""" + \
                f"""markers = ['o','s', '*', 'P', 'X', 'D', 'p', 'x', '8', '2', 'H', '+', '|', '<', '>', '^', 'v', ',']\nmarkersize = 3.5 # 标记符号的大小，默认3.5。\n""" + \
                f"""# 线的颜色\ncolors = ['black', 'blue', 'green', 'red', 'darkgoldenrod', 'darkcyan', 'indigo', 'chocolate', 'navy', 'purple']\nisgrid = False\n""" + \
                f"""# 分别为x/y轴刻度值距离横轴的距离。\nxpad = 3\nypad = 3\n# 分别为x/y轴名字标签距离纵轴刻度的距离。\nxlabelpad = 7\nylabelpad = 7\n\n# 坐标轴字体大小\n""" + \
                f"""xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大\nylabelsize = 'auto' # 纵轴字大小\nlegendsize = 'auto' # 图例字大小\n\n# 传给draw_lines函数\n"""+ \
                f"""the_plt = draw_lines(expressions=expressions, assigns=assigns, the_var=the_var, ranges=ranges, x_name=x_name, y_name=y_name, 
    save_dir=save_dir, location=location, ncol=ncol, fsize=fsize, figsize=figsize, xt_rotation=xt_rotation,
    xrotation=xrotation, yrotation=yrotation, linestyles=linestyles, linewidth=linewidth, markers=markers,
    markersize=markersize, colors=colors, isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad,
    xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize)\nthe_plt.show()"""

        elif tab_index == 1:
            y_var_name = tab.controls['y_list'].get()
            y_start_val = tab.controls['y_start'].get()
            y_end_val = tab.controls['y_end'].get()

            the_marker_val = tab.controls['the_marker'].get()
            if the_marker_val.strip() == "":
                new_marker_val = 'None'
            else:
                tmp_the_marker_val = the_marker_val.split(",")
                new_marker_val = "["
                for ii, em in enumerate(tmp_the_marker_val):
                    if ii != 0:
                        new_marker_val += ", r'"+em.strip()+"'"
                    else:
                        new_marker_val += "r'" + em.strip() + "'"
                new_marker_val += "]"

            pycode_str = f"""
{code_str}

# 参数赋值
assigns = {{{assi_str}}}

# 要分析的参数，及其取值范围
the_var_x = {x_var_name}
start_end_x = [{x_start_val}, {x_end_val}]  # [起始值, 终止值]。 
the_var_y = {y_var_name}
start_end_y = [{y_start_val}, {y_end_val}]  # [起始值, 终止值]。 

# xy轴的名字
x_name = r'{x_name_str}' 
y_name = r'{y_name_str}'  

# 图片保存路径、文件名
save_dir = None 

# 四个表达式分别达到最大时显示的标签、区域背景颜色和区域图案。
texts = {new_marker_val} 
colors = 'sci'
patterns = 'sci'

# 其他设置
fsize = {fsize_str}
text_fsize_add = 2 # 区域标签字号增量。
# 图片大小。
figsize = [{figsizeW_str}, {figsizeH_str}] 
# x轴标签名旋转角度（0为不旋转）。
xrotation = {xrotation_str}  
# y轴标签名旋转角度（0为不旋转）。 
yrotation = {yrotation_str} 
linewidths = 0.1 # 线粗

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 3

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = 'auto'
pattern_moves = [(0, 0), (0, 0), (0, 0), (0, 0)]  # 区域标签较原来的偏移量，(x方向，y方向)

# 传给draw_max_area函数
the_plt = draw_max_area(expressions=expressions, assigns=assigns, 
              the_var_x=the_var_x, start_end_x=start_end_x, 
              the_var_y=the_var_y, start_end_y=start_end_y, 
              x_name=x_name, y_name=y_name, 
              fsize=fsize, texts=texts, text_fsize_add=text_fsize_add,
              save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
              xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
             xlabelsize=xlabelsize, ylabelsize=ylabelsize, pattern_colors=pattern_colors, 
              pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
the_plt.show()
"""
        elif tab_index == 2:
            y_var_name = tab.controls['y_list'].get()
            y_start_val = tab.controls['y_start'].get()
            y_end_val = tab.controls['y_end'].get()

            the_pref_val = tab.controls['the_pref'].get()
            marker_way_val = tab.controls['marker_way'].get()


            pycode_str = f"""
{code_str}

# 参数赋值
assigns = {{{assi_str}}}

# 要分析的参数，及其取值范围
the_var_x = {x_var_name}
start_end_x = [{x_start_val}, {x_end_val}] 
the_var_y = {y_var_name}
start_end_y = [{y_start_val}, {y_end_val}] 

# xy轴的名字
x_name = r'{x_name_str}' 
y_name = r'{y_name_str}'  

# 图片保存路径、文件名
save_dir = None 

# 每个关系区域的标签前缀、编号样式、背景颜色和图案。
# 前缀。可以是"区域"也可以是"Region"，默认"Region"。
prefix = '{the_pref_val}'
# 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。
numbers = '{marker_way_val}' 
colors = 'sci'
patterns = 'sci'

# 其他设置
fsize = {fsize_str}
text_fsize_add = -2 # 区域标签字号增量。 Increment of regional label font size.
# 图片大小。
figsize = [{figsizeW_str}, {figsizeH_str}] 
# x轴标签名旋转角度（0为不旋转）。
xrotation = {xrotation_str}  
# y轴标签名旋转角度（0为不旋转）。 
yrotation = {yrotation_str} 
linewidths = 0.1 # 线粗

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 3

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 'auto' # 图例字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = 'auto'  # 设置标签背景色，'auto'为自动，'none'为透明
pattern_moves = [(0, 0), (0, 0), (0, 0), (0, 0)]  # 设定区域标签较原来的偏移量，(x方向，y方向)   

# 传给draw_detail_area函数
the_plt = draw_detail_area(expressions=expressions, assigns=assigns, 
        the_var_x=the_var_x, start_end_x=start_end_x, 
        the_var_y=the_var_y, start_end_y=start_end_y, 
        x_name=x_name, y_name=y_name, 
        fsize=fsize, text_fsize_add=text_fsize_add,
        save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
        xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
        prefix=prefix, numbers=numbers, xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize, 
      pattern_colors=pattern_colors, pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
the_plt.show()
"""
        else:
            y_var_name = tab.controls['y_list'].get()
            y_start_val = tab.controls['y_start'].get()
            y_end_val = tab.controls['y_end'].get()

            z_name_str = tab.controls['z_name'].get()

            location_str = tab.controls['location'].get()
            ncol_str = tab.controls['ncol'].get()

            zrotation_str = tab.controls['zrotation'].get()
            azimuth_str = tab.controls['azimuth'].get()
            elevation_str = tab.controls['elevation'].get()

            pycode_str = f"""
{code_str}

# 参数赋值
assigns = {{{assi_str}}}

# 要分析的参数，及其取值范围
the_var_x = {x_var_name}
start_end_x = [{x_start_val}, {x_end_val}] 
the_var_y = {y_var_name}
start_end_y = [{y_start_val}, {y_end_val}] 

# xy轴的名字
x_name = r'{x_name_str}' 
y_name = r'{y_name_str}'  
z_name = r'{z_name_str}'

# 图片保存路径、文件名
save_dir = None 

# 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。
color_alpha = 0.8 
# 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。
location = '{location_str}' 
# 图例的列数，默认为1列，即竖着排布。
ncol = {ncol_str}
# 图片中字号的大小
fsize = {fsize_str}
# 图片的大小，写成`[宽, 高]`的形式。默认为`[7, 5]`。
figsize = [{figsizeW_str}, {figsizeH_str}]
# xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。
xrotation = {xrotation_str}
yrotation = {yrotation_str}
# Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴
zrotation = {zrotation_str}
# 是否要网格。要就填True，不要就是False
isgrid = True

# 在多面图中用于按顺序制定每个面的颜色（包含标记符号的颜色）。
colors = ['yellow','blue','red','green', 'darkgoldenrod', 'darkcyan', 'indigo', 'chocolate', 'navy', 'purple']
# 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。
edgecolor = 'black'
linestyles = ['-','-.','--', ':', (0, (1, 10)), (0, (5, 10)), (0, (3, 10, 1, 10, 1, 10)), (5, (10, 3)), (0, (5, 5)), (0, (5, 1))]
linewidth = 0.5 # 线粗。
density = 50 # 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。

# 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。
elevation = {elevation_str}
# 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。
azimuth = {azimuth_str}

# 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。
left_margin = 0
bottom_margin = 0
right_margin = 1
top_margin = 1

# 分别为/y/z轴刻度值距离横轴的距离。
xpad = 3
ypad = 3
zpad = 3

# 分别为/y/z轴名字标签距离纵轴刻度的距离。
xlabelpad = 7
ylabelpad = 7
zlabelpad = 7

# 自定义坐标轴字体大小
xlabelsize = 'auto' # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
zlabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 'auto' # 图例字大小，默认'auto'，自动和fsize一样大

# 传给draw_3D函数 (不要改！)
# Passed to the draw_3D function (Don't change!).
the_plt = draw_3D(expressions=expressions, assigns=assigns, the_var_x=the_var_x, start_end_x=start_end_x, the_var_y=the_var_y, 
        start_end_y=start_end_y, x_name=x_name, y_name=y_name, z_name=z_name, 
        save_dir=save_dir, color_alpha=color_alpha, location=location, ncol=ncol, fsize=fsize, figsize=figsize, 
        xrotation=xrotation, yrotation=yrotation, zrotation=zrotation, isgrid=isgrid, colors=colors, 
        edgecolor=edgecolor, linestyles=linestyles, linewidth=linewidth, density=density, elevation=elevation, azimuth=azimuth, 
        left_margin=left_margin, bottom_margin=bottom_margin, right_margin=right_margin, top_margin=top_margin,
        xpad=xpad, ypad=ypad, zpad=zpad, xlabelpad=xlabelpad, ylabelpad=ylabelpad, zlabelpad=zlabelpad,
       xlabelsize=xlabelsize, ylabelsize=ylabelsize, zlabelsize=zlabelsize, legendsize=legendsize)
the_plt.show()
"""
        return pycode_str


    def check_syntax():
        # 这里应该添加语法检查的实际实现
        # messagebox.showinfo("语法检查", "语法检查功能尚未实现。")
        # 假设语法检查通过，启用绘制和保存按钮
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]

        try:
            pycode_str = combile_code()
            ast.parse(pycode_str)
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, f"OK！所有填写的信息语法上无错误！代码如下：\n\n{pycode_str}")
            tab.controls['print_log'].configure(state='disabled')
            return 'OK'
        except SyntaxError as e:
            # print(f"填写的信息存在语法错误: {e}\n\n{pycode_str}")
            # 识别失败，显示错误信息
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, f"填写的信息存在语法错误: {e}")
            tab.controls['print_log'].configure(state='disabled')
            return 'NO'

    def draw_image():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        try:
            # 这里应该添加绘制图片的实际实现
            ret = check_syntax()
            if ret != 'OK':
                messagebox.showerror("绘制图片", "信息有误，绘制失败。")
                return
            # 绘制成功，启用保存图片按钮
            pycode_str = combile_code()
            exec(pycode_str)
        except Exception as e:
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, f"填写的信息存在语法错误: {e}")
            tab.controls['print_log'].configure(state='disabled')


    def save_code():
        current_tab = notebook.select()
        tab_index = notebook.index(current_tab)
        tab = tabs[tab_index]
        try:
            pycode_str = combile_code()
            file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                     filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")])
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(pycode_str)
                messagebox.showinfo("保存代码", f"代码已保存到：{file_path}")
        except Exception as e:
            tab.controls['print_log'].configure(state='normal')
            tab.controls['print_log'].delete("1.0", tk.END)
            tab.controls['print_log'].insert(tk.END, f"填写的信息存在语法错误: {e}")
            tab.controls['print_log'].configure(state='disabled')

    # 启动主循环
    root.mainloop()

def make_example(fun_name):
    welcome = "Welcome to use the tools for thesis simulation drawing. The available functions include `data_lines`, `draw_lines`, `draw_3D`, `draw_max_area`, `draw_detail_area`, etc." + \
              "\nIf you want to display high-definition pictures in Jupyter, please use `%config InlineBackend.figure_format = " + "'retina'`." + \
              "\nIf you want to generate example code, please run the function`make_example(<data_lines/draw_lines/draw_3D/draw_max_area/draw_detail_area>)`." + \
              "\n欢迎使用论文模拟绘图工具。可用功能包括 `data_lines`(由数据点画线), `draw_lines`(符号函数仿真画线), `draw_3D`(符号函数仿真画3维图), `draw_max_area`(符号函数俩参数分析-“最大区域图”), `draw_detail_area`(符号函数俩参数分析-“不同关系区域图”) 等。" + \
              "\n如果您想在 Jupyter 中显示高清图片，请使用 `% config InlineBackend.figure_format = 'retina'`。" + \
              "\n如果你想生成实例代码，请运行函数`make_example(<data_lines/draw_lines/draw_3D/draw_max_area/draw_detail_area>)`。"

    data_lines_code = r"""
# 以方括号（列表、numpy数组均可）形式给出数据，并给这组数据起个名字：
data = {
    '景区1旅游人次': [1230, 45789, 2600, 320, 991480, 65780, 89990, 70001, 6423, 415000, 340, 102],
    '景区2旅游人次': [800, 34000, 1690, 139, 76788, 453565, 87898, 64302, 3423, 325001, 127, 13],
    '景区3旅游人次': [5230, 65789, 7600, 820, 1091480, 85780, 99995, 90001, 9423, 705000, 640, 707],
}

# 给横轴添加刻度标签，注意要和data长度一致！
label_x = ['2020-1', '2020-2', '2020-3', '2020-4',  '2020-5', '2020-6',  '2020-7',  '2020-8',  '2020-9',  
           '2020-10',  '2020-11',  '2020-12']

# 自定义xy轴名称：
x_name = '月总旅游人次'
y_name = '月份'

# 保存路径
save_dir = 'data_sigle.tiff'

# 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。
# 默认值为'best'，表示自动安排至合适的位置。
location = 'best'
# 图例的列数，默认为1列，即竖着排布。
ncol = 1

fsize = 14 # 图片中字号的大小，默认值为14。
figsize = [7, 5] # 图片的大小，写成`[宽, 高]`的形式。

# 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
xt_rotation = 45

# 横轴名字标签旋转角度，默认值0，基本不需要动。
xrotation = 0
# 纵轴名字标签旋转角度，默认值90，字是正的。如果y轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴y轴。
yrotation = 90 

# 一组线的形状，如实线'-'，点横线'-.'，虚线'--'，点线':'。
linestyles = ['-', '-.','--'] 
linewidth = 1.2 # 线粗。

markers = ['o','s', '*'] # 线上的标记符号,关于标记符号的详细说明 https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
markersize = 3.5 # 标记符号的大小，默认3.5。
# 四条线的颜色
colors = ['blue','red','green']

isgrid = False # 是否要网格。要就填True，不要就是False，默认不要。
# x/y轴刻度值距离横轴的距离
xpad = 3
ypad = 3
# x/y轴名字标签距离横轴刻度的距离。
xlabelpad = 3
ylabelpad = 3

# 传给data_lines函数 (不要改！)
# Passed to the data_lines function (Don't change!).
data_lines(data, label_x=label_x, x_name=x_name, y_name=y_name, save_dir=save_dir, location=location, ncol=ncol,
           fsize=fsize, figsize=figsize, xt_rotation=xt_rotation, xrotation=xrotation, yrotation=yrotation, 
           linestyles=linestyles, linewidth=linewidth, markers=markers, markersize=markersize, colors=colors,
          isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
    """

    draw_lines_code = r"""
# 定义符号 
# Define symbols
c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha = symbols('c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha')

# 四个表达式
# Four expressions
expressions = {
    r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2), 
    r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2), 
    r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
    r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
# Parameter assignment
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1, alpha:0.9}

# 要分析的参数，及其取值范围
# The parameters to be analyzed and their value ranges.
the_var = b
ranges = [0, 0.08, 0.01]  # [起始值, 终止值, 间隔]。 [Starting value, ending value, interval].

# xy轴的名字
# The names of the x-axis and y-axis.
x_name = r'(a) Parameter $b$'
y_name = r'$\pi_r$'

# 图片保存路径、文件名
# Picture save path and file name.
save_dir = r'mutiple_line.tiff'

# 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。
# 默认值为'best'，表示自动安排至合适的位置。
location = 'best' 

# 图例的列数，默认为1列，即竖着排布。
ncol = 1
# 图片中字号的大小
fsize = 14
# 图片的大小，写成`[宽, 高]`的形式。
figsize = [5, 4]

xt_rotation = 0 # 横轴刻度标签旋转角度。用于刻度为年份，横着挤不下的情况，可以设成45度，错开排布。默认不旋转，即0度。
# xrotation/yrotation: x/y轴名字标签旋转角度。
xrotation = 0
yrotation = 90

linestyles = ['-','-.','--', ':'] # 线的风格，实线'-'，点横线'-.'，虚线'--'，点线':'。
linewidth = 1.0 # 线粗。
markers = ['o','s', '*', 'P'] # 线上的标记符号,关于标记符号的详细说明 https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
markersize = 3.5 # 标记符号的大小，默认3.5。
# 四条线的颜色
colors = ['black','blue','red','green']

# 是否要网格。要就填True，不要就是False
isgrid = False

# 分别为x/y轴刻度值距离横轴的距离。
xpad = 3
ypad = 3

# 分别为x/y轴名字标签距离纵轴刻度的距离。
xlabelpad = 2
ylabelpad = 2


# 传给draw_lines函数 (不要改！)
# Passed to the draw_lines function (Don't change!).
draw_lines(expressions=expressions, assigns=assigns, the_var=the_var, ranges=ranges, x_name=x_name, y_name=y_name, 
           save_dir=save_dir, location=location, ncol=ncol, fsize=fsize, figsize=figsize, xt_rotation=xt_rotation,
          xrotation=xrotation, yrotation=yrotation, linestyles=linestyles, linewidth=linewidth, markers=markers,
          markersize=markersize, colors=colors, isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
    """

    draw_3D_code = r"""
# 定义符号 
# Define symbols
c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha = symbols('c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha')

# 四个表达式
# Four expressions
expressions = {
    r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2), 
    r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2), 
    r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
    r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
# Parameter assignment
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1}

# 要分析的参数，及其取值范围
# The parameters to be analyzed and their value ranges.
the_var_x = alpha
start_end_x = [0.7, 0.8]  # [起始值, 终止值]。 [starting value, ending value].
the_var_y = b
start_end_y = [0, 0.08]  # [起始值, 终止值]。 [starting value, ending value].

# xy轴的名字
# The names of the x-axis and y-axis.
x_name = r'$\alpha$' 
y_name = r'$b$'
z_name = r'$\pi_r$' 

# 图片保存路径、文件名
# Picture save path and file name.
save_dir = r'muti_3d.tiff'

# 曲面的透明度。取值范围0到1，浮点数。0表示全透明，1表示完全不透明。
color_alpha = 0.8 

# 图例的方位，可以选填的内容有'best','northeast','northwest','southwest','southeast','east','west','south','north','center'。
# 默认值为'best'，表示自动安排至合适的位置。
location = 'best'

# 图例的列数，默认为1列，即竖着排布。
ncol = 4
# 图片中字号的大小
fsize = 14
# 图片的大小，写成`[宽, 高]`的形式。
figsize = [7, 5]

# xrotation/yrotation: x/y轴名字标签旋转角度，默认值0，基本不需要动。
xrotation = 0
yrotation = 0

# Z轴名字标签旋转角度，默认值90，字是正的。如果Z轴的名字较长，不好看，可以设成0，字是竖倒着写的，紧贴Z轴
zrotation = 90
# 是否要网格。要就填True，不要就是False
isgrid = True

# 在多面图中用于按顺序制定每个面的颜色（包含标记符号的颜色）。
colors = ['yellow','blue','red','green']
# 曲面上线框的颜色。若为None，则曲面上不画线。当该参数不为None时，参数`linestyles`，`linewidth`和`density`才起作用。
edgecolor = 'black'
linestyles = ['-','-.','--', ':'] # 实线'-'，点横线'-.'，虚线'--'，点线':'。
linewidth = 0.5 # 线粗。
density = 50 # 曲面上画线的密度，也就是曲面横纵方向各画多少根线。默认100。

# 仰角 (elevation)。定义了观察者与 xy 平面之间的夹角，也就是观察者与 xy 平面之间的旋转角度。
elevation = 15
# 方位角 (azimuth)。定义了观察者绕 z 轴旋转的角度。它决定了观察者在 xy 平面上的位置。
azimuth = 45

# 左、下、右、上的图片留白，默认分别为0,0,1,1。不需要动，除非不好看。
left_margin = 0
bottom_margin = 0
right_margin = 1
top_margin = 1

# 分别为x/y/z轴刻度值距离横轴的距离。
xpad = 1
ypad = 1
zpad = 5

# 分别为x/y/z轴名字标签距离纵轴刻度的距离。
xlabelpad = 2
ylabelpad = 2
zlabelpad = 12


# 传给draw_3D函数 (不要改！)
# Passed to the draw_3D function (Don't change!).
draw_3D(expressions=expressions, assigns=assigns, the_var_x=the_var_x, start_end_x=start_end_x, the_var_y=the_var_y, 
        start_end_y=start_end_y, x_name=x_name, y_name=y_name, z_name=z_name, 
        save_dir=save_dir, color_alpha=color_alpha, location=location, ncol=ncol, fsize=fsize, figsize=figsize, 
        xrotation=xrotation, yrotation=yrotation, zrotation=zrotation, isgrid=isgrid, colors=colors, 
        edgecolor=edgecolor, linestyles=linestyles, linewidth=linewidth, density=density, elevation=elevation, azimuth=azimuth, 
        left_margin=left_margin, bottom_margin=bottom_margin, right_margin=right_margin, top_margin=top_margin,
        xpad=xpad, ypad=ypad, zpad=zpad, xlabelpad=xlabelpad, ylabelpad=ylabelpad, zlabelpad=zlabelpad) 
    """

    draw_max_area_code = r"""
# 定义符号 
# Define symbols
c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha = symbols('c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha')

# 四个表达式
# Four expressions
expressions = {
    r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2), 
    r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2), 
    r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
    r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
# Parameter assignment
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1}

# 要分析的参数，及其取值范围
# The parameters to be analyzed and their value ranges.
the_var_x = alpha
start_end_x = [0.7, 0.8]  # [起始值, 终止值]。 [starting value, ending value].
the_var_y = b
start_end_y = [0, 0.08]  # [起始值, 终止值]。 [starting value, ending value].

# xyz轴的名字
# The names of the x-axis and y-axis.
x_name = '$\\alpha$ \n (b) With blockchain' 
y_name = r'$b$'  

# 图片保存路径、文件名
# Picture save path and file name.
save_dir = r'max_area.tiff' 

# 四个表达式分别达到最大时显示的标签、区域背景颜色和区域图案。
# The labels, regional background colors and regional patterns displayed when the four expressions reach their maxima respectively.
texts = [r'NW', r'BW', r'NS', r'BS']  
colors = ['#dae3f3', '#fbe5d6', '#e2f0d9', '#ededed']
patterns = [' ', '+', '\\', '-']

# 其他设置
text_fsize_add = 2 # 区域标签字号增量。 Increment of regional label font size.
figsize=[5, 4] # 图片大小：宽5高4。 icture size: width 5, height 4.
xrotation=0 # x轴标签名旋转角度（0为不旋转）。 Rotation angle of x-axis label name (0 means no rotation).
yrotation=0 # y轴标签名旋转角度（0为不旋转）。 Rotation angle of y-axis label name (0 means no rotation).
linewidths=0.1 # 线粗0.1. Line thickness: 0.1.

# 传给draw_max_area函数（不要改！）
# Passed to the draw_max_area function (Don't change!).
draw_max_area(expressions=expressions, assigns=assigns, 
              the_var_x=the_var_x, start_end_x=start_end_x, 
              the_var_y=the_var_y, start_end_y=start_end_y, 
              x_name=x_name, y_name=y_name, 
              fsize=14, texts=texts, text_fsize_add=text_fsize_add,
              save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
              xrotation=xrotation, yrotation=yrotation, linewidths=linewidths)

    """

    draw_detail_area_code = r"""
# 定义符号 
# Define symbols
c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha = symbols('c_n, c_r, delta, e_n, e_r, p_e, E, k, b, alpha')

# 四个表达式
# Four expressions
expressions = {
    r'$\pi_r^{NW}$': E*p_e+(k*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2)/(8*(k+alpha*delta*(1-alpha*delta))**2), 
    r'$\pi_r^{BW}$': E*p_e + ( k*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+delta-delta**2)**2), 
    r'$\pi_r^{NS}$': E*p_e + ((k+2*alpha*delta)*(alpha*delta*(c_n+e_n*p_e)-(c_r+e_r*p_e))**2 )/( 8*(k+alpha*delta*(2-alpha*delta))**2),
    r'$\pi_r^{BS}$': E*p_e + ( (k+2*delta)*(delta*(c_n+e_n*p_e)-(c_r+e_r*p_e+b))**2 )/( 8*(k+2*delta-delta**2)**2),
}

# 参数赋值
# Parameter assignment
assigns = {c_n: 0.2, c_r: 0.1, delta: 0.8, e_n: 1, e_r: 0.6, p_e: 0.1, E: 2, k: 1.1}

# 要分析的参数，及其取值范围
# The parameters to be analyzed and their value ranges.
the_var_x = alpha
start_end_x = [0.7, 0.8]  # [起始值, 终止值]。 [starting value, ending value].
the_var_y = b
start_end_y = [0, 0.08]  # [起始值, 终止值]。 [starting value, ending value].

# xy轴的名字
# The names of the x-axis and y-axis.
x_name = '$\\alpha$ \n (b) With blockchain' 
y_name = r'$b$'  

# 图片保存路径、文件名
# Picture save path and file name.
save_dir = r'max_area_detail.tiff' 

# 每个关系区域的标签前缀、编号样式、背景颜色和图案。
# The label prefix, numbering style, background color and pattern of each relational area.
prefix=r'Region'  # 前缀。可以是"区域"也可以是"Region"，默认"Region"。
numbers='roman' # 序号标记风格。有三种可选："roman", "letter" 和"number"，分别表示罗马数字、大写英文字母和阿拉伯数字。Numbering style. There are three options: "roman", "letter", and "number".
colors = ['#dae3f3', '#fbe5d6', '#e2f0d9', '#ededed', 'yellow', '#adb9ca', 'white']
patterns = [' ', '+', '\\', '-', '//', '|', 'o']

# 其他设置
text_fsize_add = -2 # 区域标签字号增量。 Increment of regional label font size.
figsize=[7, 4] # 图片大小：宽5高4。 icture size: width 5, height 4.
xrotation=0 # x轴标签名旋转角度（0为不旋转）。 Rotation angle of x-axis label name (0 means no rotation).
yrotation=0 # y轴标签名旋转角度（0为不旋转）。 Rotation angle of y-axis label name (0 means no rotation).
linewidths=0.1 # 线粗0.1. Line thickness: 0.1.

# 传给draw_detail_area函数（不要改！）
# Passed to the draw_detail_area function (Don't change!).
draw_detail_area(expressions=expressions, assigns=assigns, 
                the_var_x=the_var_x, start_end_x=start_end_x, 
                the_var_y=the_var_y, start_end_y=start_end_y, 
                x_name=x_name, y_name=y_name, 
                fsize=14, text_fsize_add=text_fsize_add,
                save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
                xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
                prefix=prefix, numbers=numbers)
    """

    example_codes = {
        'data_lines': data_lines_code,
        'draw_lines': draw_lines_code,
        'draw_3D': draw_3D_code,
        'draw_max_area': draw_max_area_code,
        'draw_detail_area': draw_detail_area_code
    }
    print(example_codes.get(fun_name, welcome))


if __name__ == '__main__':
    makefig()