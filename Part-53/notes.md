# Part 53 — Type Hints (Readable, Safe, and Real-World Code)

In Part 52, you learned decorators. Now we shift to a different kind of clarity: type hints, which tell readers and tools exactly what data flows through your functions. This part goes from the basics to the advanced workflow used on real projects.

This chapter uses one running example: a `login(email, password)` flow. Each section adds a new requirement to the same login system.

## Why Type Hints Matter

```python
def login(email, password):             # What types are these?
    return "token-abc123"                # What can this return?

def login(email: str, password: str) -> str:
    return "token-abc123"
```

The second signature is immediately clear: `login` accepts two strings and returns a token string. The contract is visible without reading the function body.

---



## Basic Annotations

```python
def login(email: str, password: str) -> str:
    return "token-abc123"
```



### Hints Are NOT Enforced at Runtime

```python
login(123, True)   # Python still runs this and returns "token-abc123"
```

The Python interpreter does **not** enforce annotations during normal function calls. They exist for **developers**, **IDEs**, and **type checkers** such as mypy and pyright. Libraries can inspect the metadata with `typing.get_type_hints()` and add runtime behavior.

---



## Built-in Generic Types (Python 3.9+)

```python
roles: list[str] = ["member", "editor"]
active_sessions: dict[str, str] = {"alice@example.com": "token-abc123"}
login_fields: tuple[str, str] = ("email", "password")
scopes: tuple[str, ...] = ("read", "write", "profile")
trusted_devices: set[str] = {"laptop", "phone"}
```


| Type              | Meaning in the login system     |
| ----------------- | ------------------------------- |
| `list[str]`       | A list of role names            |
| `dict[str, str]`  | Email-to-token session mapping  |
| `tuple[str, str]` | Exactly two string field names  |
| `tuple[str, ...]` | Any number of permission scopes |
| `set[str]`        | Unique trusted-device names     |




### Why They Are Called Built-in Generics

Before Python 3.9:

```python
from typing import Dict, List
roles: List[str] = ["member", "editor"]
active_sessions: Dict[str, str] = {"alice@example.com": "token-abc123"}
```

Since Python 3.9:

```python
roles: list[str] = ["member", "editor"]
active_sessions: dict[str, str] = {"alice@example.com": "token-abc123"}
```

They are called **built-in generics** because built-ins such as `list` and `dict` can now directly receive type arguments. `list[str]` means “a list expected to contain strings”; `str` is not a default.

> **Timeline tip:** `int`, `str`, and the other runtime types have existed since early Python. Function annotation syntax such as `value: int` arrived in Python 3.0 (2008), standardized type hints arrived in Python 3.5 (2015), variable annotations arrived in Python 3.6, and built-in generics such as `list[int]` arrived in Python 3.9 (2020).

---



## Optional and Union — More Than One Possible Type

Use the `|` syntax (Python 3.10+):

```python
def login(email: str, password: str) -> str | None:
    if email == "alice@example.com" and password == "demo-password":
        return "token-abc123"
    return None
```

`str | None` means login returns a token on success or `None` for invalid credentials. It is the modern form of `Optional[str]`; the broader `X | Y` syntax replaces `Union[X, Y]`.

> The plain-text credential comparison is only for this small teaching example. Production systems store password hashes and use a proper authentication service.

---



## Variable Annotations and `-> None`

```python
email: str = "alice@example.com"
failed_attempts: int = 0
active_sessions: dict[str, str] = {}

def record_login(email: str) -> None:  # -> None = called for side effects only
    print(f"Login recorded for {email}")
```

---



## Extending the Login Function

```python
def login(email: str, password: str) -> str | None:
    if not email or not password:
        raise ValueError("Email and password are required")

    if email == "alice@example.com" and password == "demo-password":
        return "token-abc123"

    return None
```

The signature now communicates the complete flow: two required strings enter; either a token or `None` comes back. The IDE can provide autocomplete, inline errors, hover information, and safer refactoring.

---



## Advanced — The Harder Cases

You have the basics: annotations, generics, `Optional`/`Union`, and variables. Now the cases you hit on real projects: structured dicts, structural typing, restricted values, function types, and static checking.

### TypedDict — Dictionaries with Known Keys

`dict[str, Any]` loses nearly all useful detail. `TypedDict` describes a dictionary's known keys and the type of each value:

```python
from typing import TypedDict, NotRequired

class LoginResponse(TypedDict):
    access_token: str
    expires_in: int
    roles: list[str]
    refresh_token: NotRequired[str]

def login(email: str, password: str) -> LoginResponse | None:
    if email != "alice@example.com" or password != "demo-password":
        return None

    return {
        "access_token": "token-abc123",
        "expires_in": 3600,
        "roles": ["member"],
    }
```

A checker verifies that required keys exist and value types match (`"expires_in": "3600"` is flagged). `TypedDict` describes the login response for static checking; it does not create a new runtime class or validate incoming API data.

### Protocol — Structural Typing

You saw `Protocol` briefly in Part 46. It defines what methods an object must have — **without inheritance**:

```python
from typing import Protocol

class CredentialsVerifier(Protocol):
    def verify(self, email: str, password: str) -> bool: ...

class DemoVerifier:
    def verify(self, email: str, password: str) -> bool:
        return email == "alice@example.com" and password == "demo-password"

def login(
    verifier: CredentialsVerifier,
    email: str,
    password: str,
) -> LoginResponse | None:
    if not verifier.verify(email, password):
        return None

    return {
        "access_token": "token-abc123",
        "expires_in": 3600,
        "roles": ["member"],
    }

verifier = DemoVerifier()

result = login(verifier, "alice@example.com", "demo-password")
print(result)
# {'access_token': 'token-abc123', 'expires_in': 3600, 'roles': ['member']}
```

