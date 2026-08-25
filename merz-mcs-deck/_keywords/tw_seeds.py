import json,sys
sys.path.insert(0,'.')
import pull_keywords as P
P.MARKETS = {"TW": {"location_name":"Taiwan","language_name":"Chinese (Traditional)",
   "seeds":["ultherapy","音波拉提","電波拉皮","超音波拉皮"]}}
P.main()
