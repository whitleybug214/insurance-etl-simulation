from config.settings import get_connection_url

def test_connection_url_format():
    url = get_connection_url()
    assert url.startswith("postgresql://"), "Connection string must start with 'postgresql://'"
    assert "@" in url and ":" in url, "Connection string should contain username, password, host, and port"