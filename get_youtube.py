#!/usr/bin/python3

from selenium import webdriver
import json
import time

email = "sphinxpig@gmail.com"
passwd = "hqz1hqz2"

channel_rank_table = {
    "3Blue1Brown":                  3,
    "Adult Swim":                   5,
    "Anton Petrov":                 4,
    "AwesomeEpicGuys":              2,
    "Best Replays World of Tanks":  6,
    "Binging with Babish":          9,
    "CaptainSparklez":              5,
    "CaptainSparklez 2":            4,
    "Cody'sLab":                    7,
    "Computerphile":                3,
    "Curious Droid":                5,
    "CuriousMarc":                  3,
    "DemolitionRanch":              5,
    "EEVblog":                      3,
    "ElectroBOOM":                  6,
    "Emergency Awesome":            5,
    "Everyday Astronaut":           4,
    "Food Wishes":                  9,
    "How Ridiculous":               5,
    "Joe Scott":                    9,
    "Joe Scott - TMI":              3,
    "JustforlolzFYI":               7,
    "Klei Entertainment":           7,
    "Kurzgesagt – In a Nutshell":   9,
    "LemmingRush":                  9,
    "Linus Tech Tips":              5,
    "LiveOverflow":                 6,
    "Mark Felton Productions":      3,
    "Mark Rober":                   9,
    "MinuteEarth":                  7,
    "New Rockstars":                5,
    "NightHawkInLight":             7,
    "NileRed":                      8,
    "PBS Space Time":               5,
    "Pixar":                        4,
    "QuickyBaby":                   9,
    "Scott Manley":                 8,
    "Screen Rant":                  6,
    "ScreenCrush":                  6,
    "Seeker":                       7,
    "ShadowZone":                   6,
    "Simone Giertz":                9,
    "SmarterEveryDay":              8,
    "Subject Zero Science":         7,
    "TAOFLEDERMAUS":                4,
    "Taugrim":                      8,
    "TechLinked":                   4,
    "Techquickie":                  4,
    "The Mighty Jingles":           9,
    "The Tank Museum":              5,
    "The Thought Emporium":         9,
    "Today I Found Out":            6,
    "Unbox Therapy":                6,
    "Veritasium":                   7,
    "Vsauce":                       8,
    "Vsauce2":                      4,
    "Vsauce3":                      4,
    "Wintergatan":                  6,
    "World of Tanks Best Replays":  7,
    "World of Tanks North America": 4,
    "bigclivedotcom":               3,
    "colinfurze":                   6,
    "minutephysics":                7,
    "mitxela":                      6,
    "skill4ltu":                    9,
    "thoughtbot":                   6,
}

def get_youtube():
    browser = webdriver.Firefox()

    browser.get("https://youtube.com")

    try:
        signin_button = browser.find_element_by_css_selector("paper-button#button.size-small.ytd-button-renderer")
        signin_button.click()

        email_form = browser.find_element_by_id("identifierId")
        email_form.click()
        email_form.send_keys(email)
        browser.find_element_by_id("identifierNext").click()

        passwd_form = None
        while True:
            try:
                passwd_form = browser.find_element_by_css_selector("[type=password][name=password]")
            except:
                time.sleep(0.5)
            finally:
                break
        time.sleep(1)
        passwd_form = browser.find_element_by_css_selector("[type=password][name=password]")
        passwd_form.click()
        passwd_form.send_keys(passwd)
        browser.find_element_by_id("passwordNext").click()
    except Exception as e:
        # pass
        print(e)

    while True:
        try:
            browser.find_element_by_css_selector("yt-icon.ytd-notification-topbar-button-renderer").click()
        except:
            time.sleep(0.2)
        finally:
            print(browser.find_element_by_css_selector("yt-icon.ytd-notification-topbar-button-renderer"))
            break
    items = None
    while True:
        try:
            items = browser.find_element_by_css_selector("div#items.yt-multi-page-menu-section-renderer")
            print(items)
        except:
            time.sleep(0.2)
        finally:
            break
    print("Logged in.")
    # items = browser.find_element_by_css_selector("div#items.yt-multi-page-menu-section-renderer")
    notifications = items.find_elements_by_css_selector("ytd-notification-renderer a[href]")
    browser.find_element_by_css_selector("yt-icon.ytd-notification-topbar-button-renderer").click()
    # notifications = items.find_elements_by_css_selector("ytd-notification-renderer.unread a[href]")
    spinner = browser.find_element_by_css_selector("div#spinnerContainer.paper-spinner")
    while len(browser.find_elements_by_css_selector("ytd-rich-grid-video-renderer")) < 100:
        browser.execute_script("scroll(0, 10000000);")
        try:
            while "active" not in spinner.get_attribute("class"):
                time.sleep(0.05)
            while "active" in spinner.get_attribute("class"):
                time.sleep(0.05)
        except:
            break
    tiles = browser.find_elements_by_css_selector("ytd-rich-grid-video-renderer")
    videos = []
    time.sleep(1)
    print("Processing tiles ...")
    for i, tile in enumerate(tiles):
        video_link = tile.find_element_by_css_selector("a[href]").get_attribute("href")
        thumbnails = tile.find_elements_by_css_selector("img#img")
        thumbnail_link = thumbnails[0].get_attribute("src")
        channel_avater_link = thumbnails[1].get_attribute("src")

        progress = ""
        try:
            progress = tile.find_element_by_css_selector("#progress").get_attribute("style")
            progress = progress.replace("width: ", "").replace(";", "")
        except:
            pass

        title = tile.find_elements_by_css_selector("yt-formatted-string")[0].text
        channel_name = tile.find_elements_by_css_selector("yt-formatted-string")[1].text
        print("\r", i, title)

        time_status = None
        while True:
            try:
                time_status = tile.find_element_by_css_selector("ytd-thumbnail-overlay-time-status-renderer")
            except:
                time.sleep(0.2)
            finally:
                break

        if time_status == None:
            continue
        browser.execute_script("arguments[0].scrollIntoView(true);", time_status)
        length = ""
        while True:
            time_status = tile.find_element_by_css_selector("ytd-thumbnail-overlay-time-status-renderer")

            length = time_status.text
            if len(length) > 0:
                break
            time.sleep(0.2)
        # tile.find_elements_by_css_selector("yt-formatted-string")[1].get_attribute("href") # channel link
        view_count, publish_time = None, None
        while True:
            metadata_lines = tile.find_elements_by_css_selector("#metadata-line span")
            if len(metadata_lines) == 0:
                break
            else:
                view_count = metadata_lines[0].text
                publish_time = metadata_lines[1].text
                print(view_count, publish_time)
                if len(view_count) == 0 or len(publish_time) == 0:
                    print("continue")
                    continue
                break

        videos.append(process_video({
            "title": title,
            "video_link": video_link,
            "thumbnail_link": thumbnail_link,
            "channel_avater_link": channel_avater_link,
            "progress": progress,
            "length": length,
            "channel_name": channel_name,
            "view_count": view_count,
            "publish_time": publish_time,
        }))
    return videos

