Requires CSV

The way this works is:

If a torrent is stalled, a strike is recorded in a CVS file.

If a torrent is downloading, a strike is removed.

3 strikes and the torrent gets removed from Radarr and added to the blocklist.

When a torrent gets removed from Radarr, it automatically starts a new search for the file.

I set up my system to run the script every 10 minutes via Windows Task Scheduler.

This way, the sctipt is not always running.  Rather it is run on a schedule defined by the user and the information is stored and edited in a separate file.

You will have to Put your own API key in on line 5.

api_key = "Your-API-Key"

If you are having issues with the Task Scheduler not running the script, Make sure the CSV file is in the same directory as the script.  
