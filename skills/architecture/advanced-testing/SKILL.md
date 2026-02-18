---
name: advanced-testing
description: Advanced testing strategies including property-based testing, chaos engineering, contract testing, fuzzing, and test architecture at scale. Use when designing test strategies beyond unit/integration/E2E basics.
---

# Advanced Testing Strategies

Good tests prove your system works. Great tests prove your system works in ways you didn't expect.

## When to Activate

- Designing test strategy for complex systems
- Implementing property-based or generative tests
- Planning chaos engineering experiments
- Setting up contract testing between services
- Reviewing test architecture for effectiveness

## Testing Pyramid — Extended

```
                    ╱╲
                   ╱  ╲         Chaos Tests
                  ╱    ╲        (Production resilience)
                 ╱──────╲
                ╱        ╲      Contract Tests
               ╱          ╲    (Service boundaries)
              ╱────────────╲
             ╱              ╲   E2E Tests
            ╱                ╲  (Critical flows)
           ╱──────────────────╲
          ╱                    ╲ Integration Tests
         ╱                      ╲(Components together)
        ╱────────────────────────╲
       ╱                          ╲ Property-Based Tests
      ╱                            ╲(Invariant verification)
     ╱──────────────────────────────╲
    ╱                                ╲ Unit Tests
   ╱                                  ╲(Fast, isolated)
  ╱────────────────────────────────────╲
```

## Property-Based Testing

Instead of specific examples, define properties that must always hold:

### Concept
```
Example-based: add(2, 3) == 5
Property-based: for all a, b: add(a, b) == add(b, a)  [commutativity]
```

### Common Properties

| Property | Description | Example |
|----------|------------|---------|
| Round-trip | encode(decode(x)) == x | Serialization |
| Idempotency | f(f(x)) == f(x) | API retries, cache sets |
| Commutativity | f(a, b) == f(b, a) | Set operations |
| Invariant | precondition → postcondition holds | Balance never negative |
| No crash | f(random_input) doesn't panic | Input validation |

### Go Example
```go
func TestSortProperties(t *testing.T) {
    f := func(input []int) bool {
        sorted := Sort(input)

        // Property 1: Same length
        if len(sorted) != len(input) {
            return false
        }

        // Property 2: Ordered
        for i := 1; i < len(sorted); i++ {
            if sorted[i] < sorted[i-1] {
                return false
            }
        }

        // Property 3: Same elements (permutation)
        inputCounts := countElements(input)
        sortedCounts := countElements(sorted)
        return reflect.DeepEqual(inputCounts, sortedCounts)
    }

    if err := quick.Check(f, nil); err != nil {
        t.Error(err)
    }
}
```

### Python Example
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)

@given(st.lists(st.integers()))
def test_sort_is_ordered(xs):
    result = sorted(xs)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]
```

## Fuzzing

Feed random/mutated inputs to find crashes and edge cases:

### Go Native Fuzzing
```go
func FuzzParseInput(f *testing.F) {
    // Seed corpus
    f.Add([]byte(`{"name": "test"}`))
    f.Add([]byte(`{}`))
    f.Add([]byte(``))

    f.Fuzz(func(t *testing.T, data []byte) {
        result, err := ParseInput(data)
        if err != nil {
            return // errors are fine, panics are not
        }
        // Re-serialize and verify round-trip
        output, err := json.Marshal(result)
        if err != nil {
            t.Fatalf("failed to re-serialize: %v", err)
        }
        result2, err := ParseInput(output)
        if err != nil {
            t.Fatalf("round-trip failed: %v", err)
        }
        if !reflect.DeepEqual(result, result2) {
            t.Fatalf("round-trip mismatch")
        }
    })
}
```

Run fuzzing:
```bash
go test -fuzz=FuzzParseInput -fuzztime=60s ./...
```

## Contract Testing

Verify service interfaces without running the full system:

### Consumer-Driven Contracts
```
1. Consumer defines expected interactions (contract)
2. Provider verifies it can fulfill contracts
3. Contracts live in shared repo or broker
4. Both sides test independently against contracts
```

### Contract Test Structure
```go
// Consumer side: "I expect the provider to..."
func TestUserServiceContract(t *testing.T) {
    // Define expected interaction
    contract := Contract{
        Request: Request{
            Method: "GET",
            Path:   "/api/users/123",
        },
        Response: Response{
            Status: 200,
            Body: map[string]interface{}{
                "id":    "123",
                "name":  Matcher("string"),
                "email": Matcher("email"),
            },
        },
    }

    // Verify against mock
    mock := NewContractMock(contract)
    client := NewUserClient(mock.URL())
    user, err := client.GetUser(ctx, "123")
    assert.NoError(t, err)
    assert.Equal(t, "123", user.ID)
}

// Provider side: "I can fulfill these contracts"
func TestProviderFulfillsContracts(t *testing.T) {
    contracts := LoadContracts("user-service")
    server := StartRealServer()
    for _, contract := range contracts {
        VerifyContract(t, server, contract)
    }
}
```

## Chaos Engineering

Systematically inject failures to build confidence in resilience:

### Experiment Design
```markdown
## Experiment: [Name]

### Hypothesis
When [failure condition], the system will [expected behavior],
and users will [expected user experience].

### Steady State
- Error rate: < 0.1%
- Latency p99: < 200ms
- Availability: 99.9%

### Method
[How to inject the failure]

### Blast Radius
[What's affected, safety controls]

### Abort Conditions
[When to immediately stop the experiment]
```

### Common Experiments

| Experiment | Method | Expected Result |
|-----------|--------|----------------|
| Kill a service instance | Terminate pod/container | Traffic shifts, no errors |
| Add 500ms latency | Network delay injection | Timeouts fire, fallbacks work |
| Fail database | Block DB port | Cached responses served |
| Exhaust connection pool | Open connections, don't release | Backpressure, graceful rejection |
| Corrupt cache | Inject bad data | Validation catches, re-fetches |

## Test Data Management

### Strategies
- **Factories**: Generate test data programmatically (preferred)
- **Fixtures**: Static JSON/YAML test data (for complex scenarios)
- **Snapshots**: Captured production data (anonymized)
- **Synthetic generators**: Realistic data at scale

### Test Isolation
```go
// ✅ Each test gets its own data
func TestOrderProcessing(t *testing.T) {
    db := setupTestDB(t)         // fresh database per test
    user := factory.CreateUser(t, db)
    order := factory.CreateOrder(t, db, user)

    err := processOrder(ctx, db, order.ID)
    assert.NoError(t, err)
}
```

## Test Architecture Principles

1. **Tests are production code** — same quality standards apply
2. **Test behavior, not implementation** — survive refactors
3. **One assertion per concept** — clear failure messages
4. **Fast by default** — unit tests < 1s, integration < 30s
5. **Deterministic always** — no flaky tests in CI
6. **Isolated completely** — no shared state between tests

## Verification Checklist

- [ ] Property-based tests for core algorithms and data transformations
- [ ] Fuzz tests for parsers and input handlers
- [ ] Contract tests at service boundaries
- [ ] Chaos experiments for critical resilience requirements
- [ ] Test factories (not fixtures) for test data
- [ ] No flaky tests in CI (quarantine immediately)

---

**Remember**: Tests don't prove the absence of bugs — they prove the presence of expected behavior. The more creative your test inputs, the more confident you can be.
