from __future__ import annotations

import socket


def _assert_connectivity(host: str, port: int, timeout_seconds: int = 5) -> None:
    try:
        with socket.create_connection((host, port), timeout=timeout_seconds):
            return
    except OSError as error:
        raise RuntimeError(f"Unable to connect to {host}:{port}") from error


def main() -> int:
    _assert_connectivity("mongodb", 27017)
    _assert_connectivity("redis", 6379)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
