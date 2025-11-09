import requests

def scan(url):
    try:
        response = requests.get(url, timeout=10)
        cookies = response.cookies

        insecure_cookies = []
        for cookie in cookies:
            if not cookie.secure:
                insecure_cookies.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'secure': cookie.secure,
                    'httponly': cookie.has_nonstandard_attr('HttpOnly') or False
                })

        server_info = response.headers.get('Server', 'Unknown')

        return {
            'insecure_cookies': insecure_cookies,
            'server_info': server_info,
            'total_cookies': len(cookies)
        }
    except Exception as e:
        return {'error': str(e)}
