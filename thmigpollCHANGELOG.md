## Changelog
(most recent first)

### v0.1.12 2018-03-18:
* Skipped processing of notifications by checking if `<=>` exists within a post.
* Removed now-obsoleted `import feedparser`.

### v0.1.11 2018-03-18:
* Replaced previous limiting reliance on RSS feed; now uses PNUTpy's `pnutpy.api.posts_with_hashtag` to return more than 9 results (currently set to an arbitrary maximum of 50.)
* Tidied messages text again.
* Changed version numbering to use thmigpen's, currently at 0.1; but note thmigpoll is in more active development, might eventually be split out.

### v0.1.7 2018-03-15:
* Added post numbers to votes as a precursor to reply confirmation of votes.
* Tidied messages, re-ordered some code.

### v0.1.4 2018-03-13:
* Added notification if no-one voted.

### v0.1.3 2018-03-12:
* Tidied up poll summary output.

### v0.1.2 2018-03-12:
* Trapped posts without a hash attached to the tag.

### v0.1.1 2018-03-11:
* Added vote totals.

### v0.1.0 2018-03-10:
* First commit - a rudimentary script to list respondents to a poll; entirely dependent on an RSS feed of a pnut.io hashtag.
