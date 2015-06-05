from selenium import webdriver

webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Pipiska/37.0"
webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Connection'] = "keep-alive"
driver = webdriver.PhantomJS()
driver.get('http://httpbin.org/headers')


print(driver.page_source)