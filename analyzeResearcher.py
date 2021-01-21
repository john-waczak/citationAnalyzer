import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json  # for saving data
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome("./drivers/chromedriver")
pathToDrLary = "https://scholar.google.com/citations?user=gqR4v14AAAAJ"


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True





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
    author_summary["name"] = ""

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
    author_summary["hindex"] = ''
    print(e)

i10_xpath = '//*[@id="gsc_rsb_st"]/tbody/tr[3]/td[2]'
try:
    i10_search = driver.find_element_by_xpath(i10_xpath)
    i10_index = int(i10_search.get_attribute("innerHTML"))
    print("i10-index: {0}".format(i10_index))
    author_summary["i10 index"] = i10_index
except Exception as e:
    print(e)
    author_summary["i10 index"] = ''

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
    years_soup = BeautifulSoup(years.get_attribute("innerHTML"), features="html.parser")

    citation_years =  [int(year.text) for year in years_soup.find_all('span', {"class": "gsc_g_t"})]
    citation_nums =  [int(num.text) for num in years_soup.find_all('span', {"class": "gsc_g_al"})]

    author_summary["citation years"] = citation_years
    author_summary["citation numbers"] = citation_nums

    plt.figure()
    plt.bar(citation_years, citation_nums, align='center', color='indigo')
    plt.xlabel('Year')
    plt.title("{0} Citations Per Year".format(author_summary["name"]))
    plt.savefig("./figures/citations_per_year.eps")

    # close histogram
    exit_xpath = '//*[@id="gsc_md_hist-x"]'
    exit_button = driver.find_element_by_xpath(exit_xpath)
    exit_button.click()

except Exception as e:
    print(e)
    author_summary["citation years"] = []
    author_summary["citation numbers"] = []




# Save summary dictionary to JSON file
with open('./json/summary_data.json', 'w') as fp:
    json.dump(author_summary, fp)

# click the body of the references to exit the graph
# try:
#     reference_list_body_id = 'gsc_a_b'
#     reference_list_body = driver.find_element_by_id(reference_list_body_id)
#     reference_list_body.click()
# except Exception as e:
#     print(e)


# Next we want to autogenerate the bibtex. To do that, let's first make json files for each reference
# first we find the div that contains the paper list
more_button_id = "gsc_bpf_more"
hasTableChanged = True
prev_length = 0
counter = 0
while hasTableChanged:
    more_button = driver.find_element_by_id(more_button_id)
    more_button.click()
    print("Clicked the 'more' button")
    # check to see if the table is longer
    table_id = 'gsc_a_b'
    table = driver.find_element_by_id(table_id)
    table_length = len(table.find_elements_by_tag_name('tr'))
    if counter > 0:
        if table_length == prev_length:
            hasTableChanged = False
    prev_length = table_length
    counter += 1
    time.sleep(0.5)


# Go through each publication and generate json with citation info
table_id = 'gsc_a_b'
table = driver.find_element_by_id(table_id)
table_rows = table.find_elements_by_tag_name('tr')

counter = 1
for row in table_rows:
    citation_json = {}

    link = row.find_element_by_xpath(".//td[1]/a")
    title = link.text
    print("Title: ", title)
    citation_json['title'] = title
    link.click()
    time.sleep(1)


    info_table_id = 'gsc_vcd_table'
    info_table = driver.find_element_by_id(info_table_id)
    table_soup = BeautifulSoup(info_table.get_attribute("innerHTML"), features="html.parser")
    divs = table_soup.find_all('div', {"class": "gs_scl"})

    field_list = ['Authors', 'Publication date', 'Journal', 'Volume', 'Issue', 'Pages', 'Publisher', 'Desciption']

    for div in divs:
        fields = div.find_all('div', {"class": "gsc_vcd_field"})
        vals = div.find_all('div', {"class": "gsc_vcd_value"})
        field = fields[0].text
        val = vals[0].text
        if field in field_list:
            print("\t", field)
            citation_json[field] = val


    # now save the json file
    with open('./json/paper_info/paper{}.json'.format(counter), 'w') as fp:
        json.dump(author_summary, fp)

    counter += 1


    # close the window
    exit_id = 'gs_md_cita-d-x'
    exit_button = driver.find_element_by_id(exit_id)
    exit_button.click()
    time.sleep(2)




# Close the browser
# driver.quit()
