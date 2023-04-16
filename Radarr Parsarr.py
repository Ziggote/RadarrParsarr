import requests
import csv

# API key & endpoint
api_key = "Your-API-Key"
headers = {"X-Api-Key": api_key}

response = requests.get("http://localhost:7878/api/v3/queue", headers=headers)
if response.status_code == 200:
    data = response.json()

    # Keep track of strikes for each torrent
    strikes = {}

    with open("radarrTestarrInfo.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Read the existing strikes for each torrent from the file
            download_id = row["Download ID"]
            strikes[download_id] = int(row["Strike"])

    with open("radarrTestarrInfo.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Title", "Download ID", "ID", "Sizeleft", "Size", "Status", "Strike"]
        )
        for torrent in data:
            title = torrent.get("title", "")
            download_id = torrent.get("downloadId", "")[-5:]
            id = torrent.get("id", "")
            sizeleft = torrent.get("sizeleft", "")
            size = torrent.get("size", "")
            status = torrent.get("status", "")

            # Initialize the strikes for each torrent in an individual dictionary
            torrent_strikes = {download_id: strikes.get(download_id, 0)}

            # Increment the strike count for the current torrent if its status is 'Warning'
            if status == "Warning":
                torrent_strikes[download_id] += 1
                strikes[download_id] = torrent_strikes[download_id]

            # Remove a strike if the status is 'Downloading'
            if status == "Downloading":
                if torrent_strikes[download_id] > 0:
                    torrent_strikes[download_id] -= 1
                    strikes[download_id] = torrent_strikes[download_id]

            # Remove the torrent if it has 3 or more strikes
            if torrent_strikes[download_id] >= 3:
                delete_response = requests.delete(
                    "http://localhost:7878/api/v3/queue/{}?removeFromClient=true&blocklist=true&apikey={}".format(
                        id, api_key
                    )
                )
                if delete_response.status_code == 200:
                    print("Torrent: {} removed".format(title))
                    # Remove the torrent from the strikes dictionary
                    strikes.pop(download_id, None)
                    # Update the torrent_strikes dictionary to 0 strikes after removal
                    torrent_strikes[download_id] = 0
                else:
                    print(
                        "Failed to remove torrent with download ID {} and status code {}".format(
                            download_id, delete_response.status_code
                        )
                    )

            writer.writerow(
                [
                    title,
                    download_id,
                    id,
                    sizeleft,
                    size,
                    status,
                    torrent_strikes[download_id],
                ]
            )

else:
    print("Request failed with status code", response.status_code)
