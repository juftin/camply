"""
CloudFront Edge Connection Session for Recreation.gov
=====================================================
Maintains low-latency, warm HTTPS connection pools pinned to the local AWS
CloudFront edge node (SFO, ~19-50ms RTT) for cache-aligned campsite availability
polling with zero connection handshake overhead.
"""

import json
import logging
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class CloudFrontRateLimitError(ConnectionError):
    """Raised when CloudFront returns HTTP 429 Too Many Requests."""
    pass


class CloudFrontEdgeSession:
    """
    Manages persistent HTTPS connection pool pinned to local SFO CloudFront edge node.
    """

    TARGET_HOST = "www.recreation.gov"
    CLOUDFRONT_DOMAIN = "d339229sl9sepr.cloudfront.net"

    # Known stable edge IPs and representative subnet for fast DoH recovery
    PRIMARY_IP = "18.155.202.79"
    FALLBACK_IPS = ["18.155.202.55", "18.155.202.24", "18.155.202.127"]
    SFO_SUBNET = "198.27.128.0/24"

    def __init__(self, connect_timeout: float = 3.0, read_timeout: float = 6.0):
        self.timeout = urllib3.Timeout(connect=connect_timeout, read=read_timeout)
        self._current_ip = self.PRIMARY_IP
        self._pool = urllib3.HTTPSConnectionPool(
            self._current_ip,
            port=443,
            server_hostname=self.TARGET_HOST,
            timeout=self.timeout,
            maxsize=2,
        )
        self._doh_pool: Optional[urllib3.HTTPSConnectionPool] = None

    def _resolve_fresh_ip(self) -> str:
        """Resolve a fresh edge IP using Google DoH with SFO EDNS Client Subnet."""
        url = f"/resolve?name={self.CLOUDFRONT_DOMAIN}&type=A&edns_client_subnet={self.SFO_SUBNET}"

        if self._doh_pool is None:
            self._doh_pool = urllib3.HTTPSConnectionPool("dns.google", port=443, maxsize=2)

        try:
            r = self._doh_pool.request("GET", url, timeout=urllib3.Timeout(connect=2.0, read=3.0))
            if r.status == 200:
                data = json.loads(r.data.decode("utf-8"))
                ips = [ans["data"] for ans in data.get("Answer", []) if ans.get("type") == 1]
                if ips:
                    return random.choice(ips)
        except Exception as e:
            logger.warning(f"DoH resolution failed for SFO: {e}")

        # Fallback to predefined pool
        return random.choice(self.FALLBACK_IPS)

    def _rotate_pool(self) -> None:
        """Refresh connection pool with a freshly resolved edge IP."""
        try:
            self._pool.close()
        except Exception:
            pass

        self._current_ip = self._resolve_fresh_ip()
        self._pool = urllib3.HTTPSConnectionPool(
            self._current_ip,
            port=443,
            server_hostname=self.TARGET_HOST,
            timeout=self.timeout,
            maxsize=2,
        )

    def get_monthly_availability(
        self,
        campground_id: int,
        month: datetime,
    ) -> Tuple[dict, dict]:
        """
        Query monthly availability from local CloudFront edge node.

        Returns
        -------
        Tuple[dict, dict]
            (availability_dict, metadata_dict)
            where metadata_dict has keys: cf_pop, x_cache, age, latency_ms, ip
        """
        raw_month = month.strftime("%Y-%m-01T00:00:00.000Z")
        encoded_month = raw_month.replace(":", "%3A")
        endpoint = f"/api/camps/availability/campground/{campground_id}/month?start_date={encoded_month}"

        headers = {
            "Host": self.TARGET_HOST,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": f"https://www.recreation.gov/camping/campgrounds/{campground_id}",
        }

        t0 = time.time()
        try:
            r = self._pool.request("GET", endpoint, headers=headers)
        except Exception as e:
            logger.warning(f"Connection error to SFO edge ({self._current_ip}): {e}. Rotating edge IP...")
            self._rotate_pool()
            t0 = time.time()
            r = self._pool.request("GET", endpoint, headers=headers)

        latency_ms = (time.time() - t0) * 1000

        if r.status == 429:
            retry_after = r.headers.get("retry-after", "N/A")
            cf_id = r.headers.get("x-amz-cf-id", "N/A")
            server = r.headers.get("server", "CloudFront")
            raise CloudFrontRateLimitError(
                f"Recreation.gov API returned status 429 (Too Many Requests) via SFO "
                f"[Server: {server}, Retry-After: {retry_after}, CF-ID: {cf_id}]"
            )
        elif r.status != 200:
            error_body = r.data.decode("utf-8", errors="ignore")[:200]
            raise ConnectionError(
                f"Recreation.gov API returned status {r.status} via SFO: {error_body}"
            )

        data = json.loads(r.data.decode("utf-8"))
        age_header = r.headers.get("age")
        age = int(age_header) if age_header and age_header.isdigit() else 0

        metadata = {
            "cf_pop": r.headers.get("x-amz-cf-pop", "UNKNOWN"),
            "x_cache": r.headers.get("x-cache", "UNKNOWN"),
            "age": age,
            "latency_ms": round(latency_ms, 1),
            "ip": self._current_ip,
        }

        return data, metadata
