
# Concept 7: Access Specifiers (Public, Protected, Private)

## 1\. Deep Explanation (The Logic)

In OOP, we don't want every part of the code to touch every variable. If a variable is critical (like the robot's main voltage), we want to lock it away so no one changes it accidentally.

**The Python Difference:**
C++ uses **Compiler Enforcement** (it stops the code from building).
Python uses **Naming Conventions** (it trusts you to behave). Python follows the philosophy: *"We are all consenting adults here."*

1.  **Public (The Storefront):**

      * **Syntax:** `self.variable` (No underscores).
      * **Who can access?** Everyone.
      * **Usage:** The "User Interface." Functions like `start_engine()` or variables meant to be shared.

2.  **Protected (The "Internal Use" Sign):**

      * **Syntax:** `self._variable` (One underscore).
      * **Meaning:** "Please do not touch this unless you are working inside this class or a Child class."
      * **Enforcement:** None. Python allows you to touch it, but it is considered bad manners and risky.

3.  **Private (The Hidden Vault):**

      * **Syntax:** `self.__variable` (Two underscores).
      * **Meaning:** "This is strictly for this specific class."
      * **Enforcement:** **Name Mangling.** Python secretly renames this variable to `_ClassName__variable` so you cannot accidentally access it using its original name.

-----

## 2\. Why do we use it? (Encapsulation)

  * **Safety:** Imagine a `Motor` class. If the internal variable `pwm_value` is **Public**, a lazy programmer might write `motor.pwm_value = 99999` in the main script, burning the motor.
  * **Encapsulation:** If we make it **Private** (`self.__pwm_value`), the programmer is forced to use `motor.set_speed(100)`. Inside that function, we write logic: *"If value \> 255, set to 255."* This protects the hardware.

-----

## 3\. Syntax & Rules

```python
class Robot:
    def __init__(self):
        # Public: Accessible by everyone
        self.status = "Idle"

        # Protected: Accessible, but meant for internal use/inheritance
        self._hardware_id = 101 

        # Private: Hard to access from outside
        # Python renames this to _Robot__internal_voltage
        self.__internal_voltage = 12.0

    def boot_up(self):
        # We can access everything inside the class
        self.__start_internal_systems()

    def __start_internal_systems(self):
        # This is a Private Method
        self.__internal_voltage = 12.0
```

-----

## 4\. The Trap: "The Illusion of Security" ⚠️

In C++, you *cannot* access a private variable. In Python, you *can* if you know the secret password (the mangled name).

  * **The Bug:** You assume `self.__secret` is totally safe.
  * **The Reality:** A hacker or a desperate developer can still access it by writing `object._ClassName__secret`.
  * **The Lesson:** Python's privacy is about **preventing accidents**, not preventing malicious attacks.

-----

## 5\. Code Example

```python
class SafeMotor:
    def __init__(self):
        # DATA IS PRIVATE (Double Underscore)
        # No one outside can mess with this variable easily.
        self.__speed_limit = 100
        self.__current_speed = 0

    # INTERFACE IS PUBLIC
    # This provides a safe way to set speed.
    def set_speed(self, s):
        if s > self.__speed_limit:
            print(f"Error: {s} exceeds limit! Clamped to {self.__speed_limit}.")
            self.__current_speed = self.__speed_limit
        elif s < 0:
            print("Error: Negative speed not allowed. Stopping.")
            self.__current_speed = 0
        else:
            self.__current_speed = s
            print(f"Speed set to: {self.__current_speed}")

    def get_speed(self):
        return self.__current_speed

# Main Execution
m = SafeMotor()

# m.__current_speed = 500  # ERROR! AttributeError: 'SafeMotor' object has no attribute '__current_speed'
# m.__speed_limit = 200    # ERROR! 

# Correct Usage
m.set_speed(50)   # Works
m.set_speed(200)  # Triggers internal safety check

# Proving Name Mangling (Just for learning - Don't do this in real code!)
# We can access it if we use the "Mangled Name"
print(f"Hacking the vault: {m._SafeMotor__current_speed}") 
```

-----

## 6\. ROS2 Context: "Node Privacy"

In ROS2 Python nodes:

  * **Private Members:** Variables like your publishers and subscribers should usually be treated as **Protected** (`self._publisher`) or **Private** (`self.__publisher`).
      * *Why?* You don't want another node accidentally deleting your publisher object.
  * **Public Members:** The functions you want others to call, or data you explicitly want to share.

-----

## 7\. Task: The "Bank Vault" ✅

**Scenario:**
You are creating a class for a Bank Account (or a Robot's Power Budget).

**Requirements:**

1.  Create a class `Account`.
2.  **Private Variable:** `self.__balance` (Initialize to 0.0 in `__init__`).
3.  **Public Method:** `def deposit(self, amount):`
      * *Logic:* If amount \> 0, add to balance. Else, print "Invalid amount".
4.  **Public Method:** `def withdraw(self, amount):`
      * *Logic:* If amount \<= balance, subtract and return the amount. Else, print "Insufficient funds" and return 0.

**The Logic Puzzle (Main):**

1.  Create an `Account` object.
2.  **Try to cheat:** Write `my_account.__balance = 1000000`.
3.  **Observe:**
      * Python will likely *let you write this line* without crashing, BUT...
      * It creates a **new** public variable named `__balance` instead of changing the real private one inside the class.
      * When you call `withdraw(50)`, check if the million dollars is actually there. (Spoiler: It won't be).
4.  **Fix:** Use `deposit(100)` and `withdraw(50)` to interact with the object legally.

*Goal: This proves that `__private` variables are hidden from the main scope.*
