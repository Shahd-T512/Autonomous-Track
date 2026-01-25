
# Concept 18: Templates (Generics)

## 1. Deep Explanation (The Logic)
In standard functions, you must be specific.
* `int add(int a, int b)` works only for Integers.
* If you want to add two Doubles, you have to write a new function: `double add(double a, double b)`.

### The Solution:
**Templates** allow you to write a **"Mold"** or **"Pattern"** for a function. Instead of picking a specific data type (like `int`), you use a **Placeholder** (usually named `T`).

When you run the code, you tell C++: *"Use the mold, but treat `T` as a double this time."*



**Analogy:** Think of a **Cookie Cutter**. The shape (the Logic) is the same, but the dough (the Data Type) can be chocolate, vanilla, or gingerbread.

---

## 2. Why do we use it?
1.  **Code Reusability:** You write the logic **once**. It works for `int`, `float`, `Robot`, `LaserScan`, or any future type you invent.
2.  **ROS2 Architecture:** ROS2 developers didn't want to write `create_publisher_int`, `create_publisher_string`, `create_publisher_image`.
    * They wrote **one function**: `create_publisher<T>`.
    * You fill in the `<T>` with your specific message type.

---

## 3. Syntax & Rules

### A. Defining the Template
We use the keyword `template <typename T>` (or `template <class T>`) right before the function.

```cpp
// The "Mold"
template <typename T>
T add_numbers(T a, T b) {
    return a + b;
}

```

### B. Using the Template

We use angled brackets `< >` to specify the type.

```cpp
int x = add_numbers<int>(5, 10);        // T becomes int
double y = add_numbers<double>(5.5, 2.2); // T becomes double

```

---

## 4. The Trap: "The Linker Error" ⚠️

Templates are unique because they are processed at **Compile Time**, not Run Time.

* **The Bug:** If you put the *Declaration* of a template in a Header file (`.h`) and the *Implementation* in a Source file (`.cpp`), the compiler often fails to link them.
* **The Fix:** Unlike normal functions, Template code usually lives **entirely inside the Header File (.hpp)**.

---

## 5. Code Example

```cpp
#include <iostream>
#include <string>

// --- 1. The Generic Template ---
// This function can check which of two items is "Maximum"
// It works for ANY type that supports the '>' operator.
template <typename T>
T findMax(T a, T b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int main() {
    // --- 2. Using with Integers ---
    std::cout << "Max Int: " << findMax<int>(10, 50) << "\n";

    // --- 3. Using with Doubles ---
    std::cout << "Max Double: " << findMax<double>(5.5, 5.7) << "\n";

    // --- 4. Using with Strings ---
    // (Strings are compared alphabetically)
    std::string s1 = "Apple";
    std::string s2 = "Banana";
    std::cout << "Max String: " << findMax<std::string>(s1, s2) << "\n";

    return 0;
}

```

---

## 6. ROS2 Context: "The Publisher Syntax"

In ROS2, you will encounter templates immediately when creating communication channels.

**The ROS2 Pattern:**

```cpp
// "I want to create a publisher..."
// "...that specifically sends String messages."
publisher_ = this->create_publisher<std_msgs::msg::String>("topic_name", 10);

// "I want to create a publisher..."
// "...that specifically sends Velocity commands."
cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);

```

*Note: The logic of "publishing" is identical in both lines. The only difference is the Data Type `<T>` inside the brackets.*

---

## 7. Task: "The Universal Printer" ✅

**Scenario:**
You are building a debugging tool. You need a single function that can take any variable (ID, Speed, Name) and print it with a formatted log prefix.

**Requirements:**

1. Write a function template named `logInfo`.
2. It accepts one argument of type `T`.
3. **The Logic:** Print `[SYSTEM LOG]: ` followed by the value and a newline.

**In Main:**

1. Create an `int id = 101;` and log it.
2. Create a `double battery = 12.5;` and log it.
3. Create a `std::string status = "Ready";` and log it.

**Observation:**
You should see 3 clean log lines. You only wrote the `cout` logic **one time**.
