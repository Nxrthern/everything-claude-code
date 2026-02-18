---
paths:
  - "**/*.php"
---

# PHP Coding Style

Follow **PSR-12** (Extended Coding Style) and use **PHP-CS-Fixer**.

## Conventions

- Use 4-space indentation
- Use `camelCase` for methods and properties
- Use `PascalCase` for classes and interfaces
- Use `CONSTANT_CASE` for constants
- Use `snake_case` for database columns

## Type Declarations

Always use return type declarations:

```php
<?php

class User {
    private string $name;
    private string $email;
    
    public function getName(): string {
        return $this->name;
    }
    
    public function setEmail(string $email): void {
        $this->email = $email;
    }
}
```

## Error Handling

Use exceptions:

```php
<?php

class ValidationException extends Exception {}

function validateEmail(string $email): void {
    if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
        throw new ValidationException("Invalid email");
    }
}
```

## Formatting

- Use **php-cs-fixer** to fix style issues
- Use **phpstan** for static analysis
- Use **psalm** for type checking
