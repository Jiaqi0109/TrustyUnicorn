import matplotlib
from matplotlib.font_manager import *
#定义自定义字体，文件名从1.b查看系统中文字体中来
def zh_font():
    myfont = FontProperties(fname='./app/static/fonts/wqy-microhei.ttc')
    #解决负号'-'显示为方块的问题
    matplotlib.rcParams['axes.unicode_minus']=False
    return myfont
