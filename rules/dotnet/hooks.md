---
paths:
  - "**/*.cs"
---

# C# / .NET Hooks

> Automatically enforce code quality in .NET projects.

## Pre-Commit Checks

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "script": "dotnet build",
      "condition": "file matches '**/*.cs'",
      "exitCode": 2
    },
    {
      "matcher": "Bash",
      "script": "dotnet test",
      "condition": "file matches '**/*.cs' and type is 'test'",
      "exitCode": 2
    }
  ]
}
```

## Code Analysis

Run static analysis:

```bash
dotnet analyze
dotnet format --verify-no-changes
```

## Reference

See skill: `springboot-tdd` for testing patterns (many apply to C# unit testing with xUnit/NUnit).
