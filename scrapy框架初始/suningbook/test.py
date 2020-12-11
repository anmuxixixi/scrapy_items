# -*- coding = utf-8 -*-
# @Time：2020-12-01 23:18
# @Author：来瓶安慕嘻
# @File：test.py
# @开始美好的一天吧 @Q_Q@

import re

a = {'author': '\n'
           '\t\t\t\t\t\t    \t无著\n'
           '\t\t\t\t\t\t    \t\n'
           '\t\t\t\t\t\t    \t\n'
           '\t\t\t\t\t\t    \t\n'
           '\n'
           '\t\t\t\t\t\t    ',
 'big_cate': '经管励志',
 'detail_href': 'https://product.suning.com/0070418556/10657854848.html',
 'small_cate': '励志与成功',
 'small_href': 'https://list.suning.com/1-502298-0.html',
 'title': '月亮与六便士毛姆原著正版 文学社科书 世界名著初中生高中生必读经典课外书籍中学生月亮和六便士适合阅读的外国中外\n'}

text = 'ogj jopp kpjopjopgk po'
if 'apple' not in text:
    print('不存在')