#!/usr/bin/env python3

import sys
import html
import locale
import configparser

import fbget
#import twget

locale.setlocale(locale.LC_ALL,'it_IT.UTF-8')

def generatepost(post):
    newpost = post.copy()
    newpost['time'] = post['time'].strftime('%a %d %b %H:%M')
    if post['image'] is None:
        newpost['imagecode'] = ""
    else:
        newpost['imagecode'] = "<img src=\""+post['image']+"\" alt=\"Post image\">" 
    if post['author_pic'] is None:
        newpost['author_piccode'] = ""
    else:
        newpost['author_piccode'] = "<img src=\""+post['author_pic']+"\" alt=\"{author_name} profile picture\">"
    newpost['escapedtext'] = html.escape(post['text'][:320]).replace('\n','<br>')
    return """<div class="bs-callout bs-callout-primary">
		<div class="flex-horizontal">
			<h4>{author_piccode}{author_name}</h4>
			<div style="color: grey">{time}</div>
		</div>
			<p>{escapedtext}{imagecode}</p>
	</div>""".format(**newpost)


def main():
    config = configparser.ConfigParser()
    config.read('genconfig.ini')
    fbkey = config['facebook']['access_token']
    posts = []
    posts += fbget.get(fbkey)
    # posts += twget.get(twkey)
    sorted_posts = sorted(posts,key = lambda post: post['time'])
    sorted_posts.reverse()
    sorted_posts = sorted_posts[0:10]
    
    htmlcode = ""
    htmlcode += """<!DOCTYPE html>
<html>
<head>
	<title>Social network posts for Collegio Timpano</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta http-equiv="refresh" content="60" >

	<link rel="stylesheet" href="bootstrap.css" type="text/css"/>
	<link rel="stylesheet" href="bs-callout.css" type="text/css"/>
	<link rel="stylesheet" href="style.css" type="text/css"/>
	
</head>
 
<body style="background-color: transparent;">
  
<div class="container">
	<div style="color: #ccccff;">
		<h3 class="text-center" style="margin-bottom: 0px">Collegio Timpano @ social</h3>
		<h6 class="text-center" style="margin-top: 0px; margin-bottom: 0px;">by Enrico Polesel</h6>
	</div>"""

    for post in sorted_posts:
        htmlcode+=generatepost(post)

    htmlcode += """<h6 class="footer navbar-fixed-bottom">
	Page generated with <a href="http://github.com/epol/socialsignage/">socialsignage</a>, a GPL licensed software written by <a href="http://uz.sns.it/~enrico/">Enrico Polesel</a>.
	</h6>

</div>
    
</body>
</html>"""

    outfile = open('feed.html','wb')
    outfile.write(htmlcode.encode('utf-8'))
    outfile.close()









if __name__ == "__main__":
    main()


