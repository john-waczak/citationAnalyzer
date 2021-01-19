from selenium import webdriver

driver = webdriver.Chrome("./drivers/chromedriver")

# Navigate to google scholar
driver.get("https://scholar.google.com")
