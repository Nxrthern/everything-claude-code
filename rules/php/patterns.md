---
paths:
  - "**/*.php"
---

# PHP Patterns

## Dependency Injection Container

```php
<?php

class Container {
    private array $bindings = [];
    
    public function bind(string $key, callable $resolver): void {
        $this->bindings[$key] = $resolver;
    }
    
    public function resolve(string $key) {
        return $this->bindings[$key]($this);
    }
}
```

## Data Transfer Objects

```php
<?php

class UserDTO {
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email,
    ) {}
}
```
