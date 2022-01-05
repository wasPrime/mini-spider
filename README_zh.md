# mini-spider

一个能够实现对种子链接的广度优先抓取的小型爬虫。

抓取到的符合特定 URL 规则的网页保存到 output 文件夹中。

## 运行

```bash
python mini_spider.py -c spider.conf
```

## 配置文件 - spider.conf

```ini
[spider]
url_list_file: urls # 种子文件路径
output_directory: output # 抓取结果存储目录
max_depth: 1 # 最大抓取深度（种子为0级）
crawl_interval: 1 # 抓取间隔. 单位: 秒
crawl_timeout: 1 # 抓取超时. 单位: 秒
target_url: (https?|ftp|file)://[-A-Za-z0-9+&@#/%%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%%=~_|]
thread_count: 8 # 抓取线程数
```

## 种子文件

种子文件的每行为一条链接，例如:

- <http://www.baidu.com>
- <http://www.sina.com.cn>

## 特点

- 支持命令行参数处理。具体包含: `-h(帮助)`、`-v(版本)`、`-c(配置文件)`。
- 单个网页抓取或解析失败，不会导致整个程序退出，在日志中记录下错误原因并继续。
- 当程序完成所有抓取任务后，优雅退出。
- 从 HTML 提取链接时处理相对路径和绝对路径。
- 能够处理不同字符编码的网页（例如 utf-8 或 gbk）。
- 网页存储时每个网页单独存为一个文件，以 URL 为文件名。对 URL 中的特殊字符有转义操作。
- 支持多线程并行抓取。
