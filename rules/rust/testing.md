---
paths:
  - "**/*.rs"
---

# Rust Testing

> Test-driven development with Rust.

## Unit Tests

Use `#[cfg(test)]` modules:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    fn test_subtract() {
        assert_eq!(subtract(5, 2), 3);
    }
}
```

## Table-Driven Tests

Use iterators for parameterized tests:

```rust
#[test]
fn test_fibonacci() {
    let cases = vec![
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (5, 5),
    ];

    for (input, expected) in cases {
        assert_eq!(fibonacci(input), expected);
    }
}
```

## Result-Based Tests

Test error cases:

```rust
#[test]
fn test_divide_by_zero() {
    let result = divide(10, 0);
    assert!(result.is_err());
    assert_eq!(result.unwrap_err(), "Division by zero");
}
```

## Running Tests

```bash
cargo test                    # Run all tests
cargo test --lib             # Only unit tests
cargo test --doc             # Only doc tests
cargo test -- --test-threads=1  # Single-threaded
```

## Benchmarks

Use `criterion` for performance testing:

```rust
#[cfg(test)]
mod benches {
    use super::*;
    use criterion::{black_box, criterion_group, criterion_main, Criterion};

    fn criterion_benchmark(c: &mut Criterion) {
        c.bench_function("fibonacci(10)", |b| {
            b.iter(|| fibonacci(black_box(10)))
        });
    }

    criterion_group!(benches, criterion_benchmark);
    criterion_main!(benches);
}
```

Run benchmarks:

```bash
cargo bench
```

## Integration Tests

Create `tests/` directory (separate from `src/`):

```rust
// tests/integration_test.rs
#[test]
fn test_full_workflow() {
    let app = setup();
    let result = app.run();
    assert_eq!(result.status, 0);
}
```

## Test Coverage

Use `tarpaulin` for coverage reports:

```bash
cargo tarpaulin --out Html
```

Target: **80%+ coverage** for core logic.

## Mocking

Use `mockito` for HTTP mocking:

```rust
#[test]
fn test_api_call() {
    let mut server = mockito::Server::new();
    let mock = server.mock("GET", "/users")
        .with_status(200)
        .with_body("[]")
        .create();

    // Your code here
    mock.assert();
}
```

## TDD Workflow

1. **Red**: Write failing test
2. **Green**: Implement minimum code to pass
3. **Refactor**: Improve without breaking tests

```rust
#[test]
fn test_palindrome() {
    // Red: This fails initially
    assert!(is_palindrome("racecar"));
    assert!(!is_palindrome("hello"));
}

// Implement to make it green
fn is_palindrome(s: &str) -> bool {
    s == s.chars().rev().collect::<String>()
}
```

## Reference

See skill: `golang-testing` for test organization patterns (many are language-agnostic and apply to Rust).
