# twitter-threads-blog

Generate a blog from your twitter threads.

## Usage

Start by cloning the repository.

Configuration is done in `threads.yml`. List the threads (top level tweet id, you can find it in the URL) you want in your blog, an optionnal title, and fill in your twitter handle.

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

You can change the title of the blog here https://github.com/abulte/twitter-threads-blog/blob/ebe28662f8c06f77b93d4ab12d7677c083fd265c/blog/.vuepress/config.js#L18.

The homepage is customizable here https://github.com/abulte/twitter-threads-blog/blob/master/blog/index.md.

The templates used to generate the markdown files are here https://github.com/abulte/twitter-threads-blog/tree/master/templates.

A github action workflow is included, if you push to github you should have your site automatically deployed and available through github pages. There is a few things you new to setup first:
- Apply for a twitter dev account: https://developer.twitter.com/en
- Create a twitter app and get API key and secret
- Fill those in your github repo as secrets called `TWITTER_KEY` and `TWITTER_SECRET` in an environment called `prod`

## Development

Python side, handle thread parsing and conversion to markdown. Needs `TWITTER_KEY` and `TWITTER_SECRET` env vars set (see above).

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

## TODO

- commit generated markdown for safe keeping and cache handling (beware of conflicts mayhem when running the job on github actions)
- use metadata parser for external urls (card/embed)
- handle tweet links (use urls[].expanded_url.startswith('twitter.com') and use embed)
- handle mentions and hashtags
