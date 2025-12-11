
# Concept 8: Constructors & Destructors (Lifecycle)

## 1\. Deep Explanation (The Logic)

Objects have a **Lifecycle**. They are born, they do work, and they die.
Python gives you special methods to handle these moments.

### A. The Constructor (Birth) – `__init__`

  * **What is it?** A method that runs **automatically** the instant an object is created.
  * **Purpose:** To set up the object. This is where you assign initial values to variables (attributes).
  * **Logic:** You cannot drive a car before turning the key. The `__init__` method is the "Key Turn."

### B. The Destructor (Death) – `__del__`

  * **What is it?** A method that runs **automatically** when an object is destroyed.
  * **Purpose:** To clean up (close files, disconnect Wi-Fi).
  * **Major Difference:** In C++, destruction happens *instantly* when the code block ends. In Python, destruction happens whenever the **Garbage Collector** decides to clean up memory (which might be delayed).
      * *Warning:* Because of this delay, Python programmers rarely use `__del__` for critical logic. We prefer **Context Managers** (the `with` statement) for strict cleanup.

-----

## 2\. Why do we use it?

1.  **Safety:** We never want an "Uninitialized" robot. If a Motor object exists, it must be ready. We put that setup logic in `__init__`.
2.  **Cleanup:** Even though Python manages memory automatically, sometimes you need to manually close a hardware connection.

-----

## 3\. Syntax & Rules

### A. The Constructor (`__init__`)

  * **Name:** Must be exactly `__init__`.
  * **Arguments:** Always takes `self` as the first argument.

### B. The Destructor (`__del__`)

  * **Name:** Must be exactly `__del__`.
  * **Arguments:** Only `self`.

<!-- end list -->

```python
class LidarSensor:
    # Constructor (Runs on creation)
    def __init__(self):
        print("Lidar connecting...")
        self.is_connected = True

    # Destructor (Runs on deletion)
    def __del__(self):
        print("Lidar disconnecting...")
        self.is_connected = False
```

-----

## 4\. The Trap: "The Unreliable Death" ⚠️

In C++, destructors run **exactly** at the closing brace `}`.
In Python, the **Garbage Collector** runs in the background.

  * **The Trap:** If you rely on `__del__` to stop a motor *immediately* when a function ends, it might not happen for a few extra seconds.
  * **The Fix:** For critical hardware cleanup, write an explicit `stop()` method and call it manually, or use a **Context Manager** (`with` statement).

-----

## 5\. Code Example

```python
class NetworkConnection:
    # --- CONSTRUCTOR ---
    # 1. Sets up the variables
    # 2. Prints a message so we see it happen
    def __init__(self, ip):
        self.ip_address = ip
        self.is_connected = True
        print(f"[System] Opening connection to {self.ip_address}...")

    # --- DESTRUCTOR ---
    # Runs when the object is deleted (garbage collected)
    def __del__(self):
        self.is_connected = False
        print(f"[System] Closing connection to {self.ip_address}. Bye!")

    def send_data(self):
        if self.is_connected:
            print("   -> Sending Data packets...")

print("--- Main Program Started ---")

# 1. Scope Start (Simulated by a function)
def create_session():
    print("   [Function Start]")
    # Object is Born -> __init__ Runs
    wifi = NetworkConnection("192.168.1.55") 
    wifi.send_data()
    print("   [Function End]")
    # When this function returns, 'wifi' is no longer needed.
    # Python usually deletes it here.

create_session()

print("--- Back in Main (Object is usually gone) ---")
```

-----

## 6\. ROS2 Context: "The Node Lifecycle"

In ROS2 Python, `__init__` is the most important function you will write.

```python
import rclpy
from rclpy.node import Node

class MyRobot(Node):
    # The Constructor
    def __init__(self):
        # We must initialize the Parent Class (Node) first
        super().__init__("robot_node")
        
        # THIS is where you create Publishers
        self.publisher_ = self.create_publisher(String, "topic", 10)
        
        # THIS is where you create Timers
        self.timer_ = self.create_timer(0.5, self.timer_callback)
        
        # You rarely write logic in the main script. You put setup in __init__.
```

-----

## 7\. Task: "The Secure Session" ✅

**Scenario:**
You are writing a **Logger system**. When a logging session starts, it must print "Log Started". When it ends, it must print "Log Saved & Closed" to ensure data isn't lost.

**Requirements:**

1.  Create a class named `Logger`.
2.  **Constructor:** Print `"--- LOG STARTED ---"`.
3.  **Destructor:** Print `"--- LOG SAVED & CLOSED ---"`.

**In Main:**

1.  Print `"Step 1"`.
2.  Create a function `def test_scope():`.
3.  Inside the function, create a `Logger` object and print `"Step 2 (Inside Function)"`.
4.  Call the function.
5.  Print `"Step 3 (Outside Function)"`.

**Observation:**

  * You should see "LOG SAVED" appear automatically after Step 2 but before Step 3 (or immediately after Step 3 depending on Python's speed).
  * *Note:* To force the destructor to run instantly for testing, you can add the line `del my_logger_object` inside the function, but usually, we let Python handle it.
