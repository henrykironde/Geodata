

**Shell** is an interface between a user and OS to access to an operating system's services. It can be either `GUI` or `CLI` (Command Line interface).
This is where the sys in and sys out componets inteface.(it is a file)

**sh (Bourne shell)** is a shell command-line interpreter,
for Unix/Unix-like operating systems. It provides some built-in commands.
In scripting language we denote interpreter as `#!/bin/sh`.

It was one most widely supported by other shells like bash (free/open), kash (not free).

**Bash (Bourne again shell)** is a shell replacement for the Bourne shell.
Bash is superset of sh. Bash supports sh. 
POSIX is a set of standards defining how POSIX-compliant systems should work. 
Bash is not actually a POSIX compliant shell. 
In a scripting language we denote the interpreter as #!/bin/bash


**Analogy:**

**Shell** is like an interface or specifications or API.

**sh** is a class that implements the Shell interface.

**Bash** is a subclass of the sh or inherites sh.


Profile files
=============
**.bashrc**, **.bash_profile**, **.bash_login**, **.profile**, **.Rprofile**, **.environ file**

+----------------+-----------+-----------+-----------------+-----------+------+
|                |Interactive|Interactive|Non-interactive  |           |      |
|                |login      |non-login  |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|/etc/profile    |   A       |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|/etc/bash.bashrc|           |    A      |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|~/.bashrc       |           |    B      |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|~/.bash_profile |   B1      |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|~/.bash_login   |   B2      |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|~/.profile      |   B3      |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|BASH_ENV        |           |           |  A              |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|                |           |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|                |           |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+
|~/.bash_logout  |    C      |           |                 |           |      |      
+----------------+-----------+-----------+-----------------+-----------+------+



