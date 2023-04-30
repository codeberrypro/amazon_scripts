import time
import gspread
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from seleniumwire import webdriver as wire_driver


LINK_ORDER = 'https://sellercentral.amazon.com/orders-v3/order/'
PHONE_COMPANY = '18049640370'
QT = 1
COMPANY = ' WhiteLilyStore'  # use this if not specified for individual accounts
URL_AUTHORIZATION = 'https://sellercentral.amazon.com/ap/signin?openid.return_to=https%3A%2F%2Fsellercentral.amazon.' \
                    'com%2Forders-v3%2Forder%2F113-8041991-3543406&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fa' \
                    'uth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_na_amazon_v2&openid.mode=checkid_setup&ope' \
                    'nid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A' \
                    '%2F%2Fspecs.openid.net%2Fauth%2F2.0&mons_redirect=sign_in&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiO' \
                    'iJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.X_9GyMvWbWamxCL6VBFyzbrdnhlRfb5jz9woie3o3Jt2M8cDoURRdA.8CjjJ' \
                    '5CJyBPezQVb.fCj92UF-dYSV_KCIZrbCDZQs_xKIJKH34t1iXbNUgwCerTCAsks5BCBmiSNaz28sf-KieC-WMj4gAGQAlLJ' \
                    'lltBQJgd_OW_8n30zkAarjrzAnULGNXpEUlEuEOdnH0Pv_fRoIGqPNT6IBspV-j1xpG9BvcEfJxKe2XPYeCl1wn90NWKy2w' \
                    'qXcBX7Lxm_jBVv4H5KQanyGWrCs-37sJBmmGc3U7TbdvygoH62otIgC41j0Z0v_6SZ0ffAs-uekLkkFgFM.p0Z69TBgDnuu' \
                    'tCXfIAi1jA'


def initialize_gspread_api():
    '''
    Initializes the Google Sheets API and returns the worksheet object to write data to.
    '''
    gc = gspread.service_account(filename='sheet.json')  # service account file name
    sh = gc.open_by_key('1UHUJt2guYcXtUF-FU7L7k7y1TKbxTRwZW8AYvCn5bTE')  # Google Sheets ID
    worksheet = sh.worksheet('testlist')  # worksheet name
    return worksheet


def initialize_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Mobile Safari/537.36")

    # Set Webdriver options for fingerprint stealth using the Stealth module
    stealth_options = {
        "languages": ["en-US", "en"],
        "vendor": "Google Inc.",
        "platform": "Win32",
        "webgl_vendor": "Intel Inc.",
        "renderer": "Intel Iris OpenGL Engine",
        "fix_hairline": True,
    }
    chrome_options = stealth.chromedriver().webdriver.ChromeOptions().merge(chrome_options)
    chrome_options = stealth.add_options(chrome_options, **stealth_options)

    return webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)


def main():
    driver_initialize = initialize_driver()
    initialize_gspread = initialize_gspread_api()


if __name__ == '__main__':
    main()


