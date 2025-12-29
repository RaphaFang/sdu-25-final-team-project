This short guide explains how to make your code available on GitHub and how to create a pull request.

First, go to the GitHub repository of the project you are working on.  Click on “Create branch”. GitHub will ask from which source branch the new branch should be created. 
In most cases, you should select the main branch. If you are unsure about this step, feel free to ask.

After the branch has been created, you need to connect your local workspace with the GitHub repository.
 On GitHub, copy the HTTPS URL of the repository.
Open your terminal and type:

git clone <repository-url>

This command downloads all files and folders from the repository to your local machine.

Next, navigate into the project folder and update the list of available branches by typing:

git fetch

To switch to your branch, type:

git checkout <branch-name>

You are now working on your own branch, so you do not have to worry about breaking the main branch.

After you have finished your changes, you need to add them to Git:

git add <file-name>

or, if you want to add all changed files:

git add .

Then create a commit with a short description of your changes:

git commit -m "Describe your changes"

When the commit is ready, push your changes to GitHub:

git push

Finally, go back to GitHub and click on “Create Pull Request”.
Select at least one other person to review your changes.
After that, click “Create Pull Request” to finalize it.
