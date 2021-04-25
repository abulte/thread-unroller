# twitter-threads-blog

Generate a blog from your twitter threads.

Configuration is done in `threads.yml`. List the threads (top level tweet id) you want in your blog, an optionnal title, and fill in your twitter handle.

```yml
author: abulte
threads:
  -
    id: 1385195772199714816
    title:
  -
    id: 1381281294865272833
    title:
```

## Development

Python side, handle thread parsing and conversion to markdown.

```shell
pip install -r requirements.txt
# unthread everything from threads.yml
python unthread.py bulk
# or just unthread a specific thread
python unthread.py process https://twitter.com/abulte/status/1381281294865272833
```

Javascrip side, handles static blog generation from markdown.

```shell
yarn
yarn dev
```

👉 http://localhost:8080/twitter-threads-blog/threads/
