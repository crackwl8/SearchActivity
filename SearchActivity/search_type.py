#coding:utf-8
"""
归纳资源链接,实际需要的只是活动和商品详情链接，但是爬时不知从哪些页面可以进入活动页和详情页
暂时先排除已知的页面
"""
PH_TYPES = [
    '',
]

TMALL_DESC = [
    u'新品促销',
    u'冲量促销',
    u'活动促销',
    u'火热促销',
    u'促销活动',
    u'优惠促销',
    u'满减',
    u'满*减',
    u'满*折',
    u'抢购价',
    u'促销价',
    u'卖家优惠',
    u'特惠',
    u'聚划算',
    u'抢',
]

TMALL_EXCEPT_DOMAIN = [
    'cart.tmall.com',
    'b.tmall.com',
    'login.tmall.com',
    'login.taobao.com',
    'err.taobao.com',
    'register.tmall.com',
    'vip.tmall.com',
    'service.tmall.com',
    'rule.tmall.com',
    'pass.tmall.com',
    'pages.tmall.com/wow/seller',
    'pages.tmall.com/wow/member-club',
    'discussion.htm',
    'alipay.com',
    'alicdn.com',
    'helpcenter.tmall.com',
    'mymy.maowo.tmall.com',
    'guize.tmall.com',
    'peixun.tmall.com',
    'e56.tmall.com',
]

JD_DESC = [
    u'促　　销',

]

JD_EXCEPT_DOMAIN = [
    'cart.jd.com',
    'passport.jd.com',
    'help.jd.com',
    'club.jd.com',
    'register.jd.com',
    'vip.jd.com',
    'baitiao.jd.com',
    'licai.jd.com',
    'b.jd.com',
    'o.jd.com',
    'z.jd.com',
    'train.jd.com',
    'order.jd.com',
    'game.jd.com',
    'movie.jd.com',
    'zhaopin.jd.com',
    'jr.jd.com',
    'surveys.jd.com',
    'xinren.jd.com',
    'jimi.jd.com',
    'jimi1.jd.com',
]

AMAZON_DESC = [
    u'促销信息',
    u'You Save:',
]

AMAZON_EXCEPT_DOMAIN = [
    'www.amazon.com/b/',
    'www.amazon.com/gp/help/',
    'www.amazon.com/gp/BIT/',
    'www.amazon.com/gp/orc/',
    'www.amazon.com/gp/ap/',
    'www.amazon.cn/gp/registry',
    'www.amazon.cn/gp/cart',
    '/uedata/unsticky/',
    'www.amazon.cn/gp/redirect.html',
    'www.amazon.cn/kindle-dbs/hz/signup',
    'www.amazon.cn/ap/signin',
]
