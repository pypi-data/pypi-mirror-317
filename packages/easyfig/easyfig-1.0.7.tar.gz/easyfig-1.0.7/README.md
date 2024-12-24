# Easyfig (原pyfastpaper) 使用说明

工具安装方式：       
（1）安装Python，推荐最新版本即可。官网[https://www.python.org/](https://www.python.org/)     
（2）``Ctrl+R``，输入``cmd``打开命令窗口（黑的），然后在命令窗口内输入：     
``pip install easyfig`` 或``pip install easyfig --upgrade``     
等待安装完成即可。

![img](https://pic4.zhimg.com/v2-0bb2093eb88fb09422bbfdee39686d69_r.jpg)

![img](https://pica.zhimg.com/v2-5af707663517dada34f4a8184273c946_r.jpg)

![img](https://pica.zhimg.com/v2-38f159e124c3192b66babc9b87448dfc_r.jpg)

## 1. 完全没学过Python的同学，使用界面向导

本工具独创UI界面向导，无需输入代码，即可完成仿真绘图，并自动生成规范的Python代码。启动方式：       
（1）``Ctrl+R``，输入``cmd``打开命令窗口（黑的）;         
（2）在命令窗口内输入``easyfig``回车即可。非常简单！

![img](https://pic1.zhimg.com/v2-0550d710bad493c1891e331f7743db24_r.jpg)

使用效果如下：

![png](https://picx.zhimg.com/v2-eb36e3c42a77176a954ba585f7faeac7_r.jpg)

![png](https://pic2.zhimg.com/v2-84aa3aff69fb7c968f0b5298fe23d369_r.jpg)

![png](https://pic3.zhimg.com/v2-32926481295453c64de24d4469086f3c_r.jpg)

![png](https://picx.zhimg.com/v2-7dc8619db724028a89d5ab5a538ab05f_r.jpg)

![img](https://pic4.zhimg.com/v2-c67b37504da7260ad7cfc6f2898aad57_r.jpg)

点击“保存...”，可以将你填写的画图数据保存下载，以.py或.txt的格式；当想重新画图时，点击“打开...”，选择你之前保存的.py或.txt文件，即可恢复之前的工作。

点击“$\Omega$...”，可以打开特殊符号和数学函数选择器，用于直接选取希腊字母和数学函数，如定积分$\int$，绝对值$|x|$，三角函数$\sin(x)$等。

## 2. 有Python基础的同学，推荐用Jupyter，可以直接编程使用，能够更细致地设置图片细节


```python
from easyfig import *   # 固定写法
%config InlineBackend.figure_format = 'retina' # 在 Jupyter 中显示高清图片
```

### 2.1 根据数据绘制曲线（该功能界面向导版没有）


```python
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

# 自定义坐标轴字体大小
xlabelsize = 39 # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 9 # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 17 # 图例字大小，默认'auto'，自动和fsize一样大

# 传给data_lines函数 (不要改！)
# Passed to the data_lines function (Don't change!).
plt = data_lines(data, label_x=label_x, x_name=x_name, y_name=y_name, save_dir=save_dir, location=location, ncol=ncol,
           fsize=fsize, figsize=figsize, xt_rotation=xt_rotation, xrotation=xrotation, yrotation=yrotation, 
           linestyles=linestyles, linewidth=linewidth, markers=markers, markersize=markersize, colors=colors,
          isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad, 
            xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize)
```


![png](https://pic3.zhimg.com/v2-4416be060ee29b77e00d2a573c366a16_r.jpg)


### 2.2 数值仿真符号函数的曲线


```python
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
xlabelpad = 13
ylabelpad = 2

# 自定义坐标轴字体大小
xlabelsize = 39 # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 9 # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 17 # 图例字大小，默认'auto'，自动和fsize一样大


# 传给draw_lines函数 (不要改！)
# Passed to the draw_lines function (Don't change!).
draw_lines(expressions=expressions, assigns=assigns, the_var=the_var, ranges=ranges, x_name=x_name, y_name=y_name, 
           save_dir=save_dir, location=location, ncol=ncol, fsize=fsize, figsize=figsize, xt_rotation=xt_rotation,
          xrotation=xrotation, yrotation=yrotation, linestyles=linestyles, linewidth=linewidth, markers=markers,
          markersize=markersize, colors=colors, isgrid=isgrid, xpad=xpad, ypad=ypad, xlabelpad=xlabelpad, ylabelpad=ylabelpad,
           xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize)
```




![png](https://picx.zhimg.com/v2-64a2347a6f7fe4499423e3653bf711cb_r.jpg)


### 2.3 同时分析两个参数，绘制三维曲线


```python
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

# 分别为/y/z轴刻度值距离横轴的距离。
xpad = 1
ypad = 1
zpad = 5

# 分别为/y/z轴名字标签距离纵轴刻度的距离。
xlabelpad = 2
ylabelpad = 2
zlabelpad = 12

# 自定义坐标轴字体大小
xlabelsize = 39 # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 9 # 纵轴字大小，默认'auto'，自动和fsize一样大
zlabelsize = 'auto' # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 19 # 图例字大小，默认'auto'，自动和fsize一样大


# 传给draw_3D函数 (不要改！)
# Passed to the draw_3D function (Don't change!).
draw_3D(expressions=expressions, assigns=assigns, the_var_x=the_var_x, start_end_x=start_end_x, the_var_y=the_var_y, 
        start_end_y=start_end_y, x_name=x_name, y_name=y_name, z_name=z_name, 
        save_dir=save_dir, color_alpha=color_alpha, location=location, ncol=ncol, fsize=fsize, figsize=figsize, 
        xrotation=xrotation, yrotation=yrotation, zrotation=zrotation, isgrid=isgrid, colors=colors, 
        edgecolor=edgecolor, linestyles=linestyles, linewidth=linewidth, density=density, elevation=elevation, azimuth=azimuth, 
        left_margin=left_margin, bottom_margin=bottom_margin, right_margin=right_margin, top_margin=top_margin,
        xpad=xpad, ypad=ypad, zpad=zpad, xlabelpad=xlabelpad, ylabelpad=ylabelpad, zlabelpad=zlabelpad,
       xlabelsize=xlabelsize, ylabelsize=ylabelsize, zlabelsize=zlabelsize, legendsize=legendsize)
```


![png](https://pic3.zhimg.com/v2-d942b6b539e387c83b601d4433d6687e_r.jpg)


### 2.4 基于最大利润的模式比较


```python
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

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 17

# 自定义坐标轴字体大小
xlabelsize = 8 # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 29 # 纵轴字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = ['#dae3f3', 'white', 'none', 'auto']  # 分别为NW,BW,NS,BS设置标签背景色，'auto'为自动，'none'为透明
pattern_moves = [(+0.005, +0.01), (+0, -0.005), (0, 0), (0, 0)]  # 分别为NW,BW,NS,BS设定区域标签较原来的偏移量，(x方向，y方向)


# 传给draw_max_area函数（不要改！）
# Passed to the draw_max_area function (Don't change!).
draw_max_area(expressions=expressions, assigns=assigns, 
              the_var_x=the_var_x, start_end_x=start_end_x, 
              the_var_y=the_var_y, start_end_y=start_end_y, 
              x_name=x_name, y_name=y_name, 
              fsize=14, texts=texts, text_fsize_add=text_fsize_add,
              save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
              xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
             xlabelsize=xlabelsize, ylabelsize=ylabelsize, pattern_colors=pattern_colors, 
              pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
```

    区域 0: 中心坐标 = [0.7671627089581086, 0.0634762952000335]
    区域 1: 中心坐标 = [0.74544927 0.03695231]
    区域 2: 中心坐标 = [0.7224541825812423, 0.07136930428315474]


![png](https://picx.zhimg.com/v2-38fa3848d5dc77e4c27e6f8ce7b89e31_r.jpg)


### 2.5 不同区域各个函数大小关系呈现


```python
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

# x/y轴名字标签距离横轴刻度的距离
xlabelpad = 3
ylabelpad = 17


# 自定义坐标轴字体大小
xlabelsize = 8 # 横轴字大小，默认'auto'，自动和fsize一样大
ylabelsize = 29 # 纵轴字大小，默认'auto'，自动和fsize一样大
legendsize = 9 # 图例字大小，默认'auto'，自动和fsize一样大

# 标签背景色和位置偏移自定义设置，默认'auto'自动
pattern_colors = ['#dae3f3', 'white', 'none', 'auto']  # 分别为NW,BW,NS,BS设置标签背景色，'auto'为自动，'none'为透明
pattern_moves = [(+0.005, +0.01), (+0, +0.005), (0, 0), (0, 0)]  # 分别为NW,BW,NS,BS设定区域标签较原来的偏移量，(x方向，y方向)


# 传给draw_detail_area函数（不要改！）
# Passed to the draw_detail_area function (Don't change!).
draw_detail_area(expressions=expressions, assigns=assigns, 
                the_var_x=the_var_x, start_end_x=start_end_x, 
                the_var_y=the_var_y, start_end_y=start_end_y, 
                x_name=x_name, y_name=y_name, 
                fsize=14, text_fsize_add=text_fsize_add,
                save_dir=save_dir, figsize=figsize, colors=colors, patterns=patterns,
                xrotation=xrotation, yrotation=yrotation, linewidths=linewidths,
                prefix=prefix, numbers=numbers, xlabelsize=xlabelsize, ylabelsize=ylabelsize, legendsize=legendsize, 
              pattern_colors=pattern_colors, pattern_moves=pattern_moves, xlabelpad=xlabelpad, ylabelpad=ylabelpad)
```

    区域 $\pi_r^{BW} > \pi_r^{BS} > \pi_r^{NS} > \pi_r^{NW}$: 中心坐标 = [0.71801738 0.03542176]
    区域 $\pi_r^{BW} > \pi_r^{BS} > \pi_r^{NW} > \pi_r^{NS}$: 中心坐标 = [0.7522649316484371, 0.050000071576472446]
    区域 $\pi_r^{NW} > \pi_r^{NS} > \pi_r^{BW} > \pi_r^{BS}$: 中心坐标 = [0.75467691 0.06691737]
    区域 $\pi_r^{NS} > \pi_r^{NW} > \pi_r^{BW} > \pi_r^{BS}$: 中心坐标 = [0.72038526 0.07323454]


![png](https://pica.zhimg.com/v2-03574f85a5fff05ce374098723d2809c_r.jpg)



