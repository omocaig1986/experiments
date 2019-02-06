from multi_get import multi_get
sites = ['http://msn.com/', 'http://yahoo.com/', 'http://google.com/']
requests = multi_get(sites, timeout=1.5)

for url, data in requests:
    print "received this data %s from this url %s" % (url, data)
