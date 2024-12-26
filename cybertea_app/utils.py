from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
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

    url = f"https://cve.circl.lu/api/cve/{cve_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch CVE details: {e}")
        return None


def update_views(request, object):
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context["hitcount"] = {"pk": hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    if hit_count_response.hit_counted:
        hits = hits+1
        hitcontext["hitcounted"] = hit_count_response.hit_counted
        hitcontext["hit_message"] = hit_count_response.hit_message
        hitcontext["total_hits"] = hits

