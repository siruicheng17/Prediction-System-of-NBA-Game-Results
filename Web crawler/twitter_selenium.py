from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver import ChromeOptions, DesiredCapabilities

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('disable-infobars')
# option.add_argument("--proxy-server={}".format(bb))

# user_agent = random.choice(user_agents)
# # specify headless mode
option.add_argument('--headless')
# # specify the desired user agent
# option.add_argument(f'user-agent={user_agent}')
# driv = webdriver.Chrome(options=option)
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
# Pop-up windows are prohibited.
option.add_experimental_option('prefs', prefs)




def get_driver():
    driver = webdriver.Chrome(options=option)
    return driver


def dealUrl(base, url):
    if url.startswith('javascript'):
        return None
    url = url.split('#')[0]
    if not url.startswith(('http:', 'https:')):
        url = urljoin(base, url)
    return url.strip('/')


def get_url_info(i, driver):
    driver.maximize_window()
    driver.get(i)
    content = driver.page_source
    time.sleep(10)
    # with open("aaa.html",'a',encoding="utf-8") as fw:
    #     fw.write(content)
    cookies = driver.get_cookies()
    for i in cookies:
        print(i)
        if i['name'] == 'gt':
            print(i['value'])
            with open('token.txt', 'w') as f:
                f.write(i['value'])
    driver.close()

if __name__ == '__main__':
    from datetime import datetime
    import time
    # Execute every n seconds.
    while True:
        try:
            driver = get_driver()
            get_url_info("https://twitter.com/JoeBiden", driver)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(60)
        except Exception as e:
            print(e)



            # driver.quit()
