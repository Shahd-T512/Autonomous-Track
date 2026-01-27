
# Concept 18: Generics (Templates & Type Hinting)

## 1. Deep Explanation (The Logic)
In strict languages like C++, you must create specific functions for specific data types (`add_int`, `add_float`).
In Python, **everything is generic by default**.

### The Logic: "Duck Typing" 🦆
Python uses a philosophy called **Duck Typing**.
> *"If it walks like a duck and quacks like a duck, then it must be a duck."*

If you write a function `def add(a, b): return a + b`, Python doesn't care if `a` and `b` are Integers, Floats, Strings, or Lists. As long as they support the `+` operator, the code works.



**However:** In large Robotics projects (like ROS2), "Anything Goes" is dangerous. We want **Type Safety** to ensure our code is correct *before* we run the robot. We achieve this using **Type Hints** and **Generics** (from the `typing` library).

---

## 2. Why do we use it?
1.  **Code Reusability:** Just like C++, we write the logic **once**. It works for `int`, `float`, or `Robot`.
2.  **Safety & IDE Support:** By explicitly telling the editor *"This function accepts any type T"*, tools like VS Code can autocomplete your code and warn you if you try to add a Number to a String.

---

## 3. Syntax & Rules

### A. Implicit Generics (The Default)
You don't need special syntax to make a function generic.

```python
def find_max(a, b):
    return a if a > b else b
# Works for ints, floats, strings automatically

```

### B. Explicit Generics (The Strict Way)

To enforce strict typing rules (similar to C++ Templates), we use `TypeVar`.

```python
from typing import TypeVar

# 1. Define the Placeholder "T"
T = TypeVar('T')

# 2. Use "T" in the function signature
# This says: "The inputs 'a' and 'b' MUST be the same type, 
# and the return value will be that SAME type."
def safe_find_max(a: T, b: T) -> T:
    if a > b:
        return a
    return b

```

---

## 4. The Trap: "Runtime vs Static Check" ⚠️

* **The Trap:** Python **ignores** these Type Hints when the script runs.
* If you pass a string and an int to `safe_find_max`, the program will still crash at **runtime** (because `>` fails between string and int), even if you added hints.


* **The Reality:** Generics in Python are primarily for **Static Analysis** (tools like `mypy` or your IDE's error checker) to catch bugs *before* you run the robot.

---

## 5. Code Example

```python
from typing import TypeVar, List, Any

# --- 1. Define the Generic Type 'T' ---
T = TypeVar('T')

# --- 2. The Generic Function ---
# This function works for ANY list of type T
# It returns a single item of type T
def get_first_item(items: List[T]) -> T:
    if len(items) > 0:
        return items[0]
    raise ValueError("List is empty")

# --- Main Execution ---
def main():
    # A. Using with Integers
    ids = [101, 102, 103]
    first_id = get_first_item(ids) 
    print(f"First ID: {first_id} (Type: {type(first_id)})")

    # B. Using with Strings
    names = ["Rover", "Drone", "Arm"]
    first_name = get_first_item(names)
    print(f"First Name: {first_name} (Type: {type(first_name)})")

    # C. Implicit Logic (The Python Flexibility)
    # Even without T, Python handles mixed types, though it's risky.
    print(f"Max: {max(10, 50)}")       # Built-in Generic
    print(f"Max: {max('A', 'Z')}")     # Built-in Generic

if __name__ == "__main__":
    main()

```

---

## 6. ROS2 Context: "The Publisher Syntax"

In ROS2 Python, you don't use `<T>` brackets like C++, but the concept is identical. You pass the **Type Class** as an argument.

**The ROS2 Pattern:**

```python
# "I want to create a publisher..."
# "...that specifically sends String messages."
# The first argument (String) acts as the Template Type <T>
self.pub_str = self.create_publisher(String, "topic_name", 10)

# "I want to create a publisher..."
# "...that specifically sends Twist commands."
self.pub_vel = self.create_publisher(Twist, "cmd_vel", 10)

```

*Note: The `create_publisher` function is written generically to accept ANY message class you give it.*

---

## 7. Task: "The Universal Printer" ✅

**Scenario:**
You are building a debugging tool. You need a single function that can take any variable (ID, Speed, Name) and print it with a formatted log prefix.

**Requirements:**

1. Define a function `log_info(data: Any)`.
2. **The Logic:** Print `[SYSTEM LOG]: ` followed by the value.
3. **In Main:**
* Create an `id = 101` and log it.
* Create a `battery = 12.5` and log it.
* Create a `status = "Ready"` and log it.
* Create a `list = [1, 2]` and log it.



**Observation:**
You should see 4 clean log lines. You only wrote the print logic **one time**, and Python adapted to every data type automatically.
