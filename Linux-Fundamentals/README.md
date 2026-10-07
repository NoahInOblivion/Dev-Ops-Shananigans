# Linux fundamentals

This directory is a compact practice guide for links, user creation, systemd journal inspection, and everyday command-line work. Run the examples in a test directory, virtual machine, or disposable account.

Commands beginning with `sudo` need administrator access. Read a command's manual before using it on a machine that matters.

## 1. Soft links and hard links

A symbolic link stores a pathname. It can point to a directory and cross filesystems, but it breaks when its target path disappears:

```bash
echo "hello Linux" > original.txt
ln -s original.txt soft-link.txt
cat soft-link.txt
ls -l original.txt soft-link.txt
rm soft-link.txt

![Soft link done in terminal](ss/image1.png)
```

A hard link is another directory entry for the same inode. Removing one name leaves the data available through the other name:

```bash
echo "hello Linux" > original.txt
ln original.txt hard-link.txt
ls -li original.txt hard-link.txt
rm original.txt
cat hard-link.txt
rm hard-link.txt

![Hard link done in terminal](ss/image2.png)
![Soft link failing due to deletion](ss/image3.png)
```

| Type | Points to | Usually crosses filesystems? | Can target a directory? |
|---|---|---:|---:|
| Symbolic link | A pathname | Yes | Yes |
| Hard link | The same inode/data | No | No |

Interview answer: a symbolic link points to a path and can break; a hard link points to the same inode and survives removal of the original name.

## 2. `adduser` and `useradd`

Both create users, but they serve different workflows:

| Command | Role | Typical use |
|---|---|---|
| `adduser` | Interactive distribution wrapper | Creating a normal user on Ubuntu/Debian |
| `useradd` | Low-level account utility | Scripts and precise account setup |

Create and remove a disposable practice account:

![User added in terminal](ss/image4.png)
```

Check the target account and home directory before removing anything on a real system.

## 3. `journalctl`

`journalctl` reads logs collected by `systemd-journald`. These commands cover the common inspection patterns:

![Checked in terminal](ss/image5.png)
```

The SSH unit may be named differently on another distribution. List service units when needed:

```bash
systemctl list-units --type=service
```

Press `q` to leave the normal log view and `Ctrl+C` to stop a live view.

## 4. Command reference

| Command | Purpose | Example |
|---|---|---|
| `pwd` | Show the current directory | `pwd` |
| `ls` | List files | `ls -la` |
| `cd` | Change directory | `cd /var/log` |
| `mkdir` | Create a directory | `mkdir practice` |
| `touch` | Create an empty file | `touch notes.txt` |
| `cp` | Copy files | `cp notes.txt backup.txt` |
| `mv` | Move or rename files | `mv backup.txt old-notes.txt` |
| `rm` | Delete files | `rm old-notes.txt` |
| `cat` | Print file contents | `cat notes.txt` |
| `less` | Read a file by screen | `less /var/log/syslog` |
| `grep` | Search text | `grep error app.log` |
| `find` | Find files | `find . -name '*.log'` |
| `man` | Open a manual | `man journalctl` |
| `whoami` | Show the current user | `whoami` |
| `id` | Show user and group IDs | `id` |
| `chmod` | Change permissions | `chmod 600 secret.txt` |
| `df` | Show free disk space | `df -h` |
| `du` | Show directory size | `du -sh .` |
| `ps` | Show running processes | `ps aux` |
| `systemctl` | Manage systemd services | `systemctl status ssh` |

Be especially careful with `rm` and commands run with `sudo`.
