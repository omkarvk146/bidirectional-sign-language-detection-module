# gitpush.ps1
param (
    [string]$message = "Auto-commit"
)

git add .
git commit -m "$message"
git push origin master
