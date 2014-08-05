import lxml.html
import urllib2
import sys

#url = 'http://kinhdoanh.vnexpress.net'
##u = urllib2.urlopen(url)
##data = u.read()
##
##f = open('auto_url.txt','wb')
##f.write(data)
##f.close()

max_url = 1500
url_list = []
#tree = lxml.html.parse(url)

#tags = tree.xpath('//div[@class = "title_news"]/a/@href')
url = 'http://vnexpress.net/tin-tuc/thoi-su/page/{}.html'
i = 1
j = 0
while(i < 2436):
    print i
    print len(url_list)
    next_url = url.format(i)
    try:
        tree = lxml.html.parse(next_url)
    except IOError:
        tree = lxml.html.parse(urllib2.urlopen(next_url))
    tags = tree.xpath('//div[@class = "title_news"]/a/@href')
    for link in tags:
        if link not in url_list:
            url_list.append(link)
        else:
            j += 1
    i += 1

train = '\n'.join(url_list[:1000])
test = '\n'.join(url_list[1000:])
    
f = open('total_url.txt','wb')
f.write(train)
f.write('\n#####\n')
f.write(test)
f.close()
