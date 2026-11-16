"""Build sing-box rules from manual entries and validated upstream sources."""
import ipaddress
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
GEOSITE = 'https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/'


def download(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'future-soso-domains-updater'}), timeout=30) as response:
                text = response.read(2_000_001).decode('utf-8-sig')
            if not text.strip() or len(text.encode('utf-8')) > 2_000_000:
                raise ValueError(f'Empty or oversized source: {url}')
            return text
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def domain(value):
    value = value.lower().rstrip('.')
    if len(value) > 253 or not all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', part) for part in value.split('.')):
        raise ValueError(f'Invalid domain: {value}')
    return value


def geosite(services, fetch):
    result = {'domain': set(), 'domain_suffix': set()}
    visited = set()

    def visit(service, stack=()):
        if not re.fullmatch(r'[a-z0-9-]+', service):
            raise ValueError(f'Unsupported include: {service}')
        if service in stack:
            raise ValueError(f'Include cycle: {service}')
        if service in visited:
            return
        text = fetch(GEOSITE + service)
        entries = 0
        for raw in text.splitlines():
            line = raw.split('#', 1)[0].strip()
            if not line:
                continue
            token = line.split()[0]  # @attributes do not change matching semantics.
            entries += 1
            if token.startswith('include:'):
                visit(token[8:], (*stack, service))
            else:
                kind, sep, value = token.partition(':')
                if not sep:
                    kind, value = 'domain', token
                field = {'domain': 'domain_suffix', 'full': 'domain'}.get(kind)
                if field is None:
                    raise ValueError(f'Unsupported geosite syntax: {token}')
                result[field].add(domain(value))
        if not entries:
            raise ValueError(f'Empty service: {service}')
        visited.add(service)

    for service in services:
        visit(service)
    return result


def telegram(text):
    networks = set()
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if line:
            network = ipaddress.ip_network(line, strict=True)
            if network.prefixlen == 0 or not network.is_global:
                raise ValueError(f'Unsafe network: {line}')
            networks.add(network)
    if not networks or not {4, 6}.issubset({n.version for n in networks}):
        raise ValueError('Expected nonempty IPv4 and IPv6 Telegram lists')
    return [str(n) for n in sorted(networks, key=lambda n: (n.version, int(n.network_address), n.prefixlen))]


def build(root=ROOT, fetch=download):
    config = json.loads((root / 'sources/config.json').read_text(encoding='utf-8'))
    domains = json.loads((root / 'sources/manual/domains.json').read_text(encoding='utf-8'))
    facetime = json.loads((root / 'sources/manual/facetime-ip.json').read_text(encoding='utf-8'))
    upstream = geosite(config['domain_services'], fetch)
    rule = domains['rules'][0]
    for field, values in upstream.items():
        values.update(domain(v) for v in rule.get(field, []))
        if values:
            rule[field] = sorted(values)
    cidrs = telegram(fetch(config['telegram_url']))
    # Replace only Telegram's UDP ranges; keep other networks and port scopes.
    facetime['rules'][2]['ip_cidr'] = sorted(set(facetime['rules'][2]['ip_cidr']) | set(cidrs))
    for item in facetime['rules']:
        for value in item['ip_cidr']:
            ipaddress.ip_network(value, strict=True)
    return {'domains.json': domains, 'facetime-ip.json': facetime}


def main():
    # Finish all downloads and validation before touching output files.
    outputs = build()
    for name, value in outputs.items():
        content = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
        target = ROOT / name
        if not target.exists() or target.read_text(encoding='utf-8') != content:
            temp = target.with_suffix('.tmp')
            temp.write_text(content, encoding='utf-8', newline='\n')
            temp.replace(target)
            print(f'Updated {name}')


if __name__ == '__main__':
    main()
