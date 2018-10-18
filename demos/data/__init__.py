import pollster
import pprint

from .states import get_long_name

# Types
# - Polls
# - Demographic
# - Results
class Source(object):
    def __init__(self, url):
        self.url = url


api = pollster.Api()

try:
    charts = api.charts_get(cursor=None, tags="", election_date="2013-10-20")
    pprint.pprint(charts)
except pollster.rest.ApiException as e:
    print("Exception when calling DefaultApi->charts_get: %s\n" % e)
    

__all__ = ["get_long_name"]
