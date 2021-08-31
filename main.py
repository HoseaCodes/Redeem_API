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

url = get_url('software developer', 'houston tx')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('a', 'fs-unmask')
print(len(cards))
card = cards[0]

#for card in cards:
    # Cannot get text
    #print(card.find('div','urgentlyHiring').getText())
    # Not Working
    # print(card.find('td','responsiveEmployer').getText()) 

job_url = 'https://www.indeed.com' + card.get('href')
jobTitle = card.h2.get('jobTitle')
# jobTitle = card.find('span', {'title': 'Software Developer'}).getText()
company = card.find('span', 'companyName')
job_location = card.find('div', 'companyLocation').getText()
post_date = card.find('span', 'date').text
today = datetime.today().strftime('%Y-%m-%d')
salary_tag = card.find('span', 'salary-snippet').getText()
summary = card.find('div', 'job-snippet').getText()
print(salary_tag)
