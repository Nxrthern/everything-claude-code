---
paths:
  - "**/*.rs"
---

# Rust Security

> Security best practices for Rust development.

## Secret Management

Store secrets in environment variables, never in code:

```rust
use std::env;

fn get_api_key() -> Result<String> {
    env::var("API_KEY")
        .map_err(|_| "API_KEY not set in environment")
}
```

Use `dotenv` for local development:

```rust
dotenv::dotenv().ok();
let api_key = env::var("API_KEY")?;
```

## Dependency Security

Keep dependencies up-to-date:

```bash
cargo update
cargo outdated
```

Use `cargo-audit` to check for known vulnerabilities:

```bash
cargo audit
```

Lock your dependencies:

```toml
[dependencies]
serde = "=1.0.192"  # Exact version
tokio = "1.35"      # Latest 1.x
```

## Input Validation

Always validate untrusted input:

```rust
fn validate_username(name: &str) -> Result<()> {
    if name.len() < 3 || name.len() > 50 {
        Err("Username must be 3-50 characters")?
    }
    if !name.chars().all(|c| c.is_alphanumeric() || c == '_') {
        Err("Username can only contain alphanumerics and underscore")?
    }
    Ok(())
}
```

## Panic Safety

Never panic in libraries (use Result instead):

```rust
// ❌ Bad: panics on invalid input
fn divide_unsafe(a: i32, b: i32) -> i32 {
    a / b  // panics if b == 0
}

// ✅ Good: returns Result
fn divide(a: i32, b: i32) -> Result<i32> {
    if b == 0 {
        Err("Division by zero")?
    }
    Ok(a / b)
}
```

## Memory Safety (Built-in)

Rust's memory safety is enforced by the compiler:

- No null pointers (use `Option<T>`)
- No use-after-free (borrow checker)
- No buffer overflows (bounds checking)
- No data races (Send/Sync traits)

## SQL Injection Prevention

Use parameterized queries:

```rust
use sqlx::query;

// ✅ Safe: parameters are escaped
let user = query!("SELECT * FROM users WHERE id = ?", user_id)
    .fetch_one(&pool)
    .await?;

// ❌ Never do this:
// let query = format!("SELECT * FROM users WHERE id = {}", user_id);
```

## Concurrency Safety

Use channels instead of shared mutable state:

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();

std::thread::spawn(move || {
    tx.send("message").unwrap();
});

let msg = rx.recv().unwrap();
```

Avoid `unwrap()` and `expect()` in production (use proper error handling).

## Reference

See skill: `springboot-security` for broader security patterns; apply Rust-specific context.
