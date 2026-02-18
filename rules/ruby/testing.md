---
paths:
  - "**/*.rb"
---

# Ruby Testing

Use **RSpec** for BDD:

```ruby
describe UserService do
  describe '#get_user' do
    it 'returns a user by id' do
      user = described_class.new.get(1)
      expect(user).to be_a(User)
    end
  end
end
```

Target: 80%+ coverage with SimpleCov.
