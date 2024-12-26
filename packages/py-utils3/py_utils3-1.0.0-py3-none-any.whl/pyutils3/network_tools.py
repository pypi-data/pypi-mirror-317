# smart_library/network_tools.py
import requests

def check_internet(sites=input("enter URL of site to check: ")):
    """Check internet connection by testing multiple sites."""
    for site in sites:
        try:
            response = requests.get(site, timeout=5)
            if response.status_code == 200:
                return f"Connection available with site: {site}"
        except requests.RequestException:
            continue
    return "No internet connection with any of the provided sites."
