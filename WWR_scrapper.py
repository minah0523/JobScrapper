# https://stackoverflow.com/jobs?r=true&q=python
# https://weworkremotely.com/remote-jobs/search?term=python
# https://remoteok.io/remote-dev+python-jobs

import requests
from bs4 import BeautifulSoup

print("Scrapping WeWorkRemotely")

def extract_job(html):
    title = html.find("span", {"class":"title"}).get_text(strip=True)
    company = html.find("span", {"class":"company"}).get_text(strip=True)
    location = html.find("span", {"class":"region"}).get_text(strip=True)
    link = html.find("a", recursive=False)["href"]

    return {
        "title": title,
        'company': company,
        'location': location,
        "apply_link": f"https://weworkremotely.com/{link}"
    }

def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("div", {"class": "jobs-container"}).find("section", {"class":"jobs"}).find_all("li",{"class":"feature"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    return jobs


def get_WWR_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = extract_jobs(url)
    return jobs
