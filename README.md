## What is 'thmigpen'?
A Python 3.5 script to post notifications and public channel messages to pnut.io a week before a \#ThemeMonday event.

Though probably inelegant, intended initially to be called by a cron job and run 1 to 3 times throughout the day at times to suit Far Eastern, European and North American audiences.  It's important to note it'll only post on one day a month.

### Scripts:
* **thmigpen** - the main script (see above.)
* **thmigpoll** - a very alpha rudimentary poll vote collector which checks a specific hashtag's RSS feed.  The script for the RSS feed for e.g. **`#tmpoll201803`** will examine a predefined list of candidates, reject non-matching text and add matches to the total of votes.  Intended to be called by a cron job and run at frequent intervals over a small range of dates each month.
