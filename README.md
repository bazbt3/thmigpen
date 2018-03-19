## What is 'thmigpen'?
Python 3.5 scripts to post \#ThemeMonday-related notifications and public channel messages to pnut.io.

### Scripts:
* **thmigpen** - Though probably inelegant, intended initially to be called by a cron job a week before a \#ThemeMonday event and run 1 to 3 times throughout the day at times to suit Far Eastern, European and North American audiences.  It's important to note it'll only post on one day a month.
* **thmigpoll** - A quite alpha rudimentary poll vote collector which checks a specific hashtag.  The script for e.g. `#tmpoll201803` will examine a predefined list of candidates, reject non-matching text and add matches to the total of votes.  Intended to be called by a cron job and run at frequent intervals over a small range of dates each month.
* **thmigask** - A very rudimentary poll suggestion collector which checks a specific hashtag.  The script for e.g. `#tmask201803` will check the hashtag, reject non-matching text and eventually compile and save a list of poll options. Intended to run before thmigpoll at frequent intervals over a small range of dates each month.
