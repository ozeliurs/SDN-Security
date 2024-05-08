# SDN Security Tools Installation

## Connecting hosts to Tailscale

First make sure that `vars/tailscale.yaml` is properly configured with the correct `auth_key`.

Then run the following command to install and configure Tailscale on the target host:

```bash
ansible-playbook install_configure_tailscale.yaml -i inventory.ini
```

## Installing `mosh` for better SSH experience in Vietnam

Run the following command to install `mosh` on the target host:

```bash
ansible-playbook install_mosh.yaml -i inventory.ini
```

## Installing Mininet

Run the following command to install Mininet on the target host:

```bash
ansible-playbook install_mininet.yaml -i inventory.ini
```

## Installing DELTA

Run the following command to install DELTA on the target host:

```bash
ansible-playbook install_delta.yaml -i inventory.ini
```