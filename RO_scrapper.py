# https://stackoverflow.com/jobs?r=true&q=python
# https://weworkremotely.com/remote-jobs/search?term=python
# https://remoteok.io/remote-dev+python-jobs

import requests
from bs4 import BeautifulSoup

print("Scrapping RemoteOK")

def extract_job(html):
  result = html.find("td", {"class":"company_and_position"})
  title = result.find("h2").get_text(strip=True)
  company = result.find("a", {"class":"companyLink"}).find("h3").get_text(strip=True)
  job_id = html["data-id"]

  return {
      "title": title,
      'company': company,
      'location': "Remote",
      "apply_link": f"https://remoteok.io/l/{job_id}"
  }

def extract_jobs(url):
    jobs = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("div", {"class": "page"}).find("div", {"class":"container"}).find("table", {"id":"jobsboard"}).find_all("tr",{"class":"job"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    return jobs


def get_RO_jobs(word):
    url = f"https://remoteok.io/remote-dev+{word}-jobs"
    jobs = extract_jobs(url)
    return jobs