Any authentication provider with a matching `verify(email, password) -> bool` method satisfies `CredentialsVerifier` — duck typing with static type safety.


|              | ABC (Part 46)       | Protocol           |
| ------------ | ------------------- | ------------------ |
| Inheritance  | Required            | Not required       |
| Error timing | Runtime             | Type-check time    |
| Use case     | Enforcing contracts | Expecting behavior |




### Literal — Restricting to Specific Values

```python
from typing import Literal

LoginStatus = Literal["success", "invalid_credentials", "locked"]

def record_login_status(email: str, status: LoginStatus) -> None:
    print(email, status)

record_login_status("alice@example.com", "pending")  # type-checker error
```

`Literal` restricts the login status to the three values the system understands.

### Any — Opting Out

```python
from typing import Any

def extract_token(payload: Any) -> Any:
    return payload["access_token"]   # checker cannot verify the key or value type
```

`Any` disables useful checking for that value. It may be unavoidable when first receiving data from an untyped authentication library, but it should not spread through the application.

### Callable — Typing Functions

```python
from typing import Callable

def create_jwt(email: str) -> str:
    return f"real-jwt-for-{email}"

def create_test_token(email: str) -> str:
    return "fake-test-token"

def login(
    verifier: CredentialsVerifier,
    email: str,
    password: str,
    issue_token: Callable[[str], str],
) -> LoginResponse | None:
    if not verifier.verify(email, password):
        return None

    return {
        "access_token": issue_token(email),
        "expires_in": 3600,
        "roles": ["member"],
    }

production_result = login(
    verifier,
    "alice@example.com",
    "demo-password",
    create_jwt,
)

test_result = login(
    verifier,
    "alice@example.com",
    "demo-password",
    create_test_token,
)

if production_result is not None and test_result is not None:
    print(production_result["access_token"])  # real-jwt-for-alice@example.com
    print(test_result["access_token"])        # fake-test-token
```

`Callable[[str], str]` lets the caller choose any token function that accepts an email string and returns a token string. Production passes `create_jwt`; tests pass the lightweight `create_test_token`. The authentication logic in `login` does not need to change.

---



## Static Type Checking — mypy and pyright

Writing annotations is only step one; a static checker verifies them:

```bash
pip install mypy
mypy your_file.py
```

```python
def issue_token(email: str) -> str:
    return f"token-for-{email}"

response: LoginResponse = login(
    verifier,
    "alice@example.com",
    "wrong-password",
    issue_token,
)
# checker error: login can return LoginResponse | None

login(verifier, 123, "demo-password", issue_token)
# checker error: email must be str
```

Pyright powers editor diagnostics in tools that integrate it, including Pylance. Enable an appropriate `basic`, `standard`, or `strict` checking mode in project configuration. You don't need to type everything at once: start with public signatures and return types, then add complex structures, running the checker as you go (**gradual typing**).

## Runtime vs Static Typing


| Aspect   | Static (mypy/pyright) | Runtime (Pydantic)  |
| -------- | --------------------- | ------------------- |
| When     | Before running        | While running       |
| How      | Analyzes code         | Validates live data |
| Use case | Development, CI       | API input, config   |


```python
from dataclasses import dataclass

@dataclass
class LoginRequest:
    email: str
    password: str

LoginRequest(email=42, password=True)  # runs; a checker flags both values
```



### Pydantic in Normal Python (No FastAPI Required)

```bash
pip install pydantic
```

```python
from pydantic import BaseModel, ConfigDict

class ValidatedLoginRequest(BaseModel):
    model_config = ConfigDict(strict=True)

    email: str
    password: str

request = ValidatedLoginRequest(
    email=42,
    password=True,
)
# Raises pydantic.ValidationError while the program is running
```

Pydantic reads the annotations and validates the actual values when the model is created. It works in any normal Python program; FastAPI simply integrates it automatically for API data. Validate untrusted data at the boundary, then use typed values inside the application.

---



## When to Add Types


| Situation                                   | Recommendation                        |
| ------------------------------------------- | ------------------------------------- |
| Public functions, methods, class attributes | Always                                |
| Module-level variables                      | When the type isn't obvious           |
| Internal helpers / quick prototypes         | Optional — add when helpful           |
| Complex data transformations                | Always — types are your documentation |




## Where This Applies in Real Work

- **Pydantic and FastAPI:** every endpoint and request/response model uses hints; FastAPI validates bodies and generates API docs from them.
- **Large codebases and teams:** hints make code navigable and communicate intent without comments (`Optional[str]` says "might be None").
- **AI pipelines:** `TypedDict`/dataclass-typed model inputs and outputs clarify handoffs and help AI tools produce compatible code.
- **Code review and CI/CD:** typed code is easier to review, and many teams block merges that fail mypy.

---



## Practice Assignment

Build the typed login flow used throughout this chapter.

1. Write `login(email: str, password: str) -> str | None`.
2. Replace the token string with a `LoginResponse` `TypedDict` containing `access_token`, `expires_in`, `roles`, and an optional `refresh_token`.
3. Create `LoginStatus = Literal["success", "invalid_credentials", "locked"]`.
4. Create a `CredentialsVerifier` `Protocol` with `verify(email, password) -> bool`.
5. Pass a `Callable[[str], str]` token factory into `login`.
6. Run mypy or pyright, deliberately pass an integer as the email, and fix the reported error.

Save as `src/typed_login.py`.

---

