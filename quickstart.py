from scrapy import cmdline

# import multiprocessing
# import time
#
#
# def process(num):
#     time.sleep(num)
#     cmdline.execute("scrapy crawl searchActivitySpider".split())
#     print 'Process:', num
#
#
# if __name__ == '__main__':
#     for i in range(multiprocessing.cpu_count()):
#         p = multiprocessing.Process(target=process, args=(i,))
#         p.start()
#
#     print('CPU number:' + str(multiprocessing.cpu_count()))
#     for p in multiprocessing.active_children():
#         print('Child process name: ' + p.name + ' id: ' + str(p.pid))
#
#     print('Process Ended')

cmdline.execute("scrapy crawl searchActivitySpider".split())
