# AMAS_project_2026
# Git Workflow for ERGM Study Project

# 1. Clone the repo
git clone <repo_url>
cd ergm-study-group

# 2. Create a branch for your work
git checkout -b feature/your-name

# 3. Work locally
# - Edit notebooks in notebooks/
# - Add functions in src/ergm_utils/
# - Keep raw data local or in data/raw/ if small

# 4. Commit changes
git add .
git commit -m "Short description of changes"

# 5. Update branch before pushing
git checkout main
git pull origin main
git checkout feature/your-name
git rebase main

# 6. Push branch and open a Pull Request (PR)
git push origin feature/your-name
# - Open PR on GitHub
# - Merge after review

# 7. Keep main clean: only merge tested/reviewed changes
