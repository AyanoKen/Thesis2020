import sys
import json

resp = {
    "Response":200,
    "Message":"Hello I am Python",
    "Start":'-122.42,38.78',
    "End":'-122.434924,38.794240'
}

print(json.dumps(resp))

sys.stdout.flush()
