from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json  # for saving data
from bs4 import BeautifulSoup

driver = webdriver.Chrome("./drivers/chromedriver")
pathToDrLary = "https://scholar.google.com/citations?user=gqR4v14AAAAJ"



# Navigate to google scholar
driver.get(pathToDrLary)
driver.maximize_window()

# Generate Summary
author_summary = {}
author_element_id = "gsc_prf_in"
try:
    name_search = driver.find_element_by_id(author_element_id)
    name = name_search.text
    print("name: {0}".format(name))
    author_summary["name"] = name

except Exception as e:
    print(e)


# total_citation_xpath ="/html/body/div/div[13]/div[2]/div/div[1]/div[1]/table/tbody/tr[1]/td[2]"
total_citation_xpath ='//*[@id="gsc_rsb_st"]/tbody/tr[1]/td[2]'
try:
    tot_citation_search = driver.find_element_by_xpath(total_citation_xpath)
    tot_citations = int(tot_citation_search.get_attribute("innerHTML"))
    print("total ciations: {0}".format(tot_citations))
    author_summary["total citations"] = tot_citations
except Exception as e:
    print(e)


hindex_xpath = '//*[@id="gsc_rsb_st"]/tbody/tr[2]/td[2]'
try:
    hindex_search = driver.find_element_by_xpath(hindex_xpath)
    hindex = int(hindex_search.get_attribute("innerHTML"))
    print("h-index: {0}".format(hindex))
    author_summary["hindex"] = hindex
except Exception as e:
    print(e)

i10_xpath = '//*[@id="gsc_rsb_st"]/tbody/tr[3]/td[2]'
try:
    i10_search = driver.find_element_by_xpath(i10_xpath)
    i10_index = int(i10_search.get_attribute("innerHTML"))
    print("i10-index: {0}".format(i10_index))
    author_summary["i10 index"] = i10_index
except Exception as e:
    print(e)

# get historical ciation histogram data:
hist_button_id='gsc_hist_opn'
try:
    # open the histogram
    hist_button = driver.find_element_by_id(hist_button_id)
    view_all = hist_button.find_element_by_class_name('gs_lbl')
    view_all.click()

    hist_body_id = 'gsc_md_hist-bdy'
    hist_body = driver.find_element_by_id(hist_body_id)
    years = hist_body.find_element_by_xpath(".//div/div[3]/div")
    years_soup = BeautifulSoup(years.get_attribute("innerHTML"))

    citation_years =  [int(year.text) for year in years_soup.find_all('span', {"class": "gsc_g_t"})]
    citation_nums =  [int(num.text) for num in years_soup.find_all('span', {"class": "gsc_g_al"})]

    author_summary["citation years"] = citation_years
    author_summary["citation numbers"] = citation_nums


except Exception as e:
    print(e)
