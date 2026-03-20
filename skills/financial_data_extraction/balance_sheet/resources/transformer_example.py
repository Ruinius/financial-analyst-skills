import urllib.request
import json
import sys

payload = {
    "items": [
        {"line_name": "Cash and cash equivalents", "line_category": "current_assets", "line_order": 0},
        {"line_name": "Short-term investments", "line_category": "current_assets", "line_order": 1},
        # ... your extracted items ...
    ]
}

req = urllib.request.Request('http://localhost:8000/predict/balance-sheet',
                             method='POST',
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(payload).encode('utf-8'))

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)