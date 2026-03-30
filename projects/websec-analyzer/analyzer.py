#!/usr/bin/env python3
"""
Domain Security Analyzer
Options:
1. Response Headers
2. Security Headers
3. Cookie Analysis
4. TLS Analysis
5. DNS Records
6. WHOIS Information
7. Special Files
8. All
"""

import ssl
import socket
import datetime
import sys
import tempfile
import os
import json
from urllib.parse import urlparse

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def separator(title):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


def ok(label, value):
    print(f"  [+] {label}: {value}")


def warn(label, value):
    print(f"  [!] {label}: {value}")


def err(label, value):
    print(f"  [-] {label}: {value}")


def clean_domain(target):
    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    parsed = urlparse(target)
    domain = parsed.netloc or parsed.path
    scheme = parsed.scheme or "https"

    if ":" in domain:
        domain = domain.split(":")[0]

    return domain, scheme


def make_request(url):
    try:
        response = requests.get(
            url,
            verify=False,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "DomainAnalyzer/1.0"}
        )
        return response
    except requests.exceptions.RequestException as e:
        err("Request failed", str(e))
        return None


def decode_cert_from_binary(cert_bin):
    temp_path = None
    try:
        pem_data = ssl.DER_cert_to_PEM_cert(cert_bin)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pem", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(pem_data)
            temp_path = temp_file.name

        cert_dict = ssl._ssl._test_decode_cert(temp_path)
        return cert_dict
    except Exception as e:
        return {"decode_error": str(e)}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def ask_to_save_json():
    answer = input("\nDo you want to save the results to a JSON file? (y/n): ").strip().lower()
    return answer in ["y", "yes", "s", "si", "sí"]


def save_json_report(report, domain):
    folder = "reports"

    if not os.path.exists(folder):
        os.makedirs(folder)

    safe_domain = domain.replace(".", "_")
    filename = f"{safe_domain}_analysis.json"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        ok("JSON saved", filepath)
    except Exception as e:
        err("JSON save error", str(e))


def show_menu():
    print("\nSelect the analysis you want to run:")
    print("1. Response Headers")
    print("2. Security Headers")
    print("3. Cookie Analysis")
    print("4. TLS Analysis")
    print("5. DNS Records")
    print("6. WHOIS Information")
    print("7. Special Files")
    print("8. All")
    print("\nExamples: 1 | 1,4,5 | 8")

def parse_user_selection(selection):
    selection = selection.replace(" ", "")
    parts = selection.split(",")

    valid = {"1", "2", "3", "4", "5", "6", "7", "8"}

    for part in parts:
        if part not in valid:
            return None

    if "8" in parts:
        return {"1", "2", "3", "4", "5", "6", "7"}

    return set(parts)


# ─────────────────────────────────────────────
# 1. RESPONSE HEADERS
# ─────────────────────────────────────────────

def get_response_headers(domain, scheme="https"):
    separator("RESPONSE HEADERS")
    url = f"{scheme}://{domain}"
    response = make_request(url)

    if not response:
        return {}

    headers_dict = dict(response.headers)

    for k, v in headers_dict.items():
        ok(k, v)

    return headers_dict


# ─────────────────────────────────────────────
# 2. SECURITY HEADER ANALYSIS
# ─────────────────────────────────────────────

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
]


def analyze_security_headers(headers):
    separator("SECURITY HEADER ANALYSIS")
    headers_lower = {k.lower(): v for k, v in headers.items()}
    results = {}

    for sh in SECURITY_HEADERS:
        val = headers_lower.get(sh.lower())
        if val:
            ok(sh, val)
            results[sh] = {"status": "Present", "value": val}
        else:
            warn(sh, "MISSING ⚠️")
            results[sh] = {"status": "Missing", "value": None}

    return results


# ─────────────────────────────────────────────
# 3. COOKIE ANALYSIS
# ─────────────────────────────────────────────

