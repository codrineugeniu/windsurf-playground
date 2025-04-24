import requests
from bs4 import BeautifulSoup

URL = "https://www.levi9.com/event/strategic-data-transformation-from-bi-reports-to-ai-powered-decision-making/"

def get_authors():
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the speakers section by heading
    speakers = []
    for h2 in soup.find_all(["h2", "h3", "h4", "h5", "h6"]):
        if "speaker" in h2.get_text(strip=True).lower():
            # Speakers section found, get following elements
            next_node = h2.find_next_sibling()
            while next_node:
                # Look for names and titles
                if next_node.name in ["h3", "h4", "h5", "h6"]:
                    name = next_node.get_text(strip=True)
                    # Next element might be their job title
                    job = ""
                    job_node = next_node.find_next_sibling()
                    if job_node and job_node.name in ["p", "h5", "h6"]:
                        job = job_node.get_text(strip=True)
                    speakers.append((name, job))
                next_node = next_node.find_next_sibling()
                # Stop if we hit another major section
                if next_node and next_node.name == "h2":
                    break
            break
    # Fallback: parse by LinkedIn links and nearby text
    if not speakers:
        for a in soup.find_all("a", href=True):
            if "linkedin.com/in/" in a["href"]:
                name = a.get_text(strip=True)
                # Try to get job title nearby
                job = ""
                parent = a.parent
                if parent:
                    sibs = list(parent.children)
                    for i, sib in enumerate(sibs):
                        if sib == a and i+1 < len(sibs):
                            next_sib = sibs[i+1]
                            if hasattr(next_sib, 'get_text'):
                                job = next_sib.get_text(strip=True)
                speakers.append((name, job))
    return speakers

if __name__ == "__main__":
    authors = get_authors()
    print("Authors found:")
    for name, job in authors:
        print(f"- {name} ({job})")
