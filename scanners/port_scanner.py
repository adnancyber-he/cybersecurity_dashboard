import nmap

def scan(url):
    try:
        hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
        nm = nmap.PortScanner()
        nm.scan(hostname, '1-1024')  # Scan common ports

        open_ports = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        open_ports.append({
                            'port': port,
                            'protocol': proto,
                            'service': nm[host][proto][port]['name']
                        })

        return {'open_ports': open_ports}
    except Exception as e:
        return {'error': str(e)}
