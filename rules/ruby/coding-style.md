---
paths:
  - "**/*.rb"
---

# Ruby Coding Style

Follow **Ruby Style Guide** and use **RuboCop** for enforcement.

## Conventions

- Use 2-space indentation
- Use `snake_case` for variables and methods
- Use `PascalCase` for classes and modules
- Use `CONSTANT` for constants
- Prefer double-quoted strings (interpolation-friendly)

## Immutability

Use `freeze` to prevent mutations:

```ruby
USERS = [
  { name: 'Alice', role: 'admin' },
  { name: 'Bob', role: 'user' }
].freeze
```

## Error Handling

Use custom exceptions:

```ruby
class ValidationError < StandardError; end

def validate_email(email)
  raise ValidationError, "Invalid email" unless email.include?('@')
end
```

## Formatting

- Use **RuboCop** for linting
- Use **Prettier** for Ruby files (via prettier-plugin-ruby)
