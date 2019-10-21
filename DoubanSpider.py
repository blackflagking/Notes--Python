# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import time
from lxml import etree


import io

url = 'https://movie.douban.com/subject/30413052/comments?start=%d&limit=20&sort=new_score&status=P'


headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'bid=hGPYYnU9JLM; __utmc=30149280; push_noty_num=0; push_doumail_num=0; dbcl2="196399371:puywehE7c/Q"; ck=8hwC; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1571563739%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; _pk_id.100001.8cb4=c12ba9042a841c39.1571563739.1.1571563739.1571563739.; _pk_ses.100001.8cb4=*; __yadk_uid=hTgwuCazczyCDCLv4G9BaerjQYdHKjxy; __utma=30149280.791093345.1571551187.1571553965.1571563744.3; __utmz=30149280.1571563744.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmt=1; __utmv=30149280.19639; __utmb=30149280.2.10.1571563744',
'Host':'movie.douban.com',
'Referer':'https://movie.douban.com/subject/30413052/',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'same-origin',
'Sec-Fetch-User':'?1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36}',}
if __name__ == '__main__':
    fp = io.open('./climb.csv', mode='w', encoding='utf-8')
    fp.write(unicode('author\tcomment\tvote\n'))
    for i in range(26):
        if i==25:
            url_climb=url%(50)
        else:
            url_climb =url%(i*2)
            print url_climb
        response = requests.get(url_climb, headers=headers)
        response.encoding = 'utf-8'
        text = response.text
        #
        # 打印网页文件
        print ('------------------打印网页文件------------')
        print (text)

        html = etree.HTML(text)
        comments = html.xpath("//div[@class='article']/div[@id='comments']/div[@class='comment-item']")

        for index, comment in enumerate(comments):
            print index

            # 爬取作者名
            auth_nu = '//div[@class="comment-item"][%d]/div[@class="avatar"]/a/@title' % (index + 1)
            author = html.xpath(auth_nu)[0].strip()
            print author

            # 爬取评论内容
            comm_nu = '//div[@class="comment-item"][%d]/div[@class="comment"]/p' % (index + 1)
            comm_text_sub = html.xpath(comm_nu)[0]
            comm_text = comm_text_sub.xpath('string(.)').strip()
            print comm_text

            # 爬取评论数
            vote_nu = '//div[@class="comment-item"][%d]/div[@class="comment"]/h3/span[@class="comment-vote"]/span[@class="votes"][1]/text()' % (index + 1)
            vote = html.xpath(vote_nu)[0]
            print int(vote)
            
            fp.write('%s\t%s\t%s\n' % (author, comm_text, vote))
            print('爬取成功第%d条--Bingo' % (index + 1))
            time.sleep(2)
        fp.close()
