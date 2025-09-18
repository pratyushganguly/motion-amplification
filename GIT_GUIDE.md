# Git & GitHub Quick Reference for Daily Use

This guide helps you manage your project with Git and GitHub in VS Code or the terminal. It includes daily commands, best practices, and tips for recovering from mistakes.

---

## 1. Initial Setup

### Initialize (First Time Only)
```bash
git init
```

### Add Remote (e.g., to connect to GitHub; do only once)
```bash
git remote add origin <your_repo_url>
# If you named it 'RealOrigin':
git remote add RealOrigin <your_repo_url>
```

---

## 2. Daily Workflow

### See Current Status
```bash
git status
# OR use the Source Control icon in VS Code to see unstaged/staged files.
```

### Add File(s) You Changed or Created
```bash
git add filename.py
# Add all changes at once:
git add .
```

### Make a Commit (Must do after adding)
```bash
git commit -m "Describe what you changed"
```

### Push Changes to GitHub
```bash
git push RealOrigin main
# Use 'main' or 'master', depending on your branch name.
```

> **Tip:** Always pull before you start work and push when you finish, or after completing a feature or bugfix.

---

## 3. When You Update or Add Files

1. Save your work in VS Code.
2. `git status` to see what's new/changed.
3. `git add <your_files>` or `git add .` for all files.
4. `git commit -m "brief message"`.
5. `git push RealOrigin main`.

**VS Code Alternative:**
- Use Source Control panel (Ctrl+Shift+G)
- Stage files with `+` button
- Enter commit message and press Ctrl+Enter
- Click "Push" or use ellipsis menu

---

## 4. Pulling Remote Changes (Stay Up to Date)

```bash
git pull RealOrigin main
```
> **Best Practice:** Do this every day before starting work, or if you work in a team, before making changes.

**VS Code Alternative:** Use "Pull" button in Source Control panel.

---

## 5. If You Mess Up (Recovery Commands)

### Undo Last Commit (If not pushed yet)
```bash
git reset --soft HEAD~1
```
- This puts changes back into staging; fix and re-commit.

### Undo Local Changes to a File (Before add/commit/push)
```bash
git checkout -- filename.py
# Or restore specific file:
git restore filename.py
```

### Undo Changes After Add, Before Commit
```bash
git reset filename.py
# Removes file from staging area.
```

### Roll Back to a Previous Commit (Danger: Erases history!)
```bash
git log --oneline
# Find the commit hash you want (e.g. abc1234)
git reset --hard abc1234
# WARNING: This permanently deletes commits after abc1234
```

### Create a New Branch from Previous Commit (Safer Option)
```bash
git checkout -b recovery-branch abc1234
# Work from this branch, then merge back when ready
```

> **Tip:** If unsure, create a backup branch before running destructive commands!

---

## 6. Branching (For Advanced Features)

### Create and Switch to New Branch
```bash
git checkout -b feature-branch-name
# Or newer syntax:
git switch -c feature-branch-name
```

### Switch Between Branches
```bash
git checkout main
git checkout feature-branch-name
```

### Merge Branch Back to Main
```bash
git checkout main
git merge feature-branch-name
```

### Delete Branch (After Merging)
```bash
git branch -d feature-branch-name
```

---

## 7. See Commit History

```bash
git log --oneline
# Shows all commits in one line each

git log --graph --oneline
# Shows branch structure visually

git log -n 5
# Shows last 5 commits
```

---

## 8. Create and Use a .gitignore File

Create a `.gitignore` file in your project root to ignore files/folders you don't want to send to GitHub:

```gitignore
# Virtual environments
venv/
env/
.venv/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment variables
.env
.env.local

# IDE files
.vscode/settings.json
.idea/

# OS files
.DS_Store
Thumbs.db

# Logs
*.log

# Data files (if large)
*.csv
*.json
data/
```

---

## 9. Recommended Best Practices

### Commit Messages
- **Good:** "Add video compression feature"
- **Good:** "Fix memory leak in processing loop"
- **Bad:** "updates", "fixes", "stuff"

### When to Commit
- After completing a feature
- After fixing a bug
- Before trying something risky
- At end of work session

### When to Push
- After each commit (for solo projects)
- After completing a feature
- Before switching computers
- At end of work day

### General Tips
- **Commit Often:** Save your changes frequently with clear messages
- **Pull Before Push:** Always synchronize before working and pushing
- **Never Commit Secrets:** Do NOT upload `.env` files, passwords, or API keys
- **Use VS Code Source Control Tab:** Beginner-friendly GUI for Git operations
- **Test Before Commit:** Make sure your code runs before committing

---

## 10. VS Code Git Integration

### Source Control Panel (Ctrl+Shift+G)
- **U** = Untracked (new files)
- **M** = Modified
- **A** = Added (staged)
- **D** = Deleted

### Useful VS Code Git Features
- Click `+` next to files to stage them
- Click `-` to discard changes
- Use diff view to see what changed
- Timeline view shows file history
- Built-in merge conflict resolution

---

## 11. Common Error Messages & Solutions

### "fatal: remote origin already exists"
```bash
git remote rm origin
git remote add origin <your_repo_url>
```

### "Your branch is ahead of 'origin/main' by X commits"
```bash
git push RealOrigin main
```

### "Your branch is behind 'origin/main'"
```bash
git pull RealOrigin main
```

### "Please commit your changes or stash them"
```bash
# Option 1: Commit changes
git add .
git commit -m "Work in progress"

# Option 2: Stash changes temporarily
git stash
# Do your pull/checkout, then:
git stash pop
```

### "Merge conflict"
1. Open conflicted files in VS Code
2. Choose which changes to keep using VS Code's interface
3. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Save files
5. `git add .` and `git commit -m "Resolve merge conflict"`

---

## 12. Emergency Recovery

### If You Accidentally Deleted Important Code
```bash
# Check if it was committed:
git log --oneline
git show <commit-hash>

# If committed, recover from that commit:
git checkout <commit-hash> -- filename.py
```

### If You Want to Start Over from GitHub
```bash
# Save current work first!
git stash

# Reset to match GitHub exactly:
git fetch RealOrigin
git reset --hard RealOrigin/main

# Get your stashed changes back if needed:
git stash pop
```

---

## 13. Getting Help

### Git Help Commands
```bash
git help <command>
# Example: git help commit
git <command> --help
```

### Useful Resources
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- VS Code Git documentation (Help > Documentation)

---

**Keep this file in your project (`GIT_GUIDE.md`) and update as you learn!**

---

## Quick Command Cheat Sheet

| Task | Command |
|------|---------|
| Check status | `git status` |
| Add all files | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push RealOrigin main` |
| Pull | `git pull RealOrigin main` |
| See history | `git log --oneline` |
| Undo last commit | `git reset --soft HEAD~1` |
| Discard file changes | `git restore filename.py` |
| Create branch | `git checkout -b branch-name` |
| Switch branch | `git checkout branch-name` |

Happy coding! 🚀
