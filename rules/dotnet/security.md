---
paths:
  - "**/*.cs"
---

# C# / .NET Security

> Security best practices for .NET applications.

## Secrets Management

Never store secrets in code or config files:

```csharp
// ✅ Good: Use User Secrets for development
var builder = WebApplication.CreateBuilder(args);
builder.Configuration.AddUserSecrets<Program>();

// In production, use Azure Key Vault
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential()
);
```

## Input Validation

Validate all input with data annotations:

```csharp
public class User
{
    [Required]
    [StringLength(100)]
    public string Name { get; set; }

    [Required]
    [EmailAddress]
    public string Email { get; set; }

    [Range(18, 120)]
    public int Age { get; set; }
}
```

## SQL Injection Prevention

Always use parameterized queries with Entity Framework:

```csharp
// ✅ Safe: Entity Framework parameterizes automatically
var users = await _context.Users
    .Where(u => u.Email == email)
    .ToListAsync();

// ✅ Safe: Explicit parameters
var user = await _context.Users.FromSqlInterpolated(
    $"SELECT * FROM Users WHERE Id = {id}"
).FirstOrDefaultAsync();

// ❌ Never do this:
// var query = $"SELECT * FROM Users WHERE Email = '{email}'";
```

## Authentication

Use ASP.NET Core Identity:

```csharp
services.AddIdentity<User, Role>()
    .AddEntityFrameworkStores<DbContext>()
    .AddDefaultTokenProviders();

services.AddAuthentication()
    .AddCookie()
    .AddOpenIdConnect("oidc", options =>
    {
        options.Authority = "https://auth.example.com";
    });
```

## Authorization

Use role-based or policy-based authorization:

```csharp
[Authorize(Roles = "Admin")]
public async Task<IActionResult> DeleteUser(int id)
{
    await _userService.DeleteAsync(id);
    return Ok();
}

// Or with policies
[Authorize(Policy = "AdminOrModerator")]
public async Task<IActionResult> BanUser(int id)
{
    // ...
}
```

## Dependency Updates

Keep packages current:

```bash
dotnet outdated
dotnet package update
```

## CORS Configuration

Restrict cross-origin requests:

```csharp
services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigin", builder =>
    {
        builder
            .WithOrigins("https://trusted.example.com")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials();
    });
});
```

## Reference

See skill: `springboot-security` for broader security patterns.
