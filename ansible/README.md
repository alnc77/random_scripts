# Ansible – Install GitHub Actions Runner Controller (ARC)

This Ansible role installs **[GitHub Actions Runner Controller (ARC)](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/quickstart-for-actions-runner-controller)** on any server that already has access to a Kubernetes cluster (kubeconfig configured).

## What it does

1. Optionally installs `kubectl` (latest stable) if not present.
2. Optionally installs `helm` (configurable version) if not present.
3. Creates the `arc-systems` and `arc-runners` namespaces.
4. Deploys the **ARC controller** (`gha-runner-scale-set-controller`) via Helm OCI chart.
5. Creates a Kubernetes Secret containing your GitHub PAT.
6. Deploys a **runner scale set** (`gha-runner-scale-set`) via Helm OCI chart.
7. Verifies the controller deployment is healthy.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Ansible ≥ 2.14 | On the control machine |
| `kubernetes` Python package | Installed automatically by the playbook |
| A running Kubernetes cluster | Any CNCF-conformant cluster (EKS, AKS, GKE, k3s, kubeadm, …) |
| `kubeconfig` on the remote host | Must point to the target cluster |
| GitHub PAT | Scopes: `repo` + `workflow` (org runners) or `Actions: write` |

---

## Quick start

### 1. Clone / copy the `ansible/` directory to your machine

### 2. Edit `inventory.ini`

```ini
[k8s_hosts]
k8s-admin ansible_host=10.0.0.10 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_rsa
```

### 3. Create a vault file from the example

```bash
cp vault.yml.example vault.yml
# Fill in your real values, then encrypt:
ansible-vault encrypt vault.yml
```

### 4. Run the playbook

```bash
ansible-playbook -i inventory.ini install_arc.yml --ask-vault-pass
```

Or pass variables inline (not recommended for tokens):

```bash
ansible-playbook -i inventory.ini install_arc.yml \
  -e arc_github_config_url="https://github.com/my-org" \
  -e arc_github_token="ghp_xxxx" \
  -e arc_runner_scale_set_name="my-runners"
```

---

## Variables

All variables are defined in `roles/arc/defaults/main.yml` and can be overridden.

| Variable | Default | Description |
|---|---|---|
| `arc_github_config_url` | *(required)* | GitHub org or repo URL for runners |
| `arc_github_token` | *(required)* | GitHub PAT |
| `arc_controller_namespace` | `arc-systems` | Namespace for the ARC controller |
| `arc_runners_namespace` | `arc-runners` | Namespace for runner scale sets |
| `arc_runner_scale_set_name` | `arc-runner-set` | Name / label used in `runs-on:` |
| `arc_min_runners` | `0` | Minimum idle runner replicas |
| `arc_max_runners` | `5` | Maximum runner replicas |
| `arc_runner_image` | `""` | Custom runner container image |
| `arc_helm_version` | `v3.14.3` | Helm version to install |
| `arc_chart_version` | `""` | ARC chart version (empty = latest) |
| `arc_install_kubectl` | `true` | Install kubectl if missing |
| `arc_install_helm` | `true` | Install Helm if missing |

---

## Using the runners in a workflow

After a successful run, reference the runner scale set in any workflow:

```yaml
jobs:
  build:
    runs-on: arc-runner-set   # matches arc_runner_scale_set_name
    steps:
      - uses: actions/checkout@v4
      - run: echo "Running on ARC!"
```

---

## Directory structure

```
ansible/
├── install_arc.yml          # Main playbook
├── inventory.ini            # Inventory (edit this)
├── vault.yml.example        # Secret template (copy → vault.yml, then encrypt)
└── roles/
    └── arc/
        ├── defaults/
        │   └── main.yml     # Configurable defaults
        ├── vars/
        │   └── main.yml     # Internal chart repo references
        ├── tasks/
        │   ├── main.yml            # Orchestration
        │   ├── install_kubectl.yml # kubectl installer
        │   └── install_helm.yml    # Helm installer
        └── meta/
            └── main.yml     # Role metadata
```
