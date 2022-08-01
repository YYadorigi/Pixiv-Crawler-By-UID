# Pixiv UID Crawler

一个简单的Pixiv插画爬虫。根据画师的uid，爬取其主页上的全部作品。

*（仅供学习交流用途，请勿传播图片、尝试 ~~[数据删除]~~ 等不适宜行为，违者自负。）*

</br>

# 安装

运行以下命令以创建适配的虚拟环境：

```
conda create -n <env_name> python=3.8
```

</br>

运行以下命令安装依赖：

```
pip install -r requirements.txt
```

</br>

# 配置

请将仓库中的 `template_settings.json` 改名为 `pixiv_settings.json`，

然后依照实际情况如下填写 `pixiv_settings.json` 文件：

</br>

- 必须自行填写的项为：

  `cookie`，`user-agent`，`http`，`https`，`uid`；
  
  </br>
  
- 可以自行修改的项为：

  `interval_between_user`：每爬取不同uid之间的时间间隔（单位：秒），

  `interval_between_download`：每次下载之间的时间间隔（单位：秒）；

  *（警告：不建议将后者设置得过短，过于频繁的访问存在封IP的风险。）*
  
  </br>

- 不可修改的项为：

  `referer`：pixiv 主址。
  
  </br>

```
{
    "headers": {
        "cookie": "你的COOKIE",
        "user-agent": "你所需使用的用户代理",
        "referer": "https://www.pixiv.net/"
    },
    "proxies": {
        "http": "你的http代理",
        "https": "你的https代理"
    },
    "config": {
        "interval_between_user": 100,
        "interval_between_download": 2
    },
    "uid": [
        画师的uid，
        不同uid之间换行并用逗号隔开，
        最后一行后不加逗号
    ]
}
```

</br>

# 文件说明

- `pixiv_crawler.py`：主程序。执行该程序以运行本爬虫。
- `pixiv_settings.json`：配置文件。
- `pixiv_crawler.log`：运行主程序后**自动生成**的日志文件，记录日志输出。
- `pixiv_illusions`：运行主程序后**自动生成**的目录，按照作者 ID 分目录存放图片。
- `requirements.txt`：虚拟环境的依赖包。

</br>

# 使用

1. 配置好 `pixiv_settings.json` 后，直接在虚拟环境下运行 `pixiv_crawler.py` 即可。
2. 运行过程中，程序会自动在本目录下创建 `pixiv_illlusions` 目录，并在该目录下对每个作者的 ID 新建一个子目录，以存放该作者的所有作品。
3. 终端和日志文件中会实时跟进爬虫运行情况。用户可在 `pixiv_crawler.log` 中查看详情。

</br>
