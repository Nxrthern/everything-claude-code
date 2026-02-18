---
paths:
  - "**/*.rb"
---

# Ruby Patterns

## Dependency Injection

```ruby
class UserService
  def initialize(repository = UserRepository.new)
    @repository = repository
  end
  
  def get(id)
    @repository.find(id)
  end
end
```

## Method Chaining

Ruby supports fluent APIs:

```ruby
users = User.where(active: true)
         .order(:name)
         .includes(:roles)
         .limit(10)
```
