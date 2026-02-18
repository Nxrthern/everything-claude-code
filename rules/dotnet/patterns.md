---
paths:
  - "**/*.cs"
---

# C# / .NET Patterns

> Essential .NET patterns for enterprise applications.

## Dependency Injection

Built into ASP.NET Core:

```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddTransient<IEmailService, EmailService>();
    services.AddSingleton<IConfig>(new Config());
}

public class UserService
{
    private readonly IUserRepository _repo;
    
    public UserService(IUserRepository repo) => _repo = repo;
}
```

## Repository Pattern

Abstract data access:

```csharp
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}
```

## Options Pattern

Strongly-typed configuration:

```csharp
public class ApiOptions
{
    public string BaseUrl { get; set; }
    public int Timeout { get; set; }
    public string ApiKey { get; set; }
}

// In Startup.cs
services.Configure<ApiOptions>(Configuration.GetSection("Api"));

// In service
public class ApiClient
{
    private readonly ApiOptions _options;
    
    public ApiClient(IOptions<ApiOptions> options)
    {
        _options = options.Value;
    }
}
```

## Middleware Pipeline

Build request pipelines:

```csharp
app.UseMiddleware<ExceptionHandlingMiddleware>();
app.UseMiddleware<LoggingMiddleware>();
app.UseRouting();
app.UseEndpoints(endpoints =>
{
    endpoints.MapControllers();
});
```

## Reference

See skill: `jpa-patterns` for data layer patterns (Entity/Repository/UnitOfWork concepts apply to .NET).
