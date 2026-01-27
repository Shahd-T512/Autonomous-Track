
# Git & GitHub: Collaborator Workflow (Part 3)

Now you are ready to contribute! This guide explains the daily cycle of a team member. The goal is to get the latest code, do your work safely, and upload it without breaking the project.

## 1. Getting the Project (First Time Only)

To start working, you need to download the repository to your machine.

1.  Go to the repository page on GitHub.
2.  Click the green **Code** button and copy the URL.
3.  Open your terminal and run:

```bash
git clone <PASTE_URL_HERE>

```

4. This creates a folder with the project name. Enter it:

```bash
cd <PROJECT_NAME>

```

---

## 2. The Daily Workflow (Repeat Every Task)

Whenever you start a new task (e.g., "Solving Task 1"), follow these strict steps:

### Step 1: Update Your Local Code (`git pull`)

**CRITICAL:** Before touching anything, always make sure you have the latest changes from your teammates.

```bash
git checkout main
git pull origin main

```

* `git checkout main`: Switches you to the main version.
* `git pull`: Downloads updates. **If you forget this, your upload might fail later.**

### Step 2: Create a Branch (`git checkout -b`)

**Never work directly on `main`.** Create a separate "copy" for your task. If you break this branch, the main code remains safe.

```bash
# Syntax: git checkout -b <branch_name>
git checkout -b feature/task1-ammar

```

* Now you are in a safe isolated mode.
* Go to your folder (e.g., `Team_Workspace/Ammar/`) and write your code.

### Step 3: Save Changes (Add & Commit)

Once you are done coding:

```bash
git add .
git commit -m "Finished Task 1 solution"

```

### Step 4: Upload Your Branch (`git push`)

Since you created a new branch, you need to push it to GitHub.

```bash
# Syntax: git push -u origin <branch_name>
git push -u origin feature/task1-ammar

```

---

## 3. What happens next? (The Pull Request)

After you push, go to the GitHub repository page in your browser.

1. You will see a yellow banner saying **"Compare & pull request"**.
2. Click it.
3. Write a title and description of what you did.
4. Click **Create Pull Request**.

**What is a Pull Request (PR)?**
It's a request to the Team Leader: *"I finished my work on this branch, please check it and merge it into the main folder."*

---

## Summary of Commands

| Situation | Command |
| --- | --- |
| **First time setup** | `git clone <url>` |
| **Start of day** | `git pull origin main` |
| **Start new task** | `git checkout -b <new_branch>` |
| **Switch branches** | `git checkout <branch_name>` |
| **Upload task** | `git push -u origin <branch_name>` |

---

*End of Part 3. Next: Handling Merge Conflicts (When things go wrong).*
