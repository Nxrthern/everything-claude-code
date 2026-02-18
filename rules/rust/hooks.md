---
paths:
  - "**/*.rs"
---

# Rust Hooks

> Automatically enforce code quality in Rust projects.

## Pre-Commit Checks

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "script": "cargo check --all-targets",
      "condition": "file matches '**/*.rs'",
      "exitCode": 2
    },
    {
      "matcher": "Bash",
      "script": "cargo clippy --all-targets -- -D warnings",
      "condition": "file matches '**/*.rs'",
      "exitCode": 2
    }
  ]
}
```

## Auto-Format on Edit

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "script": "rustfmt '{{file}}'",
      "condition": "file matches '**/*.rs'"
    }
  ]
}
```

## Testing Hooks

Run tests after edits:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit",
      "script": "cargo test --lib --all",
      "condition": "file matches '**/*.rs' and type is 'test'"
    }
  ]
}
```

## Reference

See skill: `golang-testing` for comprehensive testing patterns (Rust testing is similar with `#[test]` and `#[cfg(test)]` attributes).
