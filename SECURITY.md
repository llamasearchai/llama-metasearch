# Security Policy

## Reporting a Vulnerability

We take the security of LlamaSearch AI software seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email security@llamasearch.ai** with details about the vulnerability
3. **Include the following information**:
   - Type of vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes (if known)

We will acknowledge receipt of your vulnerability report within 48 hours and send a more detailed response within 72 hours indicating next steps.

After the initial response, the security team will keep you informed about the progress towards a fix and full announcement. We may ask for additional information or guidance.

## Security Practices

This project implements the following security practices:

### Code Security

- **Static Analysis**: All code is scanned with security-focused static analysis tools
- **Dependency Scanning**: Regular scanning of dependencies for vulnerabilities
- **Pre-commit Hooks**: Security checks run before code is committed
- **Code Review**: All changes are reviewed with security in mind

### API Key Security

- **Encryption**: All stored API keys are encrypted at rest
- **Secure Storage**: Keys are stored in user-specific protected directories
- **Permission Controls**: Secure file permissions (0600) for sensitive files
- **No Hardcoded Keys**: No API keys are hardcoded in the codebase
- **Key Rotation**: Support for regular key rotation

### Development Security

- **CI/CD Security**: Automated security scanning in GitHub Actions
- **Secure Defaults**: Security features are enabled by default
- **Fail Secure**: Error cases default to secure options
- **Defense in Depth**: Multiple layers of security controls

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Updates

Security updates will be released as soon as possible after a vulnerability is confirmed. We will provide:

1. A security advisory on GitHub
2. An update to the latest version
3. Backports to all supported versions when possible

## Best Practices for Users

To ensure the security of your API keys when using this library:

1. **Keep the library updated**: Always use the latest version with security fixes
2. **Enable pre-commit hooks**: Prevent accidental key commits
3. **Implement key rotation**: Rotate your API keys regularly
4. **Use proper permissions**: Ensure files containing keys have proper permissions
5. **Validate security setup**: Run the `check_for_api_keys.py` tool regularly

## Security Architecture

For details on the security architecture of this project, see the [architecture documentation](docs/architecture.md).

## Responsible Disclosure

We believe in responsible disclosure and will work with security researchers to coordinate the disclosure of vulnerabilities. We appreciate your help in keeping our users secure. 