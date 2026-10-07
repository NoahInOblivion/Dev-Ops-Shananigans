# Bash host-inspection script

[`script.sh`](script.sh) is a small interactive Bash exercise. It prints host details, shows disk usage, asks for a directory and file name, writes a process listing into that file, and reports what it created.

## What the script does

1. Reads the current date with `date`.
2. Reads the hostname with `hostname`.
3. Reads the current user with `whoami`.
4. Prints `df -h` output.
5. Prompts for a directory name and a file name.
6. Creates the directory and file in the current working directory.
7. Writes `ps aux` output into the new file.

The script does not create a service, modify system configuration, or need `sudo`.

## Run safely

Run it from a temporary directory so its generated files do not mix with the repository:

```bash
script="$(pwd)/Shell-Scripting/script.sh"
workdir="$(mktemp -d)"
cd "$workdir"
bash "$script"
```

When prompted, use simple names such as:

- directory: `practice`
- file: `processes.txt`

Inspect the result:

```bash
find "$workdir" -maxdepth 2 -type f -print
sed -n '1,10p' "$workdir/practice/processes.txt"
```

Remove the temporary directory after checking it:

```bash
rm -rf "$workdir"
```

Only remove the path stored in `workdir`. The script accepts raw input for names, so avoid slashes, shell metacharacters, and paths that point outside the temporary directory.

## Captured output

![script.sh example run](image.png)

[`image.png`](image.png) records an example run. [`demo/demo`](demo/demo) contains a captured process listing from an earlier run; it is reference output, not an executable test.

## What this teaches

The exercise combines command substitution, variables, `read`, quoted paths, directory creation, redirection, and basic process inspection. It is intentionally small enough to trace line by line.
