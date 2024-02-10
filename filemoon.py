from selenium import webdriver
import time
import random


# variables
wait_start = 1
wait_end = 5
duration = 2
iphub = "https://iphub.info/"
isCheckIp = True
# drivers = []
headless = False
with_proxy = False
is_sequential = False


def browser_actions(driver, url):
    xpath_iphub = '//*[@id="hostname"]'
    xpath_country = '//*[@id="countryName"]'
    xpath_type = '//*[@id="type"]'
    xpath_play = '//*[@id="vplayer"]/div[2]/div[12]/div[1]/div/div/div[2]/div'

    if wait_start == wait_end:
        wait_time = wait_start
    else:
        wait_time = random.randrange(wait_start, wait_end)

        try:
            # check your ip
            if isCheckIp:
                driver.get(iphub)
                time.sleep(10)

                element_ip = driver.find_element("xpath", xpath_iphub)
                element_country = driver.find_element("xpath", xpath_country)
                element_type = driver.find_element("xpath", xpath_type)

                ip = element_ip.text
                country = element_country.text
                type = element_type.text

                print("Your IP is :", ip)
                print("Your country is :", country)
                print("Your IP type is :", type)

            print(f"menuju alamat video : {url}")
            print("")
            driver.get(url)

            button = driver.find_element("xpath", xpath_play)
            button.click()

            # close iklan
            # Get the handles of all open windows
            all_window_handles = driver.window_handles

            # Switch to the second window (index 1 in 0-based indexing)
            driver.switch_to.window(all_window_handles[1])

            # Close the second window
            driver.close()

            # Switch back to the main window
            driver.switch_to.window(all_window_handles[0])

            print("Memutar video di browser ", driver)
            time.sleep(duration)

            print("selesai memutar video, menunggu driver menutup")
            time.sleep(wait_time)
            driver.quit()

        except Exception as e:
            raise


def browser(index_proxy):
    if with_proxy:
        # Read proxy from the text file
        with open("proxy.txt", "r") as file:
            proxys = file.read().splitlines()

        # pilih proxy yang ingin dibuka
        if is_sequential:
            print("Using proxy : ", proxys[index_proxy])
            http_proxy = f"socks5://{proxys[index_proxy]}"
        else:
            proxy_picker = random.randrange(0, len(proxys) - 1, 1)
            print("Using proxy : ", proxys[proxy_picker])
            http_proxy = f"socks5://{proxys[proxy_picker]}"

    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    else:
        chrome_options.add_argument("--window-size=0,0")
    if with_proxy:
        chrome_options.add_argument(f"--proxy-server={http_proxy}")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")

    # Create WebDriver instances for each browser
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def main(index_proxy):
    while True:
        try:
            driver = browser(index_proxy)

            # Read URLs from the text file
            with open("filemoon.txt", "r") as file:
                urls = file.read().splitlines()

            # pilih link yang ingin dibuka
            url_picker = random.randrange(0, len(urls) - 1, 1)

            # do action with the browser
            browser_actions(driver, urls[url_picker])
            break

        except Exception as e:
            # old error logic
            # if "unknown error: net::ERR_PROXY_CONNECTION_FAILED" in str(e):
            #     print("proxy error occured ")
            #     # print("change proxy server ")
            #     # driver = browser()
            #     # browser_actions(driver, url)

            #     # error = True
            #     # index_proxys = index_proxys + 1
            #     time.sleep(5)
            #     continue
            # else:
            #     raise
            raise
        # break
