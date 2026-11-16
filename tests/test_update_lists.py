import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('update_lists', ROOT / 'scripts/update_lists.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


def fixture(url):
    name = 'telegram.txt' if url.endswith('cidr.txt') else url.rsplit('/', 1)[1]
    return (ROOT / 'tests/fixtures' / name).read_text(encoding='utf-8')


class UpdateTests(unittest.TestCase):
    def test_build_preserves_manual_entries_and_scopes(self):
        result = updater.build(ROOT, fixture)
        domains = result['domains.json']['rules'][0]
        self.assertIn('imo.im', domains['domain_suffix'])
        self.assertIn('githubcopilot.com', domains['domain_suffix'])
        self.assertIn('github-api.arkoselabs.com', domains['domain'])
        rules = result['facetime-ip.json']['rules']
        self.assertIn('5.150.156.0/22', rules[0]['ip_cidr'])
        self.assertEqual(rules[1]['port_range'], ['3478:3497', '16384:16387', '16393:16402'])
        self.assertEqual(rules[2]['network'], ['udp'])
        self.assertIn('91.108.12.0/22', rules[2]['ip_cidr'])
        self.assertEqual(result, updater.build(ROOT, fixture))

    def test_bad_upstream_is_rejected(self):
        for value in ['', '<html>Error</html>', '0.0.0.0/0', '127.0.0.0/8']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                updater.telegram(value)
        with self.assertRaises(ValueError):
            updater.geosite(['github'], lambda _: 'regexp:.*')
        with self.assertRaises(ValueError):
            updater.geosite(['github'], lambda _: 'include:github')

    def test_download_failure_does_not_write_outputs(self):
        before = (ROOT / 'domains.json').read_bytes()
        def fail(url):
            if url.endswith('cidr.txt'):
                raise OSError('Unavailable')
            return fixture(url)
        with self.assertRaises(OSError):
            updater.build(ROOT, fail)
        self.assertEqual(before, (ROOT / 'domains.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
