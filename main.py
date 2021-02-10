from selenium import webdriver
from yaml import load, FullLoader
from io import open
from getpass import getpass

yaml_data = None
with open("data.yaml", 'r') as stream:
    yaml_data = load(stream, Loader=FullLoader)

# Get the input
uname = yaml_data['username']
if uname is None:
    uname = input("Enter your student number: ")
    uname = str.lower(uname)

pwd = yaml_data['password']
if pwd is None:
    pwd = getpass(prompt='Pasword: ')

homedir = yaml_data['homeDir']
if homedir is None:
    homedir = input("Enter themis dir: ")

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
driver.get(homedir)

# If you have to login
if len(driver.find_elements_by_xpath("//*[contains(text(), 'Log in')]")) != 0:
    # Send the credentials
    username = driver.find_element_by_name("user")
    username.clear()
    username.send_keys(uname)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(pwd)

    # Press the Login button
    driver.find_element_by_xpath("//*[@type='submit']").click()

    if len(driver.find_elements_by_xpath("//*[contains(text(), 'Log in')]")) != 0:
        print("Login failed! This may also be due to slow internet connection")
        exit(1)

print("Successfully logged in")
forwardDir = yaml_data['forwardDir']
if forwardDir is None:
    forwardDir = input("Enter the page where it should be uploaded: ")

files = yaml_data['files']
if files is None:
    files = input("Select the files which should be uploaded (sep. space): ")

files = str.split(files, " ")

# wait for command
command = input("Command (push+submit, push, submit, exit, rego): ")

while command != "exit":

    if command == "push+submit":
        # First rego to page
        driver.get("https://themis.housing.rug.nl/course/2020-2021/adinc-cs/tutorial-exercises/chapter1/Exercise%201.8")

        # Commit files
        for file in files:
            element = driver.find_element_by_id("upload-0")
            element.send_keys(file)

        # And push ;)
        driver.find_element_by_id("btnUpload").click()
    elif command == "rego":
        # First rego to page
        driver.get("https://themis.housing.rug.nl/course/2020-2021/adinc-cs/tutorial-exercises/chapter1/Exercise%201.8")
    elif command == "push":
        # Commit files
        for file in files:
            element = driver.find_element_by_id("upload-0")
            element.send_keys(file)

    elif command == "reload":
        forwardDir = yaml_data['forwardDir']
        files = yaml_data['files']

    elif command == "submit":
        # And push ;)
        driver.find_element_by_id("btnUpload").click()

    else:
        print("Command unknown")

    # wait for command
    command = input("Command (push+submit, push, submit, exit, rego, reload): ")


driver.close()
