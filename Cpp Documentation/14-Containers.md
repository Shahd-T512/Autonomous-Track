
# Concept 14: Containers (Vector, Map, Array)

## 1. Deep Explanation (The Logic)
In standard C++, we rarely use raw arrays (`int arr[10]`) because they are "dumb." They cannot grow, they don't know their own size, and they crash easily.

Instead, we use **STL Containers** (Standard Template Library). These are smart data structures that handle memory for you.
* *Analogy:* If Variables are "Boxes," Containers are **"Warehouses."**



### The Big Three:

#### 1. `std::vector` (The Dynamic List) 🎒
* **Description:** Like a magic backpack. You can throw items in, and it expands automatically. You can remove items, and it shrinks.
* **Logic:** Use this for 90% of your lists (Lidar points, Waypoints).

#### 2. `std::map` (The Dictionary) 📖
* **Description:** Key-Value pairs. You don't look up by Index (0, 1, 2); you look up by **Name (Key)**.
* **Logic:** "Give me the motor ID for `'Left_Wheel'`".

#### 3. `std::array` (The Safe Fixed List) 📦
* **Description:** Like a raw array, but safer. The size is fixed at compile time.
* **Logic:** Use this for things that **never** change size (e.g., a 3x3 Transformation Matrix).

---

## 2. Why do we use it?
1.  **Growth:** You don't know how many obstacles the Lidar will see. It could be 5, it could be 500. `std::vector` handles this variable size perfectly.
2.  **Lookup Speed:** If you have 1000 params, finding one by name using `std::map` is much cleaner than writing a giant `if-else` block.

---

## 3. Syntax & Rules
You must include the headers: `#include <vector>` or `#include <map>`.

### A. Vector (Dynamic)
```cpp
std::vector<int> distances; 
distances.push_back(50); // Add 50 to the end
distances.push_back(25); // Add 25 to the end (Size is now 2)

```
Read more: https://www.geeksforgeeks.org/cpp/vector-in-cpp-stl/

### B. Map (Key-Value)

```cpp
#include <iostream>
#include <map>

int main() {
    
    // Creating an empty map
    std::map<int, string> m1;

    // Initialze map with list
    std::map<int, string> m2 = {{1, "Geeks"},
              {2, "For"}, {3, "Geeks"}};

    for (auto& p : m2)
        cout << p.first << " " <<
        p.second << endl;
    return 0;
}

```
Read More: https://www.geeksforgeeks.org/cpp/map-associative-containers-the-c-standard-template-library-stl/

---

## 4. The Trap: "Out of Range" ⚠️

* **The Bug:** You have a vector of size 3. You try to access `vec[10]`.
* **The Result:** Raw arrays will let you do this (and crash later). `std::vector` has a safer option.

| Method | Behavior |
| --- | --- |
| `vec[10]` | **Fast**, but dangerous (No checks). Can cause Segfault. |
| `vec.at(10)` | **Safer**. If index is wrong, it throws an error instantly ("Out of Range Exception"). |

---

## 5. Code Example

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <string>

int main() {
    // --- 1. Vector (List of Sensor Readings) ---
    std::vector<double> sensor_data;

    // Adding data dynamically
    sensor_data.push_back(1.5);
    sensor_data.push_back(4.2);
    sensor_data.push_back(0.8);

    std::cout << "Vector Size: " << sensor_data.size() << "\n"; // Prints 3

    // Iterating
    std::cout << "Readings: ";
    for (double val : sensor_data) {
        std::cout << val << " ";
    }
    std::cout << "\n";

    // --- 2. Map (Robot Configuration) ---
    std::map<std::string, double> config;
    
    config["Max_Speed"] = 2.5;
    config["Battery_Threshold"] = 12.0;

    // Accessing by Name
    std::cout << "Fetching Config...\n";
    std::cout << "Speed Limit: " << config["Max_Speed"] << " m/s\n";

    // --- 3. Safety Check (The Trap) ---
    // sensor_data.at(100); // This would throw a helpful error message.

    return 0;
}

```

---

## 6. ROS2 Context: "The Universal Message"

ROS2 messages rely heavily on vectors.

1. **Unbounded Arrays:** In a `.msg` file, if you write `float64[] ranges`, ROS2 converts this into `std::vector<double>` in C++.
2. **Path Planning:** A path is just a `std::vector` of `PoseStamped` (Coordinate points). You push points into the vector and publish it for the robot to follow.

---

## 7. Task: "The Inventory Manager" ✅

**Scenario:**
You are managing the spare parts for the team. You need a system to count how many of each item you have.

**Requirements:**

1. Create a `Map`: Key is `std::string` (Item Name), Value is `int` (Count).
2. **Add Initial Items:**
* "Wheel": 4
* "Motor": 2
* "Sensor": 5


3. **The Logic Puzzle:**
* A robot crashes and breaks a wheel. Subtract 1 from "Wheel".
* The team buys 3 new Motors. Add 3 to "Motor".
* **Try to print the count of a non-existent item** (e.g., "Laser").



**Output:**
Print the final counts for all items.

**Observation:**
When you accessed "Laser" (which you never added), did the map crash, or did it automatically create it with value 0?

* *(Map Feature: It creates a default entry if the key doesn't exist).*