def analyze_cookies(domain, scheme="https"):
    separator("COOKIE ANALYSIS")
    url = f"{scheme}://{domain}"
    response = make_request(url)

    if not response:
        warn("Cookies", "Could not fetch cookies")
        return []

    cookies = response.cookies
    if not cookies:
        warn("Cookies", "No cookies found in response")
        return []

    cookies_result = []

    for cookie in cookies:
        cookie_data = {
            "name": cookie.name,
            "value_preview": str(cookie.value)[:30] + ("..." if len(str(cookie.value)) > 30 else ""),
            "httponly": bool(cookie.has_nonstandard_attr("HttpOnly") or cookie._rest.get("HttpOnly") is not None),
            "secure": bool(cookie.secure),
            "samesite": cookie._rest.get("SameSite", "Missing"),
            "domain": cookie.domain or "N/A",
            "path": cookie.path or "N/A",
            "expires": None
        }

        print(f"\n  Cookie: {cookie_data['name']} = {cookie_data['value_preview']}")
        ok("HttpOnly", "✅ Present" if cookie_data["httponly"] else "❌ Missing")
        ok("Secure", "✅ Present" if cookie_data["secure"] else "❌ Missing")
        ok("SameSite", f"✅ {cookie_data['samesite']}")
        ok("Domain", cookie_data["domain"])
        ok("Path", cookie_data["path"])

        if cookie.expires:
            exp = datetime.datetime.fromtimestamp(cookie.expires)
            cookie_data["expires"] = exp.strftime("%Y-%m-%d %H:%M:%S")
            ok("Expires", cookie_data["expires"])
        else:
            warn("Expires", "Session cookie (no expiry)")

        cookies_result.append(cookie_data)

    return cookies_result


# ─────────────────────────────────────────────
# 4. TLS ANALYSIS
# ─────────────────────────────────────────────

def analyze_tls(domain):
    separator("TLS ANALYSIS")

    tls_result = {
        "tls_version": None,
        "cipher_suite": None,
        "when_tls_expires": None,
        "days_left": None,
        "status": None,
        "subject_cn": None,
        "issued_by": None,
        "sans": [],
        "error": None
    }

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((domain, 443), timeout=10) as raw_sock:
            with context.wrap_socket(raw_sock, server_hostname=domain) as tls_sock:
                tls_result["tls_version"] = tls_sock.version()
                ok("TLS Version", tls_result["tls_version"])

                cipher = tls_sock.cipher()
                if cipher:
                    tls_result["cipher_suite"] = f"{cipher[0]} ({cipher[1]}, {cipher[2]} bits)"
                    ok("Cipher Suite", tls_result["cipher_suite"])
                else:
                    warn("Cipher Suite", "Not available")

                cert_bin = tls_sock.getpeercert(binary_form=True)

                if not cert_bin:
                    warn("Certificate", "No certificate binary data available")
                    tls_result["error"] = "No certificate binary data available"
                    return tls_result

                cert = decode_cert_from_binary(cert_bin)

                if "decode_error" in cert:
                    warn("Certificate decode", cert["decode_error"])
                    tls_result["error"] = cert["decode_error"]
                    return tls_result

                expire_str = cert.get("notAfter")
                if expire_str:
                    try:
                        exp_date = datetime.datetime.strptime(
                            expire_str,
                            "%b %d %H:%M:%S %Y %Z"
                        )
                        days_left = (exp_date - datetime.datetime.utcnow()).days

                        tls_result["when_tls_expires"] = exp_date.strftime("%Y-%m-%d %H:%M:%S UTC")
                        tls_result["days_left"] = days_left

                        if days_left > 30:
                            status = "VALID"
                        elif days_left > 0:
                            status = "EXPIRING SOON"
                        else:
                            status = "EXPIRED"

                        tls_result["status"] = status

                        ok(
                            "When TLS expires",
                            f"{tls_result['when_tls_expires']} → {days_left} days left {status}"
                        )
                    except Exception as e:
                        warn("When TLS expires", f"Could not parse expiration date: {e}")
                        tls_result["error"] = f"Could not parse expiration date: {e}"
                else:
                    warn("When TLS expires", "No expiration date found in certificate")
                    tls_result["error"] = "No expiration date found in certificate"

                subject = cert.get("subject", ())
                issuer = cert.get("issuer", ())
                san = cert.get("subjectAltName", ())

                cn = "N/A"
                for item in subject:
                    for key, value in item:
                        if key == "commonName":
                            cn = value

                issuer_org = "N/A"
                for item in issuer:
                    for key, value in item:
                        if key == "organizationName":
                            issuer_org = value

                sans = [value for key, value in san if key == "DNS"]

                tls_result["subject_cn"] = cn
                tls_result["issued_by"] = issuer_org
                tls_result["sans"] = sans

                ok("Subject CN", cn)
                ok("Issued by", issuer_org)

                if sans:
                    ok("SANs", ", ".join(sans[:5]) + ("..." if len(sans) > 5 else ""))
                else:
                    warn("SANs", "Not available")

    except ssl.SSLError as e:
        err("TLS Error", f"SSL error: {e}")
        tls_result["error"] = f"SSL error: {e}"
    except socket.timeout:
        err("TLS Error", "Connection timed out")
        tls_result["error"] = "Connection timed out"
    except socket.gaierror:
        err("TLS Error", "Could not resolve domain")
        tls_result["error"] = "Could not resolve domain"
    except Exception as e:
        err("TLS Error", str(e))
        tls_result["error"] = str(e)

    return tls_result


