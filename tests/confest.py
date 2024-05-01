import logging
import os

import vcr

# ALL = "all"
# ANY = "any"
# NEW_EPISODES = "new_episodes"
# NONE = "none"
# ONCE = "once"

logging.getLogger("vcr").setLevel(logging.WARNING)
vcr_c = vcr.VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode=os.environ.get("VCR_RECORD_MODE", "none"),
    match_on=["host", "path", "method", "query", "raw_body", "body"],
    filter_headers=["Authorization", "Cookie"],
    ignore_hosts=["127.0.0.1", "localhost"],
)
