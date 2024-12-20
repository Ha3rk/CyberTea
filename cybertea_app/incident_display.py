import requests

def fetch_recent_cves(limit=10):
    url = "https://cve.circl.lu/api/last"
    try:
        response = requests.get(url)
        response.raise_for_status()
        cve_list = response.json()
        # Filter out CVEs missing the 'id' field
        return [cve for cve in cve_list if 'id' in cve][:limit]
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []


def fetch_cve_details(cve_id):
    """
    Fetch details of a specific CVE using its ID.
    :param cve_id: CVE ID (e.g., CVE-2024-1234).
    :return: JSON details of the CVE or None on failure.
    """
    url = f"https://cve.circl.lu/api/cve/{cve_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch CVE details: {e}")
        return None
