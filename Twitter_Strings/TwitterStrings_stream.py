from twitter import TwitterStream, OAuth
from KnuthMorrisPrattStream import KMP
from flask import render_template
import re

CREDS = {"consumer_key": "fill-in-your-key",
          "consumer_secret": "fill-in-your-secret",
          "token": "fill-in-your-token",
          "token_secret": "fill-in-your-token-secret"
          }



auth = OAuth(
    consumer_key=CREDS["consumer_key"],
    consumer_secret=CREDS["consumer_secret"],
    token=CREDS["token"],
    token_secret=CREDS["token_secret"]
)

id_dict = {"wikileaks": "16589206",
           "aljazeera": "76067316",
           "NYFBI": "211635204",
           "reutersiran": "47633485",
           "WhiteHouse": "30313925"
           }


# public_stream = TwitterStream(auth=auth, domain='stream.twitter.com')
# iterator = public_stream.statuses.filter(language="en",
#                                          follow=','.join(id_dict.values()),
#                                          track="terrorism, weapons, \
#                                          drone attack, i want to kill")

# def set_context(language, follow, track, locations):
def set_context(language, follow, track):
    """
    language: "en"
    follow: comma-separated list of account ids
    track: comma-separated list of strings
    locations: 2 pairs of numbers
    """
    public_stream = TwitterStream(auth=auth, domain='stream.twitter.com')
    # iterator = public_stream.statuses.filter(language=language,
    #                                          follow=follow,
    #                                          track=track,
    #                                          locations=locations)
    iterator = public_stream.statuses.filter(language=language,
                                             follow=follow,
                                             track=track)
    return iterator


def run_kmp(pattern_to_search_for, iterator):
    """
    pattern_to_search_for:
    input pattern to search for in twitter stream
    iterator: yields twitter objects
    """
    kmp = KMP(pattern_to_search_for)
    pattern_index = 0

    for item in iterator:
        try:
            text = item['text']
            # replaces non-ascii character with ascii string
            text = re.sub('[^\x00-\xff]', '--', text)
            for c in text:
                pattern_index = kmp.dfa.next(c, pattern_index)
                if int(pattern_index) == len(pattern_to_search_for):
                #  print("MATCH!!!!!")
                    print(text)
                    yield render_template("match.html", match=text)
        except StopIteration:
            print("Stopped!")
        except Exception as e:
            print('error:', str(e))
            #break

########################################################
if __name__ == "__main__":
    #  comment out yield statements in run_kmp before running this module
    run_kmp("trump", set_context(language="en",
                                follow=','.join(id_dict.values()),
                                track="New Hampshire, Cruz, Rubio"))
