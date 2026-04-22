---
id: gotcha-python-fstrings
type: knowledge
tags: ["#python", "#syntax"]
links: ["[[MOC-debugging]]"]
---

# Gotcha: Python f-string Expressions

**Symptom:** Expressions like `{'s' if x != 1 else ''}` inside braces print literally.

**Why:** The `f` prefix is required for evaluation. Without it, `{}` is literal text.

**Fix:** Use a lambda for conditional/computed values in template strings:
```python
MSG_COUNT = lambda n: f"Found {n} item{'s' if n != 1 else ''}!"
```

**Note:** Plain `.format()` is for simple substitution, not arbitrary expression evaluation.
