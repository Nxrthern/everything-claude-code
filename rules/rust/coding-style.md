---
paths:
  - "**/*.rs"
---

# Rust Coding Style

> This file extends [common/coding-style.md](../common/coding-style.md) with Rust-specific content.

## Standards

- Follow **Rust idioms** from the Rust Book and Clippy lints
- Use **rustfmt** for automatic formatting (enforced in CI)
- Enable all **Clippy** warnings in your CI: `cargo clippy -- -D warnings`
- Use **semantic versioning** for dependencies

## Ownership & Borrowing

Understand and leverage Rust's ownership model:

```rust
// Prefer references over cloning
fn process(data: &[u8]) { }

// Use references in structs when appropriate
struct Handler<'a> {
    callback: &'a dyn Fn(),
}

// Explicit lifetime annotations for clarity
fn process<'a>(input: &'a str) -> &'a str { }
```

## Error Handling

- Use `Result<T, E>` for fallible operations
- Use `?` operator instead of `match` when propagating errors
- Define custom error types with `thiserror` or `anyhow`

```rust
use anyhow::Result;

fn connect(url: &str) -> Result<Connection> {
    let conn = tcp::connect(url)?;
    Ok(conn)
}
```

## Immutability

- Prefer `let` over `let mut`
- Use `const` for compile-time constants
- Use `static` for global state (rare)

## Type System

- Leverage pattern matching with `match` and `if let`
- Use traits for polymorphism
- Prefer `newtype` pattern for type safety

```rust
struct UserId(u64);
struct ProductId(u64);

fn get_product(id: ProductId) { }
// get_product(UserId(1)) // Compile error!
```

## Tooling

- **rustfmt** for formatting
- **clippy** for linting
- **cargo check** before commits
- **cargo test** for testing
- **cargo bench** for performance testing

## Performance

- Profile with `cargo flamegraph` before optimizing
- Use `&` for zero-copy references
- Consider SIMD with `packed_simd`
- Avoid unnecessary allocations

## Reference

See skill: `rust-pro` for comprehensive Rust patterns and advanced techniques.
