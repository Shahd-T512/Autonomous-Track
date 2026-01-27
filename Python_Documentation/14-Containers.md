
# Concept 14: Containers (Lists, Dictionaries, Tuples)

## 1. Deep Explanation (The Logic)
In Python, we rely on **Data Structures** to hold collections of data. Unlike standard variables that hold one value, these Containers act like **"Warehouses"** that can hold many values at once.



### The Big Three:

#### 1. `list` (The Dynamic Backpack) 🎒
* **Equivalent to:** `std::vector` in C++.
* **Description:** An **ordered** collection. You can throw items in, and it expands automatically. You can remove items, and it shrinks.
* **Logic:** Use this for 90% of your sequences (Lidar points, Waypoints, Sensor logs).

#### 2. `dict` (The Dictionary) 📖
* **Equivalent to:** `std::map` in C++.
* **Description:** **Key-Value** pairs. You don't look up by Index (0, 1, 2); you look up by **Name (Key)**.
* **Logic:** "Give me the motor ID for `'Left_Wheel'`".

#### 3. `tuple` (The Safe Fixed List) 📦
* **Equivalent to:** `std::array` (mostly).
* **Description:** Like a list, but **Immutable**. Once you create it, you **cannot** add, remove, or change items.
* **Logic:** Use this for things that never change size (e.g., a coordinate pair `(x, y)` or a color `(r, g, b)`).

---

## 2. Why do we use it?
1.  **Growth:** You don't know how many obstacles the Lidar will see. It could be 5, it could be 500. A `list` handles this variable size perfectly.
2.  **Lookup Speed:** If you have 1000 configuration parameters, finding one by name using a `dict` is much cleaner and faster than looping through a list to find it.

---

## 3. Syntax & Rules

### A. List (Dynamic)
```python
distances = []        # Create empty list
distances.append(50)  # Add 50 to the end
distances.append(25)  # Add 25 to the end

```

### B. Dictionary (Key-Value)

```python
# Create dictionary with data
config = {
    "speed": 100, 
    "mode": "auto"
}

# Accessing
print(config["speed"]) # Prints 100

```

---

## 4. The Trap: "IndexError" & "KeyError" ⚠️

### The List Bug:

You have a list of size 3. You try to access `my_list[10]`.

* **Result:** Python raises an `IndexError`.

### The Dict Bug (Crucial Difference from C++):

You try to access `my_dict["missing_key"]`.

* **Result:** Python raises a **`KeyError`**.
* *Note: This is different from C++, which sometimes creates the key automatically with a default value.*

### The Fix (Safe Access):

For dictionaries, use `.get()`. It returns `None` (or a default value) instead of crashing if the key is missing.

```python
val = config.get("laser_scan") # Returns None (Safe)
# val = config["laser_scan"]   # CRASH (Unsafe)

```

---

## 5. Code Example

```python
# --- 1. List (List of Sensor Readings) ---
sensor_data = []

# Adding data dynamically
sensor_data.append(1.5)
sensor_data.append(4.2)
sensor_data.append(0.8)

print(f"List Size: {len(sensor_data)}") # Prints 3

# Iterating
print("Readings:", end=" ")
for val in sensor_data:
    print(val, end=" ")
print()

# --- 2. Dictionary (Robot Configuration) ---
config = {}

config["Max_Speed"] = 2.5
config["Battery_Threshold"] = 12.0

# Accessing by Name
print("Fetching Config...")
print(f"Speed Limit: {config['Max_Speed']} m/s")

# --- 3. Safety Check (The Trap) ---
# print(sensor_data[100]) # This would crash with IndexError

```

---

## 6. ROS2 Context: "The Universal Message"

ROS2 messages rely heavily on Lists.

* **Unbounded Arrays:** In a `.msg` file, if you write `float64[] ranges`, ROS2 converts this into a **Python list** of floats.
* **Path Planning:** A path is just a `list` of `PoseStamped` (Coordinate points). You append points into the list and publish it for the robot to follow.

---

## 7. Task: "The Inventory Manager" ✅

**Scenario:**
You are managing the spare parts for the team. You need a system to count how many of each item you have.

**Requirements:**

1. Create a `dict`: Keys are strings (Item Name), Values are ints (Count).
2. **Add Initial Items:**
* "Wheel": 4
* "Motor": 2
* "Sensor": 5


3. **The Logic Puzzle:**
* A robot crashes and breaks a wheel. Subtract 1 from "Wheel".
* The team buys 3 new Motors. Add 3 to "Motor".
* **Try to print the count of a non-existent item** (e.g., "Laser") using standard access `inventory["Laser"]`.



**Output:**
Does the program crash?

**Observation:**

* **In C++:** It would print 0 (it creates the entry).
* **In Python:** It will **Crash** with a `KeyError`.
* **Fix:** Use `inventory.get("Laser", 0)` to safely print 0 if the item doesn't exist.
