from xai_grok.sdk import XaiGrokSDK

# Make the module callable directly
import sys
sys.modules[__name__] = XaiGrokSDK
