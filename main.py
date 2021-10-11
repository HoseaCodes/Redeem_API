import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    """Generate url from position and location"""
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = template.format(position, location)
    return url

"""Testing Block"""
# url = get_url('software developer', 'houston tx')
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# cards = soup.find_all('a', 'fs-unmask')
# print(len(cards))
# card = cards[0]

#for card in cards:
    # Cannot get text
    #print(card.find('div','urgentlyHiring').getText())
    # Not Working
    # print(card.find('td','responsiveEmployer').getText()) 

# Currently shows none
# jobTitle = card.h2.get('jobTitle')
"""Testing Block"""

def get_record(card):
    """Extract job data from a single record"""
    try:
        job_title = card.find('span', {'title': 'Software Developer'}).getText()
    except AttributeError:
        job_title = ''
    company = card.find('span', 'companyName').getText()
    job_location = card.find('div', 'companyLocation').getText()
    post_date = card.find('span', 'date').text
    today = datetime.today().strftime('%Y-%m-%d')
    summary = card.find('div', 'job-snippet').getText()
   # this does not exists for all jobs, so handle the exceptions
    try:
        salary_tag = card.find('span', 'salary-snippet').getText()
    except AttributeError:
        salary_tag = ''  
    job_url = 'https://www.indeed.com' + card.get('href')
    record = (job_title, company, job_location, post_date, today, summary, salary_tag, job_url)
    return record

def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position, location)
    print(url)
    count = 0
    # extract the job data
    while count < 2:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('a', 'fs-unmask')
        for card in cards:
            record = get_record(card)
            records.append(record)
        count = count + 1
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
        print(records)
    # save the job data
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)

def getUserInput():
    position = input("What position are you looking for?\n")
    print(f"Great you are looking for a {position}. We still need a little more info.")
    location = input("Where would you like to work?\n")
    print(f"Gotcha, we will find a {position} in {location}.")
    info = {"position": position, "location": location}
    return info

info = getUserInput()

# run the main program
main(info['position'], info['location'])