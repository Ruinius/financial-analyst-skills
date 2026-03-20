import urllib.request
import json
import sys

payload = {
    "items": [
        {"line_name": "Subscription revenue", "line_category": "income_statement", "line_order": 0},
        {"line_name": "Product revenue", "line_category": "income_statement", "line_order": 1},
        {"line_name": "Total revenue", "line_category": "income_statement", "line_order": 2},
        # ... your extracted items ...
    ]
}

req = urllib.request.Request('http://localhost:8000/predict/income-statement',
                             method='POST',
                             headers={'Content-Type': 'application/json'},
                             data=json.dumps(payload).encode('utf-8'))

try:
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)