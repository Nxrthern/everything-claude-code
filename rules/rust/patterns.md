---
paths:
  - "**/*.rs"
---

# Rust Patterns

> Essential Rust patterns for idiomatic code.

## Functional Options Pattern

Build flexible constructors without builder bloat:

```rust
#[derive(Clone)]
struct Config {
    timeout: Duration,
    retries: u32,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            timeout: Duration::from_secs(5),
            retries: 3,
        }
    }
}

impl Config {
    pub fn timeout(mut self, d: Duration) -> Self {
        self.timeout = d;
        self
    }

    pub fn retries(mut self, n: u32) -> Self {
        self.retries = n;
        self
    }
}

// Usage
let config = Config::default()
    .timeout(Duration::from_secs(10))
    .retries(5);
```

## Small, Focused Traits

Traits should be narrowly scoped:

```rust
trait Serializable {
    fn serialize(&self) -> Vec<u8>;
}

trait Deserializable: Sized {
    fn deserialize(data: &[u8]) -> Result<Self>;
}
```

## Dependency Injection

Use trait objects for runtime polymorphism:

```rust
pub struct Handler {
    logger: Box<dyn Logger>,
    storage: Arc<dyn Storage>,
}

impl Handler {
    pub fn new(logger: Box<dyn Logger>, storage: Arc<dyn Storage>) -> Self {
        Handler { logger, storage }
    }
}
```

## Error Handling with Context

Add context to errors for better debugging:

```rust
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let data = std::fs::read_to_string(path)
        .context(format!("Failed to read config from {}", path))?;
    
    serde_json::from_str(&data)
        .context("Invalid JSON in config file")?
}
```

## Type-Driven Development

Leverage the type system to encode business logic:

```rust
#[derive(Debug, Clone, Copy)]
struct Validated<T>(T);

impl Validated<String> {
    fn new(s: String) -> Result<Self> {
        if s.is_empty() {
            Err("Email cannot be empty")?
        }
        Ok(Validated(s))
    }
}

fn send_email(to: Validated<String>) {
    // Guaranteed to be non-empty
}
```

## Reference

See skill: `rust-pro` for advanced patterns including async/await, concurrency, and macro development.
