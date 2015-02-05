##Rip images from a Tumblr blog - asynchronously.

###Installation

```
$ git clone git@github.com:shivekkhurana/rip-tumblr.git
$ cd rip-tumblr
$ pip install -r requirements.txt
$ cp scraper.example.cfg scraper.cfg
$ vim scraper.cfg # add your blog here
$ mkdir crawled_data
$ python scraper.py
```

and let it rip.

Code inspired by this (https://gist.github.com/madjar/9312452) and this  (https://github.com/dinob0t/coffee_places/blob/master/v1_async_places.py) gist.