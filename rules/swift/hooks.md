---
paths:
  - "**/*.swift"
---

# Swift Hooks

Use Xcode build phases to run SwiftFormat and SwiftLint on save.

## SwiftFormat

```bash
if which swiftformat >/dev/null; then
  swiftformat .
else
  echo "SwiftFormat not installed"
fi
```

## SwiftLint

```bash
if which swiftlint >/dev/null; then
  swiftlint autocorrect --fix
else
  echo "SwiftLint not installed"
fi
```
