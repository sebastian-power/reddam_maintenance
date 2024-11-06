# Requirement dotpoints from D'Souza
- anybody can register (Admin, Worker, Member)
- Have requirements for job
    - Can have jobs and sub-jobs
- Admin
    - Admin notified whenever there is new job requirement
    - Admin can login when they get notification and check what the new jobs are (must be highlighted)
    - Admin looks at job and can assign it to certain people and those people will receive an email about the job assigned to them, and they can view that new job
- Worker
    - Worker must add status to job (not started, in process, or done)
- Once job done, Admin confirms it is completed, and notification is sent to person who requested job to be done
- Report section for admin for status of all jobs (must be able to sort on various fields like dates and users)
# Utilise Linux
For web development, both Windows and Linux have their pros and cons, but **Linux is generally favoured** for several reasons:

1. **Server Environment Alignment**: Most web servers run Linux, so developing on Linux reduces compatibility issues when deploying the app. Testing locally in a similar environment to production can help prevent deployment surprises.
2. **Performance**: Linux tends to be more efficient with resources, which can be beneficial if you're running multiple services or working with heavier development stacks. This also helps if you’re working with virtual machines or containers.
3. **Package Management**: Linux's package managers (e.g., `apt`, `yum`, `dnf`) simplify installing, updating, and managing software packages, which is useful for quickly setting up a development environment with the necessary tools and libraries.
4. **Tooling and Scripting**: Many web development tools (especially open-source ones) are designed with Linux in mind, offering greater stability and functionality there. Bash scripting, for example, is very popular in web development and is native to Linux. While Windows has PowerShell and WSL (Windows Subsystem for Linux), it still lacks some of Linux's seamlessness.
5. **Containers and Virtualisation**: Tools like Docker are highly popular in web development for consistent environments, and they run natively on Linux. Docker support is better optimised on Linux, as it was initially designed for it. Running Docker on Windows often requires WSL2, which adds some overhead.
6. **Flexibility and Customisation**: Linux provides more control over system configurations, which can be useful for tailoring the environment to specific requirements.

That said, **Windows can still be suitable, particularly with WSL2**. This allows running a Linux distribution within Windows, bridging the gap for those who prefer Windows’ interface but need Linux's compatibility.

In summary, **Linux is generally the better choice for web development** due to compatibility, flexibility, and performance.