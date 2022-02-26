from pyecharts.charts import Bar

bar = Bar()
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
list1=[5, 20, 36, 10, 75, 90]
for o in range(25):
# bar.add_yaxis("商家A", list1)
    bar.add_yaxis("商家{}".format(o+1), [i*o for i in list1])
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render()