---
paths:
  - "**/*.swift"
---

# Swift Security

Keep secrets in Keychain, not in code:

```swift
import Security

func storeAPIKey(_ key: String) throws {
    let data = key.data(using: .utf8)!
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: "api_key",
        kSecValueData as String: data,
    ]
    SecItemAdd(query as CFDictionary, nil)
}
```

Validate all input from network or user.
