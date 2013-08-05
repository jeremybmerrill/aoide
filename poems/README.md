A script for generating arbitrary poems from "found" lines in a given input text.

TODO:

code:
  factor out creation form in source_detail
  fix two startup bugs:
	utf8 fix: ALTER TABLE poems_source MODIFY COLUMN text TEXT CHARACTER SET utf8 COLLATE utf8_general_ci;
			maybe: ALTER DATABASE poems CHARACTER SET utf8 COLLATE utf8_general_ci
	touch /tmp/pickle
  retain apostrophes, quotes, etc. somehow (when are they actually missing?)

design
  put each stanza of longer poems in their own <p>
  fancy format for free verse, limit length on free verse lines
  indent poems on front page, source pages.
  put buttons side-by-side



maybe: 
	denormalize DB to keep a poem_count on sources?
	is beautiful soup too heavy for just finding a title?
	sum shares as votes? (hard.)


better rime comparison (e.g. working in stress, don't approve "very" and "Peggy" but do approve "he" and "Peggy")


write algorithm post




maybe:
-------
voting?
users
  profiles
class-based views (more pythonic!!)


aws thing 
http://stackoverflow.com/questions/3652657/what-algorithm-does-readability-use-for-extracting-text-from-urls
make showemapoem an egg

