from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
labels_needed = ['description', 'chemical formula', 'type']


def check_if_drug_page():
    return '/drugs/' in driver.current_url


def get_drug_information(drug):
    print('Analyzing ' + drug['name'])
    data = {}
    driver.get('https://www.drugbank.ca/drugs')
    search_terms = drug['common_brands']
    page_found = False
    for term in search_terms:
        sub_search_terms = term.split()
        if len(sub_search_terms) == 1:
            sub_search_terms = sub_search_terms[0].split('-')
        if page_found:
            break
        for search in sub_search_terms:
            try:
                query = driver.find_element_by_id('query')
            except NoSuchElementException:
                time.sleep(30)
                driver.get('https://www.drugbank.ca/drugs')
                query = driver.find_element_by_id('query')
            query.send_keys(
                search)
            query.submit()
            if check_if_drug_page():
                page_found = True
                break
    if not page_found:
        return data
    data_container = driver.find_element_by_css_selector(
        'div.content-container div.card-content dl')
    labels = data_container.find_elements_by_css_selector('dt')
    values = data_container.find_elements_by_css_selector('dd')
    for index, label in enumerate(labels):
        if label.text.lower() == 'structure':
            data['structure_link'] = values[index].find_element_by_css_selector(
                '.structure a').get_attribute('href')
        elif label.text.lower().strip() in labels_needed:
            data[label.text.lower()] = values[index].text.strip()

    return data


driver = webdriver.Chrome(
    executable_path='./chromedriver.exe')
driver.get('https://www.drugbank.ca/drugs')

with open('./webmd_data.json') as f:
    webmd_data = json.load(f)

drug_names = []
for drug in webmd_data:
    drug_names.append(drug['name'])

unique_names = list(set(drug_names))

updated_webmd_data = []
for name in unique_names:
    for drug in webmd_data:
        if drug['name'] == name:
            updated_webmd_data.append(drug)
            break

print('A total of {0} unique drugs were found.'.format(
    len(updated_webmd_data)))
final_data = []
for index, drug in enumerate(updated_webmd_data):
    print('Crawling {0} / {1} Drugs'.format(index +
                                            1, len(updated_webmd_data)))
    new_info = get_drug_information(drug)
    final_drug_results = {**drug, **new_info}
    final_data.append(final_drug_results)
json.dump(final_data, open('webmd_and_drugbank.json', 'w'), indent=4)


driver.quit()
