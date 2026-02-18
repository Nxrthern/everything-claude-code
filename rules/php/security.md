---
paths:
  - "**/*.php"
---

# PHP Security

Use environment variables with vlucas/dotenv:

```php
<?php

use Dotenv\Dotenv;

$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

$apiKey = $_ENV['API_KEY'];
```

Always:
- Validate input with `filter_var()`
- Use parameterized queries (PDO prepared statements)
- Hash passwords with `password_hash()`
- Use HTTPS
- Keep dependencies updated
