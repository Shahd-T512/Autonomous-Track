
# Concept 8: Constructors & Destructors (Lifecycle)

## 1. Deep Explanation (The Logic)
Objects in C++ have a **Lifecycle**. They are born, they do work, and they die.
C++ gives you two special functions to handle the exact moment of birth and death automatically.



### A. The Constructor (Birth) 
* **What is it?** A function that runs **automatically** the instant an object is created.
* **Purpose:** To set up the object. You initialize variables, open files, or connect to hardware.
* **Logic:** You cannot drive a car before turning the key. The Constructor is the "Key Turn."

### B. The Destructor (Death) 💀
* **What is it?** A function that runs **automatically** the instant an object is destroyed (goes out of scope).
* **Purpose:** To clean up. You close files, disconnect from Wi-Fi, or free up memory.
* **Logic:** If you leave the house (scope), you must turn off the lights (Destructor). If you don't, you waste electricity (**Memory Leak**).

---

## 2. Why do we use it? (RAII)
There is a famous C++ philosophy called **RAII (Resource Acquisition Is Initialization)**.

1.  **Safety:** We never want an "Uninitialized" robot. If a Motor object exists, it must be connected and ready. We put that logic in the Constructor.
2.  **Cleanup:** If your code crashes or finishes a function, the Destructor runs automatically. This ensures the robot doesn't leave motors spinning or cameras recording forever.

---

## 3. Syntax & Rules

### A. The Constructor
* **Name:** Must be **exactly the same** as the Class name.
* **Return Type:** None (not even `void`).
* **Overloading:** You can have multiple constructors (one with no arguments, one with arguments).

### B. The Destructor
* **Name:** Same as Class name but with a **Tilde (`~`)** in front.
* **Arguments:** None. You cannot pass data to a destructor; it runs on its own.

```cpp
class LidarSensor {
public:
    // Constructor (Runs on creation)
    LidarSensor() {
        // Code to connect to hardware
    }

    // Destructor (Runs on deletion)
    ~LidarSensor() {
        // Code to disconnect/shutdown
    }
};
````

-----

## 4\. The Trap: "The Default Constructor" ⚠️

If you write a class without a constructor, C++ creates a "hidden" empty one for you.

  * **The Bug:** The hidden constructor does not set variables to zero.
  * **Result:** `int speed` inside the class will contain **garbage data**.
  * **Fix:** Always write your own constructor to initialize variables to `0`, `false`, or `NULL`.

-----

## 5\. Code Example

```cpp
#include <iostream>
#include <string>

class NetworkConnection {
private:
    std::string ip_address;
    bool is_connected;

public:
    // --- CONSTRUCTOR ---
    // 1. Sets up the variables
    // 2. Prints a message so we see it happen
    NetworkConnection(std::string ip) {
        ip_address = ip;
        is_connected = true;
        std::cout << "[System] Opening connection to " << ip_address << "...\n";
    }

    // --- DESTRUCTOR ---
    // Note the '~' symbol
    // Runs automatically when the object is deleted
    ~NetworkConnection() {
        is_connected = false;
        std::cout << "[System] Closing connection to " << ip_address << ". Bye!\n";
    }

    void sendData() {
        if (is_connected) std::cout << "   -> Sending Data packets...\n";
    }
};

int main() {
    std::cout << "--- Main Function Started ---\n";

    // 1. Scope Start
    {
        // Object is Born -> Constructor Runs
        NetworkConnection wifi("192.168.1.55"); 
        
        wifi.sendData();
        
        // 2. Scope End (The closing bracket '}')
        // The object dies here -> Destructor Runs AUTOMATICALLY
    } 

    std::cout << "--- Back in Main (Object is gone) ---\n";

    return 0;
}
```

-----

## 6\. ROS2 Context: "The Node Lifecycle"

In ROS2, almost everything happens in the Constructor.

When you create a Class for your Robot Node:

```cpp
class MyRobot : public rclcpp::Node {
public:
    // The Constructor
    MyRobot() : Node("robot_node") {
        // THIS is where you create Publishers
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        
        // THIS is where you create Timers
        timer_ = this->create_wall_timer(500ms, ...);
        
        // You rarely write logic in main(). You put the setup in the Constructor.
    }
};
```

*Note: The Destructor is less visible in ROS2 because "Smart Pointers" usually handle the cleanup, but it is still used to shut down hardware drivers safely (e.g., sending a stop command to the wheels before the program quits).*

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
2.  Create a Scope using curly braces `{ }`.
3.  Inside the scope, create a `Logger` object.
4.  Print `"Step 2 (Inside Scope)"`.
5.  Close the scope `}`.
6.  Print `"Step 3 (Outside Scope)"`.

**Observation:**
Look at the order of prints in the terminal.

  * Did "LOG SAVED" appear **before** "Step 3"?
  * *If yes, you have successfully understood how Destructors automate cleanup.*