# ─────────────────────────────────────────────
# 5. DNS RECORDS
# ─────────────────────────────────────────────

def query_dns(domain, record_type):
    if not DNS_AVAILABLE:
        if record_type == "A":
            try:
                return [socket.gethostbyname(domain)]
            except Exception:
                return []
        return []

    try:
        answers = dns.resolver.resolve(domain, record_type, raise_on_no_answer=False)
        return [str(r) for r in answers]
    except Exception:
        return []


def parse_dmarc(record):
    tags = {}
    for t in record.strip('"').split(";"):
        if "=" in t:
            key, value = t.split("=", 1)
            tags[key.strip()] = value.strip()

    policy = tags.get("p", "none")
    color = "✅" if policy == "reject" else "⚠️" if policy == "quarantine" else "❌"
    ok("Policy", f"{policy} {color}")

    result = {
        "policy": policy,
        "rua": tags.get("rua"),
        "ruf": tags.get("ruf")
    }

    if "rua" in tags:
        ok("Aggregate reports (rua)", tags["rua"])
    if "ruf" in tags:
        ok("Forensic reports (ruf)", tags["ruf"])

    return result


def analyze_dns(domain):
    separator("DNS RECORDS")

    dns_result = {
        "A": [],
        "AAAA": [],
        "MX": [],
        "TXT": [],
        "NS": [],
        "SPF": [],
        "DMARC": []
    }

    for rtype in ["A", "AAAA", "MX", "TXT", "NS"]:
        print(f"\n  ── {rtype} Records ──")
        records = query_dns(domain, rtype)
        dns_result[rtype] = records

        if records:
            for r in records:
                ok(rtype, r)
        else:
            warn(rtype, "No records found")

    print(f"\n  ── SPF Record ──")
    txt_records = dns_result["TXT"]
    spf = [r for r in txt_records if "v=spf1" in r.lower()]
    dns_result["SPF"] = spf

    if spf:
        ok("SPF", spf[0])
    else:
        warn("SPF", "Not found ⚠️")

    print(f"\n  ── DMARC Record ──")
    dmarc_records = query_dns(f"_dmarc.{domain}", "TXT")
    found = False

    for r in dmarc_records:
        if "v=dmarc1" in r.lower():
            ok("DMARC", r)
            parsed = parse_dmarc(r)
            dns_result["DMARC"].append({
                "record": r,
                "details": parsed
            })
            found = True

    if not found:
        warn("DMARC", "Not found ⚠️")

    return dns_result


# ─────────────────────────────────────────────
# 6. WHOIS INFORMATION
# ─────────────────────────────────────────────

