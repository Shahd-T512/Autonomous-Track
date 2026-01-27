# Concept 12: Automatic Memory Management (Reference Counting)

## 1. Deep Explanation (The Logic)
In Python, you never have to worry about manually destroying objects to free up RAM. Python uses a built-in system called **Reference Counting** (The Garbage Collector) to handle this for you.

**Think of every object (like a `Robot` or a `List`) as a helium balloon floating in a room.**



* **The Object:** The Balloon. 🎈
* **The Variable:** A string tied to the balloon. 🧶

### The Rules of Gravity:
1.  **Creation:** When you create an object (`bot = Robot()`), you tie **one string** (reference) to it.
2.  **Sharing:** If you assign that variable to another name (`backup_bot = bot`), you tie a **second string** to the same balloon. The balloon is now held by two strings.
3.  **The Count:** Python counts the strings. (Count = 2).
4.  **Destruction:** If you cut the strings (`del` variables) or leave the room (scope ends), the strings fall off.
5.  **The Automatic Cleanup:** The moment the **Reference Count drops to Zero** (no strings attached), the balloon flies away (the memory is deleted instantly).

### The Types of Ownership:

#### A. Shared Ownership (The Default) 🤝
* **Logic:** "I hold this object, but you can hold it too."
* **Mechanism:** In Python, all variables behave this way by default. When you pass an object to a function or assign it to a new variable, you are just increasing the Reference Count. You are **NOT** copying the data.

#### B. Weak Reference (The Observer) 👀
* **Logic:** "I want to look at this object, but I don't want to keep it alive."
* **Use case:** Sometimes you want to check if a robot exists, but if the main program deletes the robot, you don't want your reference to force it to stay in memory. (Python uses the `weakref` library for this).

---

## 2. Why do we use it?
1.  **Safety (No Leaks):** You don't need to remember to clean up. As long as you stop using an object, Python cleans it up.
2.  **Efficiency:** Passing a huge Image object to 5 different functions doesn't copy the image 5 times. It just adds 5 "strings" to the existing image. It's fast and saves RAM.
3.  **ROS2 Standard:** In ROS2, messages are passed around using this exact system. A camera node generates one image, and 10 subscribers just get references to it.

---

## 3. Syntax & Rules

### A. Creating a Shared Reference
You simply use the assignment operator `=`.

```python
# Create an object (Count = 1)
bot_1 = Robot()

# Share the object (Count = 2)
# Both variables point to the exact same memory location
bot_2 = bot_1 

```

### B. Removing a Reference

You can use the `del` keyword, or simply assign the variable to `None`.

```python
# Remove one string (Count drops to 1)
del bot_1 

# Remove the last string (Count drops to 0 -> Object Destroyed)
bot_2 = None 

```

---

## 4. The Trap: "Circular References" ⚠️

* **Scenario:** Object A holds a reference to Object B. Object B holds a reference to Object A.
* **Result:** Even if you delete the main variables, A and B are holding onto each other. The Reference Count never reaches zero.
* **Python's Solution:** Python has a special "Cyclic Garbage Collector" that runs periodically to find these isolated islands of objects holding each other and deletes them. However, it's best to avoid this structure if possible.

---

## 5. Code Example

We will use the `sys` library to peek at the actual Reference Count.

```python
import sys

class Camera:
    def __init__(self):
        print("  [Camera] Powering ON (Allocated in RAM)")

    def __del__(self):
        # This runs automatically when Ref Count hits 0
        print("  [Camera] Powering OFF (Deleted from RAM)")

    def snap(self):
        print("  [Camera] Click!")

def main():
    print("--- Start of Main ---")

    # 1. Create Object
    print("--- Creating Camera ---")
    cam_1 = Camera()
    
    # Note: sys.getrefcount returns (Count + 1) because the function argument itself adds a temp reference.
    # So if it sees 2, the real count is 1.
    print(f"Ref Count: {sys.getrefcount(cam_1) - 1}")

    # 2. Shared Scope
    print("--- Sharing Camera ---")
    cam_2 = cam_1 # We add a second string
    print(f"Ref Count: {sys.getrefcount(cam_1) - 1} (Shared!)")
    
    cam_2.snap()

    # 3. Removing References
    print("--- Deleting cam_1 ---")
    del cam_1 # We cut the first string
    print("  (Object is NOT dead yet, because cam_2 still holds it)")
    
    print("--- Deleting cam_2 ---")
    del cam_2 # We cut the last string
    # The Destructor (__del__) runs AUTOMATICALLY here

    print("--- End of Main ---")

if __name__ == "__main__":
    main()

```

---

## 6. ROS2 Context: "The Shared Node"

In ROS2 Python, this logic is everywhere.
When you create a Node and pass it to an Executor:

```python
# Create the Node object (Count = 1)
my_node = MyRobotNode()

# Pass it to the spinner
# The spinner now holds a reference to the node (Count = 2)
rclpy.spin(my_node)

```

*If the spinner stops and releases the node, and your script ends, the Count drops to 0, and the Node shuts down automatically. You don't need to manually destroy the node object.*

---

## 7. Task: "The Shared Sensor" ✅

**Scenario:**
You have a Lidar data object. Two different variables need to hold it, and we want to verify when it gets deleted from memory.

**Requirements:**

1. Create a class `LidarData`.
* **Constructor (`__init__`):** Print "Data Allocated".
* **Destructor (`__del__`):** Print "Data Freed".


2. **In Main:**
* Create a variable `main_ref` containing a `LidarData` object.
* Create a function `def process_data(data_ref):`.
* Inside the function, print "Processing..." and check the ref count (it should be higher because the function argument is holding it).
* Call the function.
* After the function call returns, set `main_ref = None`.



**Observation:**
Does the "Data Freed" message appear **immediately** after you set `main_ref = None`?

*Goal: This proves you understand that the object stays alive exactly as long as something is holding a reference to it.*
