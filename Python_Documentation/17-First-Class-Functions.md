
# Concept 17: First-Class Functions (Storing Logic)

## 1. Deep Explanation (The Logic)
Normally, a variable holds **Data** (`x = 5`).
In Python, a variable can also hold **Code**.

### The Concept:
Functions in Python are **"First-Class Citizens."** This means a function is just an **object**, like an integer or a string.



* **Flexibility:** You can create a variable named `my_job`.
    * Today, you can store a "Print Function" inside `my_job`.
    * Tomorrow, you can store a "Math Lambda" inside `my_job`.
    * When you run `my_job()`, it just executes whatever is currently inside.

---

## 2. Why do we use it? (Callbacks)
**The "Don't Call Us, We'll Call You" Principle:**

In robotics, we often write a generic **"Button Handler"** class. This class doesn't know what the button does (Launch missile? Turn on light?).



1.  We give the class a generic variable named `on_click`.
2.  The user injects their specific **function** into that variable.
3.  When the button is pressed, the class just runs `on_click()`.

---

## 3. Syntax & Rules
You don't need any special libraries.

### Storing a Function
**Crucial Distinction:**
* **`func()` (With parentheses):** Runs the function and gives you the **result**.
* **`func` (Without parentheses):** Gives you the **function itself** (the code object) so you can store it.

```python
def say_hi():
    print("Hi!")

# Store the logic in a variable
stored_logic = say_hi 

# Run it later
stored_logic()

```

---

## 4. The Trap: "Not Callable" ⚠️

Just like a variable can be empty (`None`), a function variable might not hold code yet.

* **The Bug:** You declare `action = None` but forget to assign a real function to it.
* **The Crash:** If you try to call `action()`, Python crashes with:
`TypeError: 'NoneType' object is not callable`
* **The Fix:** Always check if it is valid or use `callable()` before calling.

```python
if action is not None:
    action()

```

---

## 5. Code Example

```python
# A normal function
def turn_on_light(brightness):
    print(f"Light ON at level {brightness}")

# 1. Create the container
# We start with None (Empty)
action = None

# 2. Assign a Standard Function
# Notice: No parentheses! We are moving the logic, not running it.
action = turn_on_light # Now 'action' acts exactly like 'turn_on_light'

action(50) 

# 3. Assign a Lambda (The logic changes dynamically!)
# We overwrite the variable with new logic.
action = lambda v: print(f"Motor Speed set to {v} RPM")

action(100) # Now it calls the Lambda logic

# 4. Safety Check
empty_action = None

# Always check before calling
if empty_action is not None:
    empty_action(10)
else:
    print("Safety: Variable is empty. Did not call.")

```

---

## 6. ROS2 Context: "Storing Callbacks"

In ROS2, this is how the system stores your logic.
When you create a Subscriber, you pass your function to ROS2:

```python
# You define the logic
def my_callback(msg):
    print(msg.data)

# You pass the function object to ROS2
# ROS2 stores 'my_callback' in a variable and runs it when data arrives.
self.create_subscription(String, "topic_name", my_callback, 10)

```

*Notice we pass `my_callback`, NOT `my_callback()`.*

---

## 7. Task: "The Programmable Button" ✅

**Scenario:**
You are building a generic "Emergency Button" system. The button can be configured to do different things (Stop Motors, Sound Alarm, or Reboot).

**Requirements:**

1. Define a variable `emergency_protocol = None`.
2. **The Logic Puzzle:**
* Define a function `def stop_motors(): print("Motors Stopped")`.
* Assign `stop_motors` to your `emergency_protocol` variable.
* Call the variable. (Output should be "Motors Stopped").
* **Re-assign** the variable to a **Lambda** that prints "ALARM SOUNDING!".
* Call the variable again.



**Goal:**
This proves you can swap the behavior of a system at runtime without changing the system's core code.
