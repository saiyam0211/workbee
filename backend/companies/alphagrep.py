import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# Scrape AlphaGrep board and parse embedded JSON to get titles, locations, links and descriptions
BOARD_URL = "https://boards.greenhouse.io/alphagrepsecurities"

resp = requests.get(BOARD_URL, timeout=30)
resp.raise_for_status()
soup = BeautifulSoup(resp.content, "html.parser")

# Find the window.__remixContext JSON payload which includes jobPosts with content (JD)
script_with_ctx = None
for script in soup.find_all("script"):
    if script.string and "window.__remixContext" in script.string:
        script_with_ctx = script.string
        break

data = []
if script_with_ctx:
    # Extract JSON assigned to window.__remixContext = {...};
    match = re.search(r"window.__remixContext\s*=\s*(\{.*\})\s*;", script_with_ctx, re.DOTALL)
    if match:
        try:
            remix_ctx = json.loads(match.group(1))
            jobs = remix_ctx.get("state", {}).get("loaderData", {}).get("routes/$url_token", {}).get("jobPosts", {}).get("data", [])
            for job in jobs:
                title = job.get("title", "").strip()
                location = job.get("location", "").strip()
                link = job.get("absolute_url", "").strip()
                content_html = job.get("content", "") or ""
                jd_text = "Description not available"
                if content_html:
                    jd_text = BeautifulSoup(content_html, "html.parser").get_text(" ", strip=True) or jd_text
                data.append({
                    "job_title": title,
                    "job_location": location,
                    "job_link": link,
                    "job_description": jd_text,
                    "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        except Exception:
            pass

# Fallback: parse visible listings if JSON wasn't found
if not data:
    for row in soup.select(".job-posts table tbody tr.job-post td.cell a"):
        try:
            title = row.select_one("p.body.body--medium").get_text(strip=True)
            meta = row.select_one("p.body.body__secondary.body--metadata").get_text(strip=True)
            link = row.get("href")
            data.append({
                "job_title": title,
                "job_location": meta,
                "job_link": link,
                "job_description": "Description not available",
                "job_posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception:
            continue

print(json.dumps({"company": "Alphagrep", "data": data}))





