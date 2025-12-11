
# Concept 4: Classes (Dataclasses), Enums & Mutable Objects

## 1\. Deep Explanation (The Logic)

We are now building the **"Vocabulary"** of our robot's code. In Python, we use slightly different tools to achieve the same "Data Bag" and "Label" goals.

### A. Dataclasses (The "Data Bag")

In Python, the equivalent of a C++ Struct is often a **Class** (specifically a **Dataclass**).

  * **Without Dataclass:** You carry an Apple, a Pen, and a Book separately in your hands.
  * **With Dataclass:** You put them all in a **Backpack** (Object). You just pass the Backpack around.

### B. Enums (The "Labels")

Computers like numbers (0, 1, 2). Humans like words (STOP, GO, WAIT).
Python uses the `Enum` library to map readable names to values.

  * Instead of writing `if robot_mode == 2:`, you write `if robot_mode == State.EMERGENCY:`.
  * This removes **"Magic Numbers"** from your code, making it readable and less buggy.

### C. Passing by Reference (Python's Default Behavior)

This is a **major difference** from C++.

  * **C++:** By default, it copies data. You have to force it to use a Reference (`&`).
  * **Python:** **Everything is a Reference by default.**
      * If you pass a "Backpack" (an Object/Dataclass) to a function, Python simply passes the handle to the *existing* backpack. It does **not** create a copy.
      * If you modify the contents of the backpack inside the function, the original backpack changes.

-----

## 2\. Why do we use it?

  * **State Machines (Enums):** Robots always have states (Idle, Docking, Charging). Enums are the standard way to manage this.
  * **Clean Interfaces (Dataclasses):** Instead of a function taking 10 parameters (`func(x, y, z, r, p, y, vel...)`), we create a Dataclass `State` and pass just one parameter (`func(state)`).
  * **Efficiency:** Since Python passes objects by reference automatically, you don't need to worry about the memory cost of copying large image data frames—it simply doesn't happen unless you explicitly ask for a copy.

-----

## 3\. Syntax & Rules

### A. Defining an Enum

You need to import `Enum`.

```python
from enum import Enum

class State(Enum):
    IDLE = 0
    RUNNING = 1
    ERROR = 2
```

### B. Defining a Dataclass (The Struct Equivalent)

We use the `@dataclass` decorator to automatically write the setup code for us.

```python
from dataclasses import dataclass

@dataclass
class RobotData:
    id: int
    voltage: float
    current_state: State  # Using the Enum inside the Dataclass
```

### C. Passing to Functions

No special symbols (like `&`) are needed. Objects are mutable (changeable) by default.

```python
def update_robot(data):
    # 'data' refers to the ORIGINAL object.
    data.voltage = 12.0 
```

-----

## 4\. The Trap: "Magic Numbers" ⚠️

A **"Magic Number"** is a raw number in code with no explanation.

  * **Bad Code:** `if state == 3:`
      * *Problem:* What is 3? Is it "Error"? Is it "Shutdown"? If you come back in 6 months, you won't know.
  * **Good Code:** `if state == State.SHUTDOWN:`

-----

## 5\. Code Example

```python
from enum import Enum
from dataclasses import dataclass

# 1. Define the States (Labels)
class ConnectionState(Enum):
    DISCONNECTED = 0
    CONNECTING = 1
    CONNECTED = 2
    FAILED = 3

# 2. Define the Data Package (Dataclass)
@dataclass
class WifiModule:
    ip_address: str
    signal_strength: int
    status: ConnectionState  # Putting the Enum inside

# 3. Function taking the Object
# In Python, 'mod' is a reference to the original object.
def attempt_connection(mod):
    print(f"Connecting to {mod.ip_address}...")
    
    # Simulate logic
    if mod.signal_strength > 50:
        # We are modifying the ORIGINAL object here
        mod.status = ConnectionState.CONNECTED
    else:
        mod.status = ConnectionState.FAILED

# Helper to print Enum
def print_status(mod):
    # Match-Case works great with Enums in Python!
    match mod.status:
        case ConnectionState.CONNECTED:
            print("Status: ONLINE")
        case ConnectionState.FAILED:
            print("Status: ERROR")
        case _:
            print("Status: WAITING")

# Main Execution
# Initialize Dataclass
my_wifi = WifiModule("192.168.1.50", 80, ConnectionState.DISCONNECTED)

print_status(my_wifi) # Prints WAITING

# Pass Object (Original 'my_wifi' is modified automatically)
attempt_connection(my_wifi)

print_status(my_wifi) # Prints ONLINE
```

-----

## 6\. ROS2 Context: "Goal Responses"

ROS2 uses this pattern everywhere.

1.  **Enums for Results:** When you ask a navigation robot to move, it returns a status code. In the Python ROS2 libraries, these are often Constants or Enums:
      * `GoalStatus.STATUS_SUCCEEDED`
      * `GoalStatus.STATUS_ABORTED`
      * `GoalStatus.STATUS_CANCELED`
2.  **Classes for Config:** ROS2 messages in Python are essentially Classes. You populate the class fields (like `cmd_vel.linear.x`) and pass the whole object to the publisher.

-----

## 7\. Task: The "Traffic Light" Logic ✅

**Scenario:**
You are simulating a traffic light controller. You need to switch the lights in order.

**Requirements:**

1.  Define an Enum named `LightColor` with values: `RED`, `YELLOW`, `GREEN`.
2.  Define a Dataclass named `TrafficLight` containing:
      * `color: LightColor`
      * `timer_seconds: int`
3.  Define a Function `def update_light(light):`.

**The Logic Puzzle:**
Inside the function, check the current color and switch to the next one:

  * If `RED` $\rightarrow$ Change to `GREEN`, set timer to 30.
  * If `GREEN` $\rightarrow$ Change to `YELLOW`, set timer to 5.
  * If `YELLOW` $\rightarrow$ Change to `RED`, set timer to 60.

**In Main:**

1.  Create a `TrafficLight` object starting at `RED` (timer 60).
2.  Call `update_light` twice.
3.  Print the final state (Should be `YELLOW` if you called it twice).

*Goal: This proves you can manipulate the "State" of an object using Enums and Python's object passing.*
