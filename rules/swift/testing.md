---
paths:
  - "**/*.swift"
---

# Swift Testing

Use XCTest for unit tests:

```swift
final class UserServiceTests: XCTestCase {
    var service: UserService!
    
    override func setUp() {
        super.setUp()
        service = UserService()
    }
    
    func testFetchUser() async throws {
        let user = try await service.fetchUser(id: 1)
        XCTAssertNotNil(user)
    }
}
```

Target: 80%+ coverage for core logic.
