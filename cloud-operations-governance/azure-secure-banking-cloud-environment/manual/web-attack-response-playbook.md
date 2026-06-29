# Web Login Abuse Response Playbook

### Scenario

A high number of requests was detected against the /login endpoint.

### Severity

Medium to High

### Detection Sources

- Nginx access.log
- Nginx error.log
- Rate limiting responses
- Azure monitoring
- Defender for Cloud recommendations

### Response Steps

1. Identify the source IP.
2. Review Nginx access logs.
3. Confirm rate limiting behavior.
4. Temporarily block abusive IPs if needed.
5. Review application authentication controls.
6. Recommend WAF for production.
7. Document the incident.

### Preventive Controls

- Nginx rate limiting
- MFA
- Account lockout policy
- Azure WAF
- Bot protection