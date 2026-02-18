---
paths:
  - "**/*.cs"
  - "**/*.csproj"
---

# C# / .NET Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with C#/.NET-specific content.

## Standards

- Follow **Microsoft C# Coding Conventions**
- Use **nullable reference types** (`#nullable enable`)
- Use **LINQ** for collections and queries
- Use **records** for immutable data types (C# 9+)

## Immutability

Prefer immutable records:

```csharp
public record User(string Name, string Email);

public record Address(
    string Street,
    string City,
    string ZipCode
);

// With init-only properties
public record Product
{
    public int Id { get; init; }
    public string Name { get; init; }
    public decimal Price { get; init; }
}
```

## Error Handling

Use exceptions for exceptional cases:

```csharp
public async Task<User> GetUserAsync(int id)
{
    if (id <= 0)
        throw new ArgumentException("ID must be positive", nameof(id));

    var user = await _repository.FindAsync(id);
    if (user == null)
        throw new NotFoundException($"User {id} not found");

    return user;
}
```

## Formatting

- **CamelCase** for local variables and parameters
- **PascalCase** for properties, methods, and classes
- **_camelCase** for private fields
- Use `editorconfig` for consistency

## Async/Await

Always use async:

```csharp
public async Task<List<User>> GetUsersAsync()
{
    return await _context.Users.ToListAsync();
}

// Avoid `.Result` or `.Wait()` - can cause deadlocks
```

## Reference

See skill: `springboot-patterns` for architectural patterns (many apply to ASP.NET Core).
