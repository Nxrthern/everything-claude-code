---
name: encryption-strategies
description: Encryption at rest, in transit, and in use. Key management, envelope encryption, and compliance-driven crypto patterns. Use when implementing data encryption, managing keys, or meeting compliance requirements.
---

# Encryption Strategies

Encrypt everything. Manage keys carefully. Rotate regularly. The cost of encryption is always less than the cost of a breach.

## When to Activate

- Implementing data encryption (at rest, in transit, in use)
- Designing key management architecture
- Meeting compliance requirements (GDPR, HIPAA, SOX, PCI-DSS)
- Rotating encryption keys
- Reviewing crypto implementation for correctness

## Encryption Layers

| Layer | What | Standard | Implementation |
|-------|------|----------|---------------|
| At rest | Stored data | AES-256-GCM | Database TDE, disk encryption, object store encryption |
| In transit | Network data | TLS 1.3 | HTTPS, mTLS, gRPC TLS |
| In use | Processing data | Application-level | Field-level encryption, secure enclaves |

## Key Management

### Envelope Encryption
```
Master Key (in HSM/KMS — never leaves hardware)
    │
    └── Encrypts → Data Encryption Key (DEK)
                        │
                        └── Encrypts → Actual Data

Storage:
- Encrypted DEK stored alongside data
- Master key stays in KMS
- To decrypt: KMS decrypts DEK → DEK decrypts data
```

Benefits:
- Master key never exposed to application
- Rotate DEKs without re-encrypting all data
- Different DEKs per dataset/tenant for isolation

### Key Hierarchy
```
Root Key (HSM, air-gapped)
    ├── Master Key A (KMS, region 1)
    │   ├── DEK for user-service DB
    │   └── DEK for payment-service DB
    └── Master Key B (KMS, region 2)
        ├── DEK for analytics DB
        └── DEK for backup encryption
```

## Practical Implementation

### Field-Level Encryption
```go
// ✅ Encrypt sensitive fields before storage
func encryptPII(ctx context.Context, user *User) error {
    kms := getKMSClient()

    // Encrypt SSN with tenant-specific key
    encrypted, err := kms.Encrypt(ctx, &EncryptInput{
        KeyID:     "alias/pii-key-" + user.TenantID,
        Plaintext: []byte(user.SSN),
    })
    if err != nil {
        return fmt.Errorf("encrypt SSN: %w", err)
    }
    user.EncryptedSSN = encrypted.CiphertextBlob
    user.SSN = "" // clear plaintext

    return nil
}
```

### TLS Configuration
```go
// ✅ Enforce TLS 1.3 minimum
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS13,
    CipherSuites: []uint16{
        tls.TLS_AES_256_GCM_SHA384,
        tls.TLS_CHACHA20_POLY1305_SHA256,
    },
}
```

### mTLS Between Services
```go
// ✅ Both client and server present certificates
tlsConfig := &tls.Config{
    Certificates: []tls.Certificate{cert},
    ClientAuth:   tls.RequireAndVerifyClientCert,
    ClientCAs:    caCertPool,
    MinVersion:   tls.VersionTLS13,
}
```

## Key Rotation

### Rotation Strategy
```
Rotation lifecycle:
1. Generate new key version in KMS
2. New encryptions use new key version
3. Old data still decryptable (KMS handles version)
4. Background re-encrypt old data with new key (optional)
5. After grace period, disable old key version

Schedule:
- Data encryption keys: Rotate every 90 days
- TLS certificates: Rotate every 90 days (ACME auto-renewal)
- Signing keys: Rotate every 1 year
- Master keys: Rotate per compliance (typically 1 year)
```

### Zero-Downtime Rotation
```
Phase 1: Generate new key → Both old and new active
Phase 2: New writes use new key → Old key for reads only
Phase 3: Re-encrypt old data → All data on new key
Phase 4: Revoke old key → Only new key active
```

## Compliance Mapping

| Requirement | GDPR | HIPAA | PCI-DSS | SOX |
|------------|------|-------|---------|-----|
| Encrypt PII at rest | Required | Required | Required | Best practice |
| TLS for all transit | Required | Required | Required | Required |
| Key management | Required | Required | Required | Required |
| Audit key access | Required | Required | Required | Required |
| Right to erasure | Required | N/A | N/A | N/A |
| Key rotation | Best practice | Required | Required annually | Best practice |

## Crypto Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Rolling your own crypto | Subtle bugs, broken security | Use standard libraries (NaCl, libsodium) |
| ECB mode | Pattern preservation | Use GCM or CTR with authentication |
| MD5/SHA1 for passwords | Rainbow tables, collisions | bcrypt, argon2id, scrypt |
| Hardcoded encryption key | Key compromise = data compromise | KMS/HSM managed keys |
| Same key for all data | Single breach exposes all | Per-tenant or per-dataset keys |
| Key stored with encrypted data | Defeats the purpose | Separate key storage (KMS) |

---

**Remember**: Encryption without key management is security theater. The strength of your encryption is only as strong as your weakest key handling practice.
