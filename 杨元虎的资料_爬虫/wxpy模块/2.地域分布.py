"""

"""
import wxpy
import pyecharts
# weichat  = wxpy.Bot(cache_path=True)
#
# friends = weichat.friends()
#
# # province 表示省份
# dictc = {}
#
# for f in friends:
#     if f.province not in dictc:
#         dictc[f.province] = 1
#     else:
#         dictc[f.province] += 1
#
# # 创建地图对象
# map = pyecharts.Map("地域",width=1000,height=500)
#
# map.add("地域",dictc.keys(),dictc.values())
#
# map.render("map.html")



wx = wxpy.Bot()
provincedic = {}

for f in wx.friends():
    if f.province in provincedic:
        provincedic[f.province] += 1
    else:
        provincedic[f.province] = 1
map = pyecharts.Map("好友地域分布")
map.add("地域分布",provincedic.keys(),provincedic.values(),is_visualmap=True)
map.render("map.html")




