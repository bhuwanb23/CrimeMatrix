# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability in CrimeMatrix, please report it responsibly:

1. **Do NOT** open a public GitHub issue
2. Email security concerns to: [your-security-email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

---

## Data Handling

CrimeMatrix is designed for law enforcement use and handles sensitive data:

### Data Sensitivity

- Crime records contain personal information (names, addresses, phone numbers)
- Investigation data may be legally sensitive
- AI reasoning chains may reveal investigative strategies

### Data Protection Measures

- All data is stored locally (SQLite database)
- No data is sent to external services unless explicitly configured (cloud AI providers)
- Ollama runs locally — no data leaves the machine by default
- Session data is stored in-memory and can be cleared at any time

### When Using Cloud AI Providers

If you configure OpenAI or Gemini as AI providers:
- Queries and responses may be processed by external services
- Review the provider's data retention policies
- Consider using Ollama for sensitive investigations
- Never include classified or operationally sensitive information in AI queries

---

## Authentication & Authorization

CrimeMatrix currently does not implement authentication or authorization. This is by design for demo purposes.

For production deployment:

1. Add authentication middleware (OAuth2, JWT, etc.)
2. Implement role-based access control (RBAC)
3. Add audit logging for all data access
4. Use HTTPS for all API communication
5. Restrict CORS to known origins

---

## Dependency Security

Regularly update dependencies to patch known vulnerabilities:

```bash
# Check for vulnerable Python packages
pip install safety
safety check -r backend/requirements.txt
safety check -r ai-services/requirements.txt

# Check for vulnerable npm packages
cd frontend
npm audit
```

---

## Network Security

### Development

- CORS is set to `allow_origins=["*"]` for development convenience
- All services bind to `0.0.0.0` for Docker compatibility

### Production

- Restrict CORS to specific origins
- Use a reverse proxy (nginx, Caddy) for TLS termination
- Firewall rules to restrict access to API ports
- Use Docker networks for inter-service communication

---

## Logging & Audit

CrimeMatrix includes audit middleware that logs:

- All API requests and responses
- User actions (searches, investigations, bookmarks)
- AI tool invocations
- Reasoning traces

Audit logs are stored in the database and can be reviewed for security incidents.

---

## Known Limitations

1. **No authentication** — Anyone with network access can use the API
2. **No rate limiting** — APIs can be overwhelmed with requests
3. **No input validation beyond Pydantic** — Additional validation may be needed for production
4. **SQLite write locks** — Concurrent writes may fail under high load
5. **In-memory caches** — Data is lost on restart

These are acceptable for demo purposes but should be addressed for production deployment.
