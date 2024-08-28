from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time



def save_cookies_in_netscape_format(driver, file_path):
    cookies = driver.get_cookies()
    
    # Netscape format header
    netscape_cookies = [
        "# Netscape HTTP Cookie File",
        "# This is a generated file! Do not edit.",
    ]
    
    # Format the cookies for Netscape format
    for cookie in cookies:
        domain = cookie['domain']
        include_subdomain = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = cookie['path']
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiration = cookie.get('expiry', 0)
        name = cookie['name']
        value = cookie['value']
        
        # Append the cookie in Netscape format
        netscape_cookies.append(
            f"{domain}\t{include_subdomain}\t{path}\t{secure}\t{expiration}\t{name}\t{value}"
        )
    
    # Write the cookies to the file
    with open(file_path, 'w') as f:
        f.write("\n".join(netscape_cookies))




def main():
    while True:
        print("start")
        geckodriver_path = '/usr/local/bin/geckodriver'
        options = Options()
        options.add_argument("--headless")

        service = Service(geckodriver_path)

        driver = webdriver.Firefox(service=service, options=options)

        driver.get("https://youtube.com")

        time.sleep(10)

        save_cookies_in_netscape_format(driver, "cookies.txt")
        driver.close()
        print("done")
        time.sleep(60)
        


if __name__ == "__main__":
    main()
