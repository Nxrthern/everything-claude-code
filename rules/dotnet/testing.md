---
paths:
  - "**/*.cs"
---

# C# / .NET Testing

> Test-driven development with C# and .NET.

## Unit Tests with xUnit

```csharp
public class UserServiceTests
{
    private readonly UserService _service;
    private readonly Mock<IUserRepository> _repoMock;

    public UserServiceTests()
    {
        _repoMock = new Mock<IUserRepository>();
        _service = new UserService(_repoMock.Object);
    }

    [Fact]
    public async Task GetUserAsync_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = 1;
        var expected = new User { Id = userId, Name = "John" };
        _repoMock.Setup(r => r.GetByIdAsync(userId))
            .ReturnsAsync(expected);

        // Act
        var result = await _service.GetUserAsync(userId);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(expected.Name, result.Name);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetUserAsync_WithInvalidId_ThrowsException(int id)
    {
        await Assert.ThrowsAsync<ArgumentException>(
            () => _service.GetUserAsync(id)
        );
    }
}
```

## Integration Tests

Test with TestServer:

```csharp
public class UserControllerTests : IClassFixture<WebApplicationFactory<Startup>>
{
    private readonly WebApplicationFactory<Startup> _factory;

    public UserControllerTests(WebApplicationFactory<Startup> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task GetUser_ReturnsOkResult()
    {
        var client = _factory.CreateClient();
        var response = await client.GetAsync("/api/users/1");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

## Database Testing with TestContainers

```csharp
public class UserRepositoryTests : IAsyncLifetime
{
    private readonly MsSqlContainer _container = new MsSqlBuilder()
        .WithPassword("Strong@Password")
        .Build();

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
    }

    public async Task DisposeAsync()
    {
        await _container.StopAsync();
    }

    [Fact]
    public async Task SaveUser_PersistsToDatabase()
    {
        var connectionString = _container.GetConnectionString();
        using var context = new DbContext(connectionString);
        var repo = new UserRepository(context);

        var user = new User { Name = "John", Email = "john@example.com" };
        await repo.AddAsync(user);

        var retrieved = await repo.GetByIdAsync(user.Id);
        Assert.NotNull(retrieved);
    }
}
```

## Test Coverage

Target: **80%+ coverage** for core logic.

Use OpenCover:

```bash
dotnet test /p:CollectCoverageMetrics=true
```

## Reference

See skill: `springboot-tdd` for broader TDD patterns.