def analyze_whois(domain):
    separator("WHOIS INFORMATION")

    whois_result = {
        "registrar": None,
        "whois_server": None,
        "name_servers": None,
        "country": None,
        "organization": None,
        "creation_date": None,
        "expiration_date": None,
        "error": None
    }

    if not WHOIS_AVAILABLE:
        warn("WHOIS", "python-whois not installed — pip install python-whois")
        whois_result["error"] = "python-whois not installed"
        return whois_result

    try:
        w = whois.whois(domain)

        whois_result["registrar"] = w.registrar or "N/A"
        whois_result["whois_server"] = w.whois_server or "N/A"

        if isinstance(w.name_servers, list):
            whois_result["name_servers"] = w.name_servers
            ok("Name Servers", ", ".join(w.name_servers))
        else:
            whois_result["name_servers"] = str(w.name_servers or "N/A")
            ok("Name Servers", whois_result["name_servers"])

        whois_result["country"] = w.country or "N/A"
        whois_result["organization"] = getattr(w, "org", None) or getattr(w, "organization", None) or "N/A"

        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        expiration_date = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date

        whois_result["creation_date"] = str(creation_date or "N/A")
        whois_result["expiration_date"] = str(expiration_date or "N/A")

        ok("Registrar", whois_result["registrar"])
        ok("WHOIS Server", whois_result["whois_server"])
        ok("Country", whois_result["country"])
        ok("Organization", whois_result["organization"])
        ok("Creation Date", whois_result["creation_date"])
        ok("Expiration Date", whois_result["expiration_date"])

    except Exception as e:
        err("WHOIS Error", str(e))
        whois_result["error"] = str(e)

    return whois_result


# ─────────────────────────────────────────────
# 7. SPECIAL FILES
# ─────────────────────────────────────────────

SPECIAL_FILES = [
    "/robots.txt",
    "/sitemap.xml",
    "/.well-known/security.txt",
    "/security.txt",
    "/.env",
    "/crossdomain.xml",
    "/clientaccesspolicy.xml",
    "/.git/HEAD",
    "/wp-login.php",
    "/admin",
    "/phpinfo.php",
]


def check_special_files(domain, scheme="https"):
    separator("SPECIAL FILES")
    special_files_result = []

    for path in SPECIAL_FILES:
        url = f"{scheme}://{domain}{path}"

        try:
            r = requests.get(
                url,
                verify=False,
                timeout=8,
                allow_redirects=True,
                headers={"User-Agent": "DomainAnalyzer/1.0"}
            )

            sensitive = path in ["/.env", "/.git/HEAD", "/phpinfo.php"]
            flag = " 🚨 SENSITIVE" if sensitive and r.status_code == 200 else ""
            size = len(r.content)

            ok(path, f"HTTP {r.status_code} ({size} bytes){flag}")

            special_files_result.append({
                "path": path,
                "url": url,
                "status_code": r.status_code,
                "size_bytes": size,
                "sensitive": sensitive and r.status_code == 200
            })

        except requests.exceptions.RequestException:
            warn(path, "Unreachable / timeout")
            special_files_result.append({
                "path": path,
                "url": url,
                "status_code": None,
                "size_bytes": None,
                "sensitive": False,
                "error": "Unreachable / timeout"
            })

    return special_files_result


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def analyze(target):
    domain, scheme = clean_domain(target)

    print(f"\n{'█' * 60}")
    print(f"  🔍 DOMAIN SECURITY ANALYZER")
    print(f"  Target : {domain}")
    print(f"  Scheme : {scheme}")
    print(f"  Time   : {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"{'█' * 60}")

    show_menu()

    selected_options = None
    while selected_options is None:
        user_input = input("\nEnter your choice: ").strip()
        selected_options = parse_user_selection(user_input)
        if selected_options is None:
            print("Invalid option. Try again.")

    report = {
        "target": domain,
        "scheme": scheme,
        "time_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    headers = {}

    if "1" in selected_options:
        headers = get_response_headers(domain, scheme)
        report["response_headers"] = headers

    if "2" in selected_options:
        if not headers:
            headers = get_response_headers(domain, scheme)
        report["security_header_analysis"] = analyze_security_headers(headers)

    if "3" in selected_options:
        report["cookie_analysis"] = analyze_cookies(domain, scheme)

    if "4" in selected_options:
        report["tls_analysis"] = analyze_tls(domain)

    if "5" in selected_options:
        report["dns_records"] = analyze_dns(domain)

    if "6" in selected_options:
        report["whois_information"] = analyze_whois(domain)

    if "7" in selected_options:
        report["special_files"] = check_special_files(domain, scheme)

    print(f"\n{'═' * 60}")
    print(f"  ✅ Analysis complete for {domain}")
    print(f"{'═' * 60}\n")

    if ask_to_save_json():
        save_json_report(report, domain)
    else:
        print("JSON file was not generated.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <domain>")
        print("Example: python analyzer.py banreservas.com.do")
        sys.exit(1)

    analyze(sys.argv[1])