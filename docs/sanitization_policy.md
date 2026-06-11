# Sanitization Policy

This repository is designed for public sharing. It must remain free of any
information that can identify a private automation target, source, issuer, or
account.

## Allowed

- generic placeholders such as `SOURCE_A`, `SOURCE_B`, and `ASSET_001`
- method descriptions
- pseudocode and reusable skeleton code
- synthetic sample rows
- local-only folder conventions
- dry-run and validation logic

## Not Allowed

- real source names
- real issuer names
- real domains, URLs, login pages, or admin paths
- private API endpoints
- session cookies, tokens, passwords, or account identifiers
- raw crawled PDFs or production spreadsheets
- screenshots of internal pages
- logs copied from production runs

## Review Checklist

Before publishing changes:

1. Search for private names and domains.
2. Search for secret-like strings.
3. Confirm sample data is synthetic.
4. Confirm configs use placeholders only.
5. Confirm scripts default to dry-run behavior.

Suggested local scan:

```powershell
rg -n -i "password|token|secret|cookie|session|api[_-]?key|login|admin|real_url|private" .
```
