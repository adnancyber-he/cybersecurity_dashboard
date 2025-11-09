import requests

def scan(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        required_headers = ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']
        missing_headers = [h for h in required_headers if h not in headers]

        return {
            'present_headers': {k: v for k, v in headers.items() if k in required_headers},
            'missing_headers': missing_headers,
            'all_headers': dict(headers)
        }
    except Exception as e:
        return {'error': str(e)}
