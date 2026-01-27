
# Git & GitHub: Handling Merge Conflicts (Part 4)

Sooner or later, you will see a message saying **"Merge Conflict"**. Don't panic! It doesn't mean you broke the code. It just means Git is confused and needs a human to decide.

## 1. What is a Conflict?

Imagine this scenario:
1.  **Ammar** edits line 10 of `main.cpp` to say: `int x = 5;`
2.  **Ahmed** edits line 10 of `main.cpp` to say: `int x = 10;`
3.  Both try to push to the same branch.

Git cannot know which number is correct (5 or 10?). It stops and asks: *"Hey, you two changed the same line. Which one should I keep?"*

---

## 2. How to Spot a Conflict

When a conflict happens (usually after `git pull` or `git merge`), Git will modify your file and add **markers** to show the problem.

Open the file in VS Code, and look for something like this:

```cpp
<<<<<<< HEAD
int x = 5;  // (This is your local change)
=======
int x = 10; // (This is the change coming from the server/teammate)
>>>>>>> origin/main

```

* **`<<<<<<< HEAD`**: Starts your changes.
* **`=======`**: Separates the two conflicting versions.
* **`>>>>>>> origin/main`**: Ends the incoming changes.

---

## 3. How to Fix It (Step-by-Step)

### Step 1: Open the File

Open the file with the conflict in your code editor (VS Code is highly recommended here).

### Step 2: Choose the Winner

VS Code often gives you clickable buttons above the conflict:

* **Accept Current Change:** Keep your code.
* **Accept Incoming Change:** Keep the other person's code.
* **Accept Both Changes:** Keep both lines.

**Or do it manually:** Delete the markers (`<<<<`, `====`, `>>>>`) and the code you don't want, leaving only the correct code.

### Step 3: Save and Commit

Once the file looks clean (no weird symbols):

1. Save the file.
2. Tell Git you fixed it:
```bash
git add .

```


3. Commit the fix:
```bash
git commit -m "Resolved merge conflict in main.cpp"

```


4. Push your work:
```bash
git push

```



---

## 4. How to Avoid Conflicts?

1. **Pull Often:** Run `git pull origin main` before you start working every day.
2. **Stick to Your Folder:** As long as you work in `Team_Workspace/Your_Name`, conflicts are very rare.
3. **Communicate:** If you need to edit a shared file (like `README.md`), tell the team on the group chat.

---

*End of the Mini-Course. You are now Git-Ready! 🚀*
