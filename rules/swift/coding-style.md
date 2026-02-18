---
paths:
  - "**/*.swift"
---

# Swift Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with Swift-specific content.

## Standards

- Follow **Apple Swift API Design Guidelines**
- Use **SwiftFormat** for automatic formatting
- Use **SwiftLint** for linting
- Use **value types** (structs) by default, classes only when needed

## Immutability

Prefer immutable types:

```swift
struct User {
    let id: Int
    let name: String
    let email: String
}

class MutableContainer {
    private(set) var data: [String] = []
    
    func add(_ item: String) {
        data.append(item)
    }
}
```

## Error Handling

Use `Result` or throwing functions:

```swift
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
}

func fetchUser(id: Int) throws -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw NetworkError.invalidURL
    }
    // ...
}
```

## Protocols for Abstraction

Use protocols instead of inheritance:

```swift
protocol Repository {
    func get(id: Int) async throws -> User
    func save(_ user: User) async throws
}
```

## Reference

See skill: `swiftui-expert-skill` for comprehensive Swift patterns.
