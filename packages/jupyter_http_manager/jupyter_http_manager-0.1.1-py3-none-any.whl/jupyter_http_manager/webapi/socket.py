"""Utility functions to get an open socket."""

import socket


def find_free_port():
    """Get an open port that we can use for the jupyter server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))  # 0 means "pick an available port"
    port = s.getsockname()[1]
    s.close()
    return port


def main():
    """Find a free socket on this OS."""
    print(find_free_port())
