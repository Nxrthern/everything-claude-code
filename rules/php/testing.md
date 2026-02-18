---
paths:
  - "**/*.php"
---

# PHP Testing

Use **PHPUnit** for testing:

```php
<?php

class UserServiceTest extends TestCase {
    public function testGetUser(): void {
        $service = new UserService();
        $user = $service->getUser(1);
        
        $this->assertInstanceOf(User::class, $user);
    }
}
```

Run with:

```bash
./vendor/bin/phpunit
```

Target: 80%+ coverage using PCOV or Xdebug.
