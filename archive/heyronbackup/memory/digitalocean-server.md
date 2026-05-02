# DigitalOcean Server Access

## Server Details
- **Hostname:** ubuntu-s-1vcpu-1gb-nyc1
- **IP:** 172.17.0.1 (Docker gateway) / accessible externally
- **User:** root

## OpenClaw Container
- **Container ID:** e06d57db9e41
- **Image:** ghcr.io/openclaw/openclaw:2026.4.19-beta.2-slim
- **Status:** Running (healthy)
- **Ports:** 0.0.0.0:18789->18789/tcp

## SSH Access
- **SSH Service:** Running on 172.17.0.1:22 (host)
- **SSH Key Pair:**
  - Public: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPtl/brc4VeWNnhqqzlRGY+RR8asjYsPdH9kMZyK3+Q/ openclaw@heyron`
  - Private key stored at: `/home/openclaw/.openclaw/credentials/ssh/id_ed25519`
- **Authorized_keys location:** `/root/.ssh/authorized_keys` on host

## How to SSH from Container
Once SSH client is available in container:
```bash
ssh -i /home/openclaw/.openclaw/credentials/ssh/id_ed25519 root@172.17.0.1
```

## Notes
- SSH client was installed via: `docker exec -u root -it e06d57db9e41 apt-get install -y openssh-client`
- The private key was generated on the host and shared with the container
- This gives full root access to the DigitalOcean VPS

*Updated: 2026-04-22*