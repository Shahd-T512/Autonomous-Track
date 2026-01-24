
# Concept 10: Polymorphism (Virtual Functions & Override)

## 1. Deep Explanation (The Logic)
Polymorphism (Greek for "Many Shapes") allows different objects to respond to the **same command** in their own unique way.

**Imagine you have a Drone and a Rover.**
* They move differently (Fly vs. Roll).
* However, you want to treat them both simply as "Robots."



### The Problem:
If you create a generic pointer `Robot* my_bot` and point it to a Drone, and then call `my_bot->move()`, C++ normally looks at the **Pointer Type** (Robot). It runs the generic Robot move code (which might do nothing), ignoring the special Drone flight code.

### The Solution (`virtual`):
By marking a function as **`virtual`** in the Parent, you tell C++:
> *"Do not look at the pointer type. Look at the **Actual Object** in memory."*

This allows the program to decide **while it is running** which function to call. This is called **Dynamic Dispatch**.

---

## 2. Why do we use it? (The "Universal Interface")
1.  **Scalability:**
    * You can write a function `shutdownAll(std::vector<Robot*> list)`.
    * It loops through the list calling `stop()`.
    * The Drones land, the Rovers brake, and the Arms lock. The function doesn't need to know *what* they are, only that they are Robots.
2.  **Hardware Abstraction:**
    * In ROS2, you might have a base class `Sensor`.
    * You can swap a `RealLidar` with a `SimulatedLidar` without changing a single line of your main algorithm, as long as both override the `read()` function.

---

## 3. Syntax & Rules

### A. The Parent (Base Class)
Add `virtual` to functions you expect children to change.

```cpp
class Robot {
public:
    virtual void move() { 
        std::cout << "Robot moving generic...\n"; 
    }
};
````

### B. The Child (Derived Class)

Add `override` to ensure you are actually replacing the parent's function (Safety feature).

```cpp
class Drone : public Robot {
public:
    void move() override { 
        std::cout << "Drone is Flying!\n"; 
    }
};
```

-----

## 4\. The Trap: "The Missing Virtual" ⚠️

If you forget the word `virtual` in the Parent class:

  * **Scenario:** You point a `Robot*` to a `Drone`.
  * **Action:** You call `move()`.
  * **Result:** The **Parent's code runs** ("Robot moving generic"). The Drone logic is ignored completely. This is a common bug when designing interfaces.

-----

## 5\. Code Example

```cpp
#include <iostream>
#include <vector>

// --- 1. The Interface (Abstract Idea) ---
class Sensor {
public:
    // 'virtual' allows the child to replace this behavior
    virtual void readData() {
        std::cout << "[Base] Reading generic data...\n";
    }
};

// --- 2. Specific Implementations ---
class Lidar : public Sensor {
public:
    void readData() override {
        std::cout << "[Lidar] Scanning 360 degrees for obstacles.\n";
    }
};

class Camera : public Sensor {
public:
    void readData() override {
        std::cout << "[Camera] Capturing RGB image.\n";
    }
};

int main() {
    // --- 3. The Power of Polymorphism ---
    
    Lidar my_lidar;
    Camera my_cam;

    // We create a list of POINTERS to the Base class
    // This vector can hold ANY type of sensor
    std::vector<Sensor*> sensor_list;
    
    sensor_list.push_back(&my_lidar);
    sensor_list.push_back(&my_cam);

    std::cout << "--- System Update ---\n";
    
    // We loop through them as generic "Sensors"
    for (Sensor* s : sensor_list) {
        // Because of 'virtual', C++ finds the specific version of readData()
        // If readData() was NOT virtual, this would print "[Base]..." every time.
        s->readData(); 
    }

    return 0;
}
```

-----

## 6\. ROS2 Context: "Lifecycle Nodes"

ROS2 relies heavily on this for **Managed Nodes (Lifecycle)**.

1.  **The Concept:** ROS2 provides a base class called `LifecycleNode`. It has virtual methods like `on_configure()`, `on_activate()`, and `on_deactivate()`.
2.  **Your Job:** You create your node and **Override** these methods.
3.  **The Result:**
      * When the ROS2 system sends the "Configure" signal, it triggers **your** overridden function to connect to hardware.
      * When it sends "Activate", it triggers **your** overridden function to start publishing data.

-----


### **Task 7: The Payment Gateway (Polymorphism)**

**Scenario:**
You are developing the software for a modern vending machine. The machine needs to handle different payment methods (like Credit Cards and Cash) uniformly using a single interface.

**Requirements:**

1. **Create a Base Class** named `PaymentMethod`:
* Add a public function: `virtual void pay(double amount)`.
* **Default Behavior:** It should print `"Generic Payment processing..."`.
* *Note: The `virtual` keyword is crucial here to enable Polymorphism.*


2. **Create a Derived Class** named `CreditCard` that inherits from `PaymentMethod`:
* **Override** the `pay` function.
* **New Behavior:** It should print `"Processing Credit Card payment of $[amount]"`.


3. **Create a Derived Class** named `Cash` that inherits from `PaymentMethod`:
* **Override** the `pay` function.
* **New Behavior:** It should print `"Accepting Cash payment of $[amount]"`.



**The Challenge (In Main Function):**

1. Instantiate a `CreditCard` object (e.g., `myCard`).
2. Create a **Base Class Reference** named `paymentSystem` that refers to `myCard`:
* Syntax hint: `PaymentMethod& paymentSystem = myCard;`


3. Call `paymentSystem.pay(15.50);`.

**Success Criteria:**

* If the console prints **"Processing Credit Card payment..."**, you have successfully implemented Polymorphism using references.
* If it prints **"Generic Payment processing..."**, the virtual dispatch failed (check your `virtual` keyword!).
