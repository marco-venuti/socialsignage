#!/usr/bin/env python3

import sys
import html

import fbget
#import twget

def generatepost(post):
    newpost = post.copy()
    newpost['time'] = post['time'].strftime('%a %d %b %H:%M')
    if post['image'] is None:
        newpost['imagecode'] = ""
    else:
        newpost['imagecode'] = "<img src=\""+post['image']+"\">" 
    if post['author_pic'] is None:
        newpost['author_piccode'] = ""
    else:
        newpost['author_piccode'] = "<img src=\""+post['author_pic']+"\" alt=\"{author_name} profile picture\">"
    newpost['escapedtext'] = html.escape(post['text'])
    return """<div id="post">
  <div id="post_header">
    <div id="author">
      {author_piccode}
      {author_name}
    </div>
    <div id="time">
      {time}
    </div>
  </div>
  <div id="body">
    <p>{escapedtext}</p>
    {imagecode}
  </div>
</div>
""".format(**newpost)


def main():
    fbkey = sys.argv[1]
    posts = []
    posts += fbget.get(fbkey)
    # posts += twget.get(twkey)
    sorted_posts = sorted(posts,key = lambda post: post['time'])
    sorted_posts.reverse()

    htmlcode = ""
    htmlcode += """<html>
  <head>
    <title>Social network posts for Collegio Timpano</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link rel="stylesheet" type="text/css" href="feed.css" />
  </head>
  <body>
    <div id="header">
      <h1>Collegio Timpano @ social</h1>
    </div>
"""

    for post in sorted_posts:
        htmlcode+=generatepost(post)

    htmlcode += """  </body>
</html>
"""
    outfile = open('feed.html','wb')
    outfile.write(htmlcode.encode('utf-8'))
    outfile.close()









if __name__ == "__main__":
    main()


