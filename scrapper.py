import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def get_so_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)

def extract_so_job(html):
    title = html.find("h2", {"class":"mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class":"mb4"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return { 'title': title, 'company': company, 'location': location, 'apply_link': f"https://stackoverflow.com/jobs/{job_id}" }

def extract_so_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping so page {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_so_job(result)
            jobs.append(job)
    return jobs

def extract_wwr_job(html):
    title = html.find("span", {"class": "title"}).text
    company = html.find_all("span", {"class": "company"})[0].text
    location = html.find("span", {"class": "region"}).text
    apply_link = html.find("a")['href']
    return { 'title': title, 'company': company, 'location': location, 'apply_link': "https://weworkremotely.com"+apply_link }

def extract_wwr_jobs(url):
    jobs = []
    print("Scrapping wwm page")
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("li", {"class": "feature"})
    for result in results:
        job = extract_wwr_job(result)
        jobs.append(job)
    return jobs

def extract_rok_job(html):
    title = html.find("h2").text
    company = html.find("h3").text
    try:
        location = html.find("div", {"class": "location"}).text
    except:
        location = "No office location"
    apply_link = html.find("a", {"class": "preventLink"})['href']
    return { 'title': title, 'company': company, 'location': location, 'apply_link': "https://remoteok.io"+apply_link }

def extract_rok_jobs(url):
    jobs = []
    print("Scrapping rok page")
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("tr", {"class":"job"})
    for result in results:
        job = extract_rok_job(result)
        jobs.append(job)
    return jobs

def get_jobs(word):
    jobs = []
    so_url = f"https://stackoverflow.com/jobs?q={word}&sort=i"
    wwr_url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    rok_url = f"https://remoteok.io/remote-dev+{word}-jobs"
    so_last_page = get_so_last_page(so_url)
    if so_last_page > 10:
        so_last_page = 10
    so_jobs = extract_so_jobs(so_last_page, so_url)
    wwr_jobs = extract_wwr_jobs(wwr_url)
    rok_jobs = extract_rok_jobs(rok_url)
    jobs = so_jobs + wwr_jobs + rok_jobs
    return jobs