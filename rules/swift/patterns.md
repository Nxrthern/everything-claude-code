---
paths:
  - "**/*.swift"
---

# Swift Patterns

## Actors for Thread-Safe State

```swift
actor UserStore {
    private var users: [Int: User] = [:]
    
    func getUser(id: Int) -> User? {
        users[id]
    }
    
    func setUser(_ user: User) {
        users[user.id] = user
    }
}
```

See skill: `swift-actor-persistence` for persistence patterns with actors.
