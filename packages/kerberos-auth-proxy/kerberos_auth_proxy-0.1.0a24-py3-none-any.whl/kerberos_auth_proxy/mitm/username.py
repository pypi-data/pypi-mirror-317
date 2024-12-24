from logging import getLogger
import re
from typing import Optional

from mitmproxy.http import HTTPFlow


LOGGER = getLogger(__name__)
USERNAME_PATTERN = re.compile(r'[a-z_][a-z0-9_]*')


def get_username(flow: HTTPFlow, default_username: Optional[str] = None) -> Optional[str]:
    proxy_auth = flow.metadata.get("proxyauth")
    if not proxy_auth or not proxy_auth[0]:
        if default_username:
            return default_username
        LOGGER.debug("no authenticated user via proxyauth")
        return

    username = proxy_auth[0]
    if not USERNAME_PATTERN.match(username):
        LOGGER.warning("invalid username in proxyauth: %r", username)
        return

    return username
