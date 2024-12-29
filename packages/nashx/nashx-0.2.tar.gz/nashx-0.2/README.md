# nashx

`nashx` is a simple yet efficient Python hashing library that allows users to generate hashes with customizable lengths. The package includes two distinct functions for hashing:

- **`nashCore`**: A deterministic hashing function.
- **`nashGuard`**: A salted hashing function that adds an extra layer of security.

## Changes in Version 0.2

In version 0.2, we have introduced the following improvements:
- **`nashCore`**: A deterministic version of the original `hasher` function, which generates consistent hashes for the same input.
- **`nashGuard`**: A new salted hash function. This function adds complexity by incorporating a salt into the hashing process, making the hash more secure. The function also generates the salt if it is not provided.
- **Updated Function Names**: The old `hasher` function has been replaced with `nashCore` for deterministic hashing and `nashGuard` for salted hashing.

## Installation

You can install the `nashx` package via `pip`:

```bash
pip install nashx
```

## Usage

### 1. `nashCore` (Deterministic Hashing)

The `nashCore` function generates a deterministic hash, meaning that the same input will always produce the same output hash.

```python
from nashx import nashCore

data = "example"
hash_length = 16
hash_result = nashCore(data, hash_length)
print("Deterministic Hash:", hash_result)
```

### 2. `nashGuard` (Salted Hashing)

The `nashGuard` function generates a salted hash. If the salt is not provided, it will generate one internally. The function returns both the hash and the salt.

#### Example with generated salt:

```python
from nashx import nashGuard

data = "example"
hash_length = 16

# If salt is not provided, nashGuard will generate one
hash_result, salt_used = nashGuard(data, hash_length)
print("Salted Hash:", hash_result)
print("Salt Used:", salt_used)
```

#### Example with custom salt:

```python
salt = "your_preferred_salt_value"
hash_result, salt_used = nashGuard(data, hash_length, salt)
print("Salted Hash with Custom Salt:", hash_result)
print("Salt Used:", salt_used)
```

## Function Explanation

### `nashCore(words, length)`

- **Parameters:**
  - `words`: The input string to be hashed.
  - `length`: The desired length of the generated hash.
- **Returns:** A deterministic hash of the input string.

### `nashGuard(words, length, salt=None)`

- **Parameters:**
  - `words`: The input string to be hashed.
  - `length`: The desired length of the generated hash.
  - `salt`: The optional salt to be used in the hash. If not provided, the function will generate a random salt.
- **Returns:** A tuple containing the salted hash and the salt used.

## Example Output

### Deterministic Hash:
```python
Deterministic Hash: 8d40e2a833d2f67d
```

### Salted Hash (salt is generated):
```python
Salted Hash: 30a76f5f7585a6b9
Salt Used: f7a3e19b8cf6c2d7
```

### Salted Hash (using provided salt):
```python
Salted Hash with Custom Salt: 64b38c5f7b42cbb3
Salt Used: your_preferred_salt_value
```

