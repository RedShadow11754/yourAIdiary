# Error Report — ProjectDiaryV2

> Ignoring the NumPy/TensorFlow version mismatch warnings — those are cosmetic and don't break anything.

---

## 🚨 The Problem: Redis Is Not Running

Both `celery worker` and `celery beat` are failing with:

```
Cannot connect to redis://localhost:6379/0: Error 10061 connecting to localhost:6379.
No connection could be made because the target machine actively refused it.
```

**What's happening:** Your `config/settings.py` has:
```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

Celery needs Redis as its message broker. Right now, nothing is listening on port 6379.

**Note:** Qdrant is fine — you can see `[Qdrant] Collection already exists, skipping.` which means it's running and connected.

---

## ✅ The Fix — Start Your Docker Containers

You said it used to work. You were probably running these Docker containers before:

```powershell
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

If the containers already exist but are stopped, just restart them:

```powershell
docker start redis
docker start qdrant
```

If they don't exist anymore (were deleted), run the full `docker run` commands above.

To verify Redis is up before retrying Celery:

```powershell
docker ps
```

You should see both `redis` and `qdrant` in the running list, with ports `6379` and `6333` mapped.

---

## Summary

| Error | Cause | Fix |
|-------|-------|-----|
| `Error 10061 connecting to localhost:6379` | Redis container not running | `docker start redis` or `docker run -d --name redis -p 6379:6379 redis:7-alpine` |

That's it — one problem, one fix.
