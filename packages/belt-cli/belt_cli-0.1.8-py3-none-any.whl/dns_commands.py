from dns.resolver import resolve_at


def dns_lookup(query: str, record_type: str, server: str, root: bool) -> str:
    answer = resolve_at(server, query, record_type)
    return answer.rrset


def dns_sec() -> str:
    return "dns_sec: Not yet implemented"


def dns_flush() -> str:
    return "dns_flush: Not yet implemented"
