SELECTMOVIE
===========

通过扫描本地电影文件名，生成电影介绍网页。

安装
-----

安装Python v2.7。
下载本项目到本地，修改`generate.py`文件中的`base_path`到电影收藏目录。

运行
-----

运行 `python generate.py` 生成本地数据文件，并生成[主页](index.html).
查看[主页](index.html)。
如果本地电影文件有增加，重复运行 `python generate.py`将以增量方式添加到本地数据文件，并重新生成[主页](index.html)。

约定
-----

电影文件按以下方式命名：

* A.Beautiful.Mind.2001.美丽心灵.双语字幕.mkv
* Cinema.Paradiso.DC.1988.天堂电影院.导演剪辑版.中文字幕.mkv

系统通过检查年份后紧跟的中文名来获取电影信息。

感谢
-----

感谢[豆瓣电影](https://movie.douban.com/)提供的[API接口](http://developers.douban.com/wiki/?title=api_v2)。

许可证
------

MIT
