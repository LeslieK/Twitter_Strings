Note:
To run this for yourself, enter your twitter credentials in the file:
TwitterStrings_stream.py.


This project implements the Knuth-Morris-Pratt string search algorithm and applies it to streaming twitter data.

The user provides the following input in the welcome form:
pattern
user ids to follow
phrases to track

The algorithm streams all tweets that contain <pattern> . The tweets are filtered by the tracking phrases and the users that are followed.
Read more about the input parameters from the Twitter Streaming API docs:
<a href="https://dev.twitter.com/streaming/overview/request-parameters">Request Parameters</a>

The algorithm searches for the pattern in the twitter stream and streams the matching tweets in the browser.
The magic of the algorithm is that when a mismatch occurs between pattern and stream, the algorithm does not "back up" the index into the stream. (You cannot back up a stream!) The algorithm is based on a DFA (Deterministic Finite Automata; i.e., a deterministic state machine) that defines the input pattern. When the characters in a tweet reach an accepting state of the DFA, the algorithm declares a match.

This is my first application using flask.
