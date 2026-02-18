---
name: live-updates
description: Zero-downtime configuration reloads, dirty bit change tracking, optimistic concurrency, and hot reload patterns. Use when implementing live config updates, detecting data changes efficiently, or designing systems that update without restarts.
---

# Live Updates & Change Tracking

The best systems update without anyone noticing. No restarts, no downtime, no lost requests.

## When to Activate

- Implementing zero-downtime config reloads
- Designing change detection mechanisms (dirty bits, ETags)
- Implementing optimistic concurrency control
- Building systems that hot-reload without restart
- Designing cache invalidation triggers

## Zero-Downtime Config Reload

### Pattern: Atomic Swap
```go
// ✅ Atomically swap config without locking readers
type Server struct {
    config atomic.Value // stores *Config
}

func (s *Server) ReloadConfig(path string) error {
    newCfg, err := loadAndValidate(path)
    if err != nil {
        return fmt.Errorf("invalid config: %w", err) // keep old config
    }
    s.config.Store(newCfg)
    log.Info("config reloaded", "path", path)
    return nil
}

func (s *Server) GetConfig() *Config {
    return s.config.Load().(*Config)
}
```

### Pattern: Signal-Based Reload
```go
// ✅ Reload on SIGHUP (Unix convention)
func setupSignalReload(server *Server, configPath string) {
    sigs := make(chan os.Signal, 1)
    signal.Notify(sigs, syscall.SIGHUP)
    go func() {
        for range sigs {
            if err := server.ReloadConfig(configPath); err != nil {
                log.Error("reload failed", "error", err)
            }
        }
    }()
}
```

### Pattern: File Watcher
```go
// ✅ Watch config file for changes
func watchConfigFile(ctx context.Context, path string, onChange func()) {
    watcher, _ := fsnotify.NewWatcher()
    defer watcher.Close()
    watcher.Add(path)

    for {
        select {
        case event := <-watcher.Events:
            if event.Op&fsnotify.Write != 0 {
                onChange()
            }
        case <-ctx.Done():
            return
        }
    }
}
```

## Dirty Bit Pattern

Track which records have changed for efficient synchronization:

### Database-Level Dirty Tracking
```sql
-- Add dirty flag and timestamp to track changes
ALTER TABLE products ADD COLUMN is_dirty BOOLEAN DEFAULT false;
ALTER TABLE products ADD COLUMN updated_at TIMESTAMPTZ DEFAULT NOW();

-- Trigger to auto-set dirty on update
CREATE OR REPLACE FUNCTION mark_dirty()
RETURNS TRIGGER AS $$
BEGIN
    NEW.is_dirty = true;
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_dirty
    BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION mark_dirty();

-- Sync job: process dirty records, then clear flag
UPDATE products SET is_dirty = false
WHERE id IN (
    SELECT id FROM products WHERE is_dirty = true LIMIT 1000
);
```

### Application-Level Change Detection
```go
// ✅ ETag-based change detection for APIs
func handleGetProduct(w http.ResponseWriter, r *http.Request) {
    product := getProduct(r.Context(), productID)
    etag := computeETag(product)

    // Client sends If-None-Match header
    if r.Header.Get("If-None-Match") == etag {
        w.WriteHeader(http.StatusNotModified) // 304: no change
        return
    }

    w.Header().Set("ETag", etag)
    json.NewEncoder(w).Encode(product)
}
```

## Optimistic Concurrency Control

Prevent lost updates without pessimistic locking:

```go
// ✅ Version-based optimistic locking
func updateProduct(ctx context.Context, product Product) error {
    result, err := db.Exec(ctx,
        `UPDATE products SET name = $1, price = $2, version = version + 1
         WHERE id = $3 AND version = $4`,
        product.Name, product.Price, product.ID, product.Version,
    )
    if err != nil {
        return err
    }
    if result.RowsAffected() == 0 {
        return ErrConflict // another writer updated first — retry
    }
    return nil
}
```

```sql
-- ✅ Database-enforced version column
ALTER TABLE products ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
```

## Change Data Capture (CDC)

Stream database changes to consumers without polling:

```
Database WAL → Debezium → Kafka → Consumers
                                    ├── Search index updater
                                    ├── Cache invalidator
                                    └── Analytics pipeline
```

### Benefits Over Polling
- Real-time (milliseconds vs polling interval)
- No load on database from polling queries
- Captures all changes (including deletes)
- Ordered by transaction commit

## Graceful Restart Pattern

Update application binary without dropping connections:

```
1. New process starts, binds to same socket (SO_REUSEPORT)
2. Old process stops accepting new connections
3. Old process drains in-flight requests (grace period)
4. Old process exits
5. New process handles all traffic
```

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|-------------|------|-----|
| Restart to reload config | Downtime, lost connections | Signal-based or file-watch reload |
| Poll database for changes | Wasted resources, delay | CDC or dirty bit pattern |
| No conflict detection | Lost updates | Optimistic locking with version |
| Full sync on every change | Expensive, slow | Dirty bits for incremental sync |
| No validation before reload | Bad config crashes service | Validate before swapping |

---

**Remember**: A system that requires a restart to change behavior is a system that requires downtime to evolve. Design for live updates from day one — your future self will thank you at 3 AM.
