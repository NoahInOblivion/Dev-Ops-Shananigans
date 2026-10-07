# Dev-Ops Shananigans

A hands-on DevOps learning lab built from small, inspectable exercises. The repository covers Linux operations, shell scripting, networking, Git/GitHub workflows, Docker images, Docker networking, and multi-stage builds.

The examples are intentionally small. You can read the source, run one command, inspect the result, and clean up without needing a cloud account or a large toolchain.

## Start here

| Area | What it contains | Guide |
|---|---|---|
| Docker | Six standalone Hello World containers plus a multi-stage Node.js app | [`Docker/README.md`](Docker/README.md) |
| Docker networking | Bridge networks, host networking, bind mounts, and an overlay-network exercise | [`Docker-Network/README.md`](Docker-Network/README.md) |
| DockerFiles | Earlier Dockerfile and image exercises | [`DockerFiles/README.md`](DockerFiles/README.md) |
| Linux fundamentals | Links, users, `journalctl`, and everyday commands | [`Linux-Fundamentals/README.md`](Linux-Fundamentals/README.md) |
| Networking | Interface, route, DHCP, DNS, and connectivity commands | [`Networking/README.md`](Networking/README.md) |
| Shell scripting | A Bash script that records host details and creates a process snapshot | [`Shell-Scripting/README.md`](Shell-Scripting/README.md) |
| Git/GitHub | Cherry-pick exercise evidence and mock files | [`Github/README.md`](Github/README.md) |
| Kubernetes fundamentals | Cluster setup and architecture | [`Kubernetes Fundamentals/README.md`](Kubernetes%20Fundamentals/README.md) |
| Kubernetes core objects | Pods, controllers, rollouts, and troubleshooting | [`Kubernetes Core Objects/README.md`](Kubernetes%20Core%20Objects/README.md) |
| Kubernetes services | Service types, DNS, and selectors | [`Kubernetes Services/README.md`](Kubernetes%20Services/README.md) |
| Kubernetes ingress | ConfigMaps, Secrets, Ingress, TLS, and full demo | [`Kubernetes Ingress/README.md`](Kubernetes%20Ingress/README.md) |
| Capstone project | TaskBoard DevSecOps application, CI/CD, Kubernetes, Helm, Terraform, and observability | [`Capstone project/README.md`](Capstone%20project/README.md) |

## Prerequisites

- Linux, macOS, or WSL for the shell and networking exercises.
- Bash for [`Shell-Scripting/script.sh`](Shell-Scripting/script.sh).
- Docker Engine or Docker Desktop for the Docker exercises.
- `curl` for HTTP checks.
- `ip`, `ping`, `dig`, `nmcli`, and `resolvectl` for the networking exercises. Some are installed by separate OS packages.
- `sudo` only for the Linux user-management examples.

## Suggested path

1. Run the Linux command examples in a disposable directory or virtual machine.
2. Run the shell script from a temporary directory and inspect the generated process snapshot.
3. Use the networking guide to identify the local interface, route, DHCP lease, and DNS configuration.
4. Build the standalone Docker images in [`Docker/`](Docker/).
5. Run the network and volume exercises in [`Docker-Network/`](Docker-Network/).
6. Compare the older examples in [`DockerFiles/`](DockerFiles/) with the newer Docker examples.

## Repository conventions

- Commands are written for copy-and-paste, but destructive commands are marked with cleanup or safety notes.
- Docker examples use one folder per image so each build context stays easy to inspect.
- Screenshots and captured output remain beside the exercise they document.
- The repository documents the current files; it does not pretend that a local exercise is a production platform.

## Safe practice

Run Docker cleanup commands only for the container and network names created by the exercise. Run the Linux account commands in a VM or disposable machine. Run the shell script in a temporary directory and use simple names such as `practice` and `processes.txt` when prompted.

## Contributing an exercise

Keep a new exercise self-contained:

1. Put its source and fixtures in a named directory.
2. Add a README with prerequisites, run commands, expected output, and cleanup.
3. Add one small verification command or script.
4. Link the directory from this file.
