# Admins
1. Go to address of site, get instantly redirected to Log In page, unless have cookies, then be kept at homepage (which is step 4)
2. No account, so click on Sign Up link
3. Enter name, email, and password + make sign up request
4. Brings to admin dashboard (Like kanban board (pending, not started, in progress, done) and can sort by a bunch of fields) (will have to update tasks table in db), tab to manage users, colour coded lightly (high or low opacity, whichever is the more transparent one)
5. If click on task in pending, can assign it and change stuff
6. Setting for how long until tasks auto delete and can manually delete
# Workers
1. Go to address of site, get instantly redirected to Log In page, unless have cookies, then be kept at homepage (which is step 4)
2. No account, so click on Sign Up link
3. Enter name, email, and password + make sign up request
4. Brings to worker dashboard (Like admin, but with only the tasks assigned to them shown in not started, in progress, and done, and all tasks available shown in pending)
5. When click on task, can self-assign or upgrade status, and add notes when task made completed
# Members
1. Go to address of site, get instantly redirected to Log In page, unless have cookies, then be kept at homepage (which is step 4)
2. No account, so click on Sign Up link
3. Enter name, email, and password + make sign up request
4. Brings to user dashboard (kanban board with status for their tasks (including if pending) and can add tasks with button)


Development environment setup:
- MySQL terminal
- Project directory bash terminal
- VSCode

Order of doing:
1. Profile page functionality
    - Change name and email form
    - Email with link to change pwd
2. Dashboard functionality
TODO
- Fix task formatting (use icons for date, description, user, etc)
- Make max line number for title and description (1 or 2 for description, 3-4 for title)
- Maybe use italic or something else to differentiate between description font and date and requested by user, unless using icons does enough
3. Get james to install from instructions

Dashboard permissions:
Every user sees sections

Admin: Pending (click on task and assign), not started (drag), in progress (drag), done (drag and change autodelete)
Workers: Pending (click on task and self-assign), not started (drag own, see others), in progress (drag own, see others), done (drag own, see others)
Members: See all sections, highlight tasks made by them

Workers: Can't delete or edit tasks other than own, can only self-assign, can only change status of tasks being worked on by them
Members: Can't delete or edit tasks other than own, can't assign, can't change status

for this you only really need to change the renderTasks function for each page (have diff js script for diff pages with diff versions of the function)