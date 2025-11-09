import ssl
import socket

def scan(url):
    try:
        hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()

        return {
            'valid': True,
            'certificate_info': {
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'version': cert['version'],
                'notBefore': cert['notBefore'],
                'notAfter': cert['notAfter']
            },
            'cipher': cipher
        }
    except Exception as e:
        return {'valid': False, 'error': str(e)}
