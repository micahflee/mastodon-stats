#!/usr/bin/env python3

import json
from datetime import datetime
import httpx
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator


def millions(x, pos):
    "The two args are the value and tick position"
    return "%1.1fM" % (x * 1e-6)


def load_data_live():
    r = httpx.get("https://api.joinmastodon.org/statistics")
    data = json.loads(r.content)
    return data


def main():
    # Get the statistics
    with open("statistics.json") as f:
        data = json.load(f)

    # Convert them to lists
    dates = []
    server_counts = []
    user_counts = []
    active_user_counts = []
    for day in data:
        dates.append(day["period"][0:10])
        server_counts.append(int(day["server_count"]))
        user_counts.append(int(float(day["user_count"])))
        active_user_counts.append(int(float(day["active_user_count"])))

    # Ignore the last day
    dates = dates[:-1]
    server_counts = server_counts[:-1]
    user_counts = user_counts[:-1]
    active_user_counts = active_user_counts[:-1]

    dates = [datetime.strptime(date, "%Y-%m-%d").strftime("%b %-d") for date in dates]

    # Plot
    fig, ax = plt.subplots()
    # ax.plot(dates, user_counts, label="Total Users")
    ax.plot(dates, active_user_counts, label="Monthly Active Users")

    formatter = FuncFormatter(millions)
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_locator(MaxNLocator(10))
    ax.xaxis.set_major_locator(MaxNLocator(15))

    plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
    plt.xticks(fontsize=8)

    plt.ylim(bottom=0)

    ax.set_title(f"Mastodon Monthly Active Users", fontsize=18)
    # ax.legend()

    # plt.show()
    plt.savefig("mastadon-stats.png", dpi=200)


if __name__ == "__main__":
    main()
