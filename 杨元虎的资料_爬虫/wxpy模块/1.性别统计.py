import wxpy,os
from pyecharts import Pie
import webbrowser
#
# weichat = wxpy.Bot(cache_path=True)
#
# def show_sex():
#     friends = weichat.friends()
#     man = woman = unknown = 0
#     for f in friends:
#         if f.sex == 1:
#             man += 1
#         elif f.sex == 2:
#             woman += 1
#         else:
#             unknown += 1
#
#     pic = Pie("性别统计")
#     pic.add("", ["man", "woman", "unknown"], [man, woman, unknown], is_label_show=True)
#     pic.render("sex2.html")
#
#     webbrowser.open("sex2.html")
#

# 统计好友性别比例 最后生成一个html图像

# 打开微信二维码 得到一个微信对象\

wx = wxpy.Bot()

# 获取好友列表得到一个列表在列表中循环取出每一个好友对象  注意 friends是一个函数  bot也一样
man = 0
woman = 0
unknown = 0
for f in wx.friends():
    print(f.name,f.sex)
    print("1111111")
    if f.sex == 1:
        man += 1
    elif f.sex == 2:
        woman += 1
    else:
        unknown += 1


# 调用绘图模块生成一个html  pyecharts 中包含很多种图标模块  按需导入
# 创建对象
pie = Pie("好友性别性别统计")
# 添加数据
pie.add("详情",["男性","女性","未知"],[man,woman,unknown],is_label_show=True)
path = os.path.join(os.path.dirname(__file__),"性别统计.html")
pie.render(path)

# 调用浏览器打开

webbrowser.open(path)












