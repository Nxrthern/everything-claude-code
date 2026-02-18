---
paths:
  - "**/*.rb"
---

# Ruby Security

Store secrets in environment variables:

```ruby
require 'dotenv'
Dotenv.load

api_key = ENV.fetch('API_KEY') { raise "API_KEY not set" }
```

Validate all input and use **Brakeman** for security scanning.
