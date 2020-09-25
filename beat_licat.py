import os
import random
import subprocess
import time
import webbrowser

import requests
from bs4 import BeautifulSoup

github_url = "https://github.com/obsidianmd/obsidian-releases/releases"
discord_url = "https://discord.com/channels/686053708261228577/716028884885307432"
payload = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
    "Referer": "https://www.google.com",
    "DNT": 1,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:81.0) Gecko/20100101 Firefox/81.0",
}


def notify(title, text, url):
    os.system(f"""osascript -e 'display notification "{text}" with title "{title}"'""")
    webbrowser.open(url, new=1)


def check_page(url):
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        new = soup.find_all("a", class_="muted-link css-truncate")[0]
    return new


def write_to_clipboard(output):
    process = subprocess.Popen(
        "pbcopy", env={"LANG": "en_US.UTF-8"}, stdin=subprocess.PIPE
    )
    process.communicate(output.encode("utf-8"))


def compare_old_new(old, new):
    if old != new:  # if new release
        webbrowser.open(discord_url, new=1)
        notify("New Obsidian release!", "Quick! BEAT LICAT!", github_url)
        v = new["title"]
        # copy text to clipboard
        spoiler_txt = f"SPOILER ALERT: @Licat will release Obsidian {v} in a few seconds... ausius-Licat scoreboard: 3-2 \U0001F923\U0001F923"
        write_to_clipboard(spoiler_txt)
        return new, False  # break loop
    else:
        print("No new release yet.")
        return new, True  # continue loop


def start_checking():
    old = check_page(github_url)
    i = 0
    status = True
    while status:
        i += 1
        print(f"Checking for Obisidian release (scrape {i})...")
        new, status = compare_old_new(old, check_page(github_url))
        if status:
            time.sleep(random.randint(5, 20))


start_checking()