def process_video(video):
    publish_time = video["publish_time"]
    if publish_time != None:
        publish_time = publish_time.replace("Streamed ", "").replace(" ago", "").replace("s", "")
        publish_time = publish_time.split()
        time_conversion = {
            "minute": 1,
            "hour": 60,
            "day": 1440,
            "week": 1440 * 7,
            "month": 1440 * 30,
            "year": 1440 * 365,
        }
        publish_time = int(publish_time[0]) * time_conversion[publish_time[1]]
    else:
        publish_time = 1

    view_count = video["view_count"]
    if view_count != None:
        view_count = view_count.replace(" views", "")
        view_count = view_count[:-1], view_count[-1]
        if view_count[1] != 'M' and view_count[1] != 'K':
            view_count = view_count[0] + view_count[1], ""
        unit_conversion = {
            "M": 1_000_000,
            "K": 1_000,
            "": 1,
        }
        view_count = float(view_count[0]) * unit_conversion[view_count[1]]
    else:
        view_count = 1

    length = video["length"]
    print(length)
    length = list(map(int, length.split(":")))
    if len(length) == 3:
        length = length[0] * 3600 + length[1] * 60 + length[2]
    else:
        length = length[0] * 60 + length[1]

    # video["publish_time"] = publish_time
    # video["view_count"] = view_count
    # video["length"] = length
    video["rank"] = rank_video(length, video["channel_name"], publish_time, view_count)
    return video

def rank_video(length, channel, recency, views):
    trend = views / recency

    length_rank = 0
    if length < 10:
        length_rank = 9
    elif length < 15:
        length_rank = 8
    elif length < 22:
        length_rank = 7
    elif length < 30:
        length_rank = 6
    elif length < 45:
        length_rank = 5
    elif length < 60:
        length_rank = 4
    else:
        length_rank = 2

    view_rank = 0
    if views < 100_000:
        view_rank = 3
    if views < 200_000:
        view_rank = 4
    if views < 500_000:
        view_rank = 5
    if views < 700_000:
        view_rank = 6
    elif views < 1_000_000:
        view_rank = 7
    else:
        view_rank = 9

    recent_rank = 0
    if recency < 12 * 60:
        recent_rank = 9
    elif recency < 24 * 60:
        recent_rank = 8
    elif recency < 1440 * 7:
        recent_rank = 7
    elif recency < 1440 * 30:
        recent_rank = 6
    elif recency < 1440 * 30 * 3:
        recent_rank = 5
    elif recency < 1440 * 365:
        recent_rank = 4
    else:
        recent_rank = 2

    channel_rank = channel_rank_table[channel] if channel in channel_rank_table else 2

    rank = channel_rank * 10 + recent_rank * 8 + view_rank + length_rank
    return {
        "length_rank": length_rank,
        "view_rank": view_rank,
        "recent_rank": recent_rank,
        "channel_rank": channel_rank,
        "trend": trend,
        "rank": rank,
    }

print(json.dump(get_youtube(), open("test.json", "w")))
