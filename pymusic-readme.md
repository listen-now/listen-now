# 关于pymusic版本的使用指南

  * 首先安装Python3, 并做好软连接(各种办法均可)

  * 使用 git clone https://github.com/import-yuefeng/Listen-now 

  * 运行初始化程序 python3 setup.py

  * 尝试在终端输入 # pymusic -h 来尝试是否可用

### 关于终端版本(pymusic)使用说明

```
# pymusic -h(显示所有的帮助信息)
```    
```
usage: pymusic [-h] [-t TITLE] [-p PLATFORM] [-id ID] [-n NUM] [-page PAGE]

optional arguments:
 -h, --help   show this help message and exit

 -t TITLE       like: 白金迪斯科
 -p PLATFOR     like: 网易(net)/QQ(qq)/虾米(xia)
 -id ID,        like 123456
 -n NUM,        like 1
 -page PAGE     like 1

```

   # pymusic -t(歌曲名字)  -p(歌曲平台)

    pymusic -t 纸短情长 -p net


```    0    纸短情长（完整版）    烟把儿
1    纸短情长    烟把儿
2    纸短情长    花粥
3    纸短情长    仇志
4    纸短情长（Cover 烟把儿）    杨舒怀
5    纸短情长（Cover 烟把儿）    萧忆情Alex
6    纸短情长（Cover：烟把儿）    冯心怡
7    纸短情长（Cover：烟把儿）    尚士达
8    纸短情长（Cover 烟把儿）    叶洛洛
9    纸短情长（试听版）    烟把儿
10    >>>Enter your select 

```
   * 键入w来上翻一页, s为下翻一页被选歌曲
   * 键入歌曲前面的序号来播放歌曲
   * -p 目前可选如下 net/网易、qq(QQ音乐)、xia(虾米音乐)

如果你有歌曲id, 可直接准确播放歌曲

```
# pymusic -id 123456 -p net
```    

如果你选了一首不喜欢的歌曲, 请直接使用Ctrl + c 来选择输入检索新歌曲

```
     # pymusic -sl 123456(歌单id) -p net

     # pymusic -uid 123456(用户id) -p net

     通过 -uid 你可以得到该用户的所有歌单, 并可以选择其中的歌单进行播放
     通过 -sl 系统会自动为您播放该歌单的音乐, 听歌过程中想切换下一首歌, 请输入Ctrl + c

```    

