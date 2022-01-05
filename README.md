# mini-spider

A small crawler that can achieve breadth-first crawling of seed links.

The fetched web pages that meet the specific URL rules are saved in the output folder.

## Run

```bash
python mini_spider.py -c spider.conf
```

## Configuration file - spider.conf

```ini
[spider]
url_list_file: urls # Seed file path
output_directory: output # Capture result storage directory
max_depth: 1 # Maximum crawl depth (seed is level 0)
crawl_interval: 1 # crawl interval. Unit: seconds
crawl_timeout: 1 # crawl timeout. Unit: seconds
target_url: (https?|ftp|file)://[-A-Za-z0-9+&@#/%%?=~_|!:,.;]+[-A-Za-z0-9 +&@#/%%=~_|]
thread_count: 8 # Number of crawling threads
```

## Seed file

Each line of the seed file has a link, for example:

- <http://www.baidu.com>
- <http://www.sina.com.cn>

## Features

- Support command line parameter processing. Specifically include: `-h (help)`, `-v (version)`, `-c (configuration file)`.
- The failure of crawling or parsing a single webpage will not cause the entire program to exit. Record the cause of the error in the log and continue.
- When the program finishes all the crawling tasks, it exits gracefully.
- Handling relative and absolute paths when extracting links from HTML.
- Able to handle web pages with different character encodings (such as utf-8 or gbk).
- When storing web pages, each web page is saved as a file separately, and the URL is the file name. There is an escape operation for special characters in the URL.
- Supports multi-threaded parallel fetching.
