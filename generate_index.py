import requests, os

REPO = "Zephyroam/rspmm"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
GH_TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {"Authorization": f"Bearer {GH_TOKEN}"} if GH_TOKEN else {}

print(f"🔍 Fetching latest release from {REPO}")
res = requests.get(API, headers=headers)
res.raise_for_status()
assets = res.json()["assets"]

with open("docs/index.html", "w") as f:
    f.write("<html><body><h1>Available Wheels</h1><ul>\n")
    for asset in assets:
        if asset["name"].endswith(".whl"):
            f.write(f'<li><a href="{asset["browser_download_url"]}">{asset["name"]}</a></li>\n')
    f.write("</ul></body></html>")

print("index.html generated at docs/index.html")
