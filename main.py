import filemoon
from threading import Thread

filemoon.headless = False
filemoon.isCheckIp = True
filemoon.wait_start = 5
filemoon.wait_end = 20
filemoon.duration = 5
filemoon.with_proxy = False
loops = 3
browser = 2


def headless_input():
    headless = input("Hide the browser(y/n) : ")
    headlesss = headless.lower()

    if headlesss == "y":
        filemoon.headless = True
    elif headlesss == "n":
        filemoon.headless = False
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        headless_input()


def isCheckIp_input():
    isCheckIp = input("Wanna check the ip(y/n) : ")
    isCheckIpp = isCheckIp.lower()

    if isCheckIpp == "y":
        filemoon.isCheckIp = True
    elif isCheckIpp == "n":
        filemoon.isCheckIp = False
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        isCheckIp_input()


def isProxy_input():
    proxy = input("Wanna use proxy(y/n) : ")
    proxyy = proxy.lower()

    if proxyy == "y":
        filemoon.with_proxy = True
    elif proxyy == "n":
        filemoon.with_proxy = False
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        isProxy_input()


def is_number(input_str, input_str1):
    try:
        float(input_str)  # Try converting the input to a float
        float(input_str1)  # Try converting the input to a float
        return True  # Return True if successful
    except ValueError:
        return False  # Return False if ValueError occurs


def wait_input():
    wait_start = input("Enter start time to wait after watch video (seconds) : ")
    wait_end = input("Enter end time to wait after watch video (seconds) : ")

    if is_number(wait_start, wait_end):
        if int(wait_start) > int(wait_end):
            print("wait start must be lower than wait end")
            wait_input()
        else:
            filemoon.wait_start = int(wait_start)
            filemoon.wait_end = int(wait_end)
    else:
        print("Invalid input. Please number in second")
        wait_input()


def duration_input():
    durations = input("Enter the video duration (seconds) : ")

    if is_number(durations, 0):
        filemoon.duration = int(durations)
    else:
        print("Invalid input. Please number in second")
        duration_input()


def loop_input():
    loop = input("How many times you wanna watch (number) : ")
    global loops
    if is_number(loop, 0):
        loops = int(loop)
    else:
        print("Invalid input. Please input number")
        loop_input()


def browser_input():
    browsers = input("How many thread you wanna use (number) : ")
    global browser

    if is_number(browsers, 0):
        browser = int(browsers)
    else:
        print("Invalid input. Please input number")
        browser_input()


threads = []
success = 0
failed = 0
revenue = 0.003
stop = True
proxy = []


def run():
    try:
        headless_input()
        isCheckIp_input()
        isProxy_input()
        # wait_input()
        duration_input()
        loop_input()
        browser_input()

        with open("proxy.txt", "r") as file:
            proxy = file.read().splitlines()

        proxy_picker = len(proxy) - 1
        current_proxy = 0

        # wrapper to catch thread error
        def filemoon_func(current_proxy):
            try:
                filemoon.main(current_proxy)
            except Exception as e:
                if "unknown error: net::ERR_PROXY_CONNECTION_FAILED" in str(e):
                    print("proxy error occured ")
                else:
                    print("An error occurred in thread")

        # run the thread
        for n in range(loops):
            print("current proxy : ", proxy[current_proxy])

            for i in range(browser):
                # thread = Thread(target=browser_main_wrapper, args=(i,))
                thread = Thread(target=filemoon_func, args=(current_proxy,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete before moving to the next iteration
            for thread in threads:
                thread.join()

            # pick proxy sequential from proxy list
            if current_proxy == proxy_picker:
                current_proxy = 0
            else:
                current_proxy = current_proxy + 1

    except Exception as e:
        print("error occured in main file : ", e)
    finally:
        print("Filemoon Bot views done")


if __name__ == "__main__":
    run()
