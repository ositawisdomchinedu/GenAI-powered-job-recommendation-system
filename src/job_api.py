from apify_client import ApifyClient
import os 
import requests
from dotenv import load_dotenv
load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Fetch LinkedIn jobs based on search query and location
def fetch_linkedin_jobs(title="", location="Nigeria", rows=50, companies=None, company_ids=None):
    run_input = {
        "title": title,
        "location": location,
        "companyName": companies or [],
        "companyId": company_ids or [],
        "publishedAt": "",
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }

    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location = "nigeria", rows=60):
    run_input = {
        "keyword": search_query,
        "maxJobs": 60,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_indeed_jobs(search_query, location= "nigeria",  rows=50,):

    """Fetch job listings from Indeed using Apify actor."""
    
    run_input = {
        "scrapeJobs.searchUrl": search_query,
        "count": 50,
        "location": location,
       
    }

    run = apify_client.actor("qA8rz8tR61HdkfTBL").call(run_input=run_input)
    jobs =  list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_remotive_jobs(search_query: str, limit: int = 60):
    query = search_query.strip().replace(",", " ")
    url = f"https://remotive.com/api/remote-jobs?search={query}&limit={limit}"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json().get("jobs", [])
    else:
        print("Remotive API error:", response.status_code)
        return []

