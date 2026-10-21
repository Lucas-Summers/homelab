# Forgejo

Private Git hosting at `https://git.lucassummers.cc` through `envoy-internal` (home LAN or WireGuard only). The web UI and Git over HTTPS use port 443; Git over SSH uses a TCP listener on the **internal Gateway only**, port 2222. Registration and the install wizard are disabled, and browsing requires a login.

The rootless image stores its configuration, SQLite database, repositories, and generated signing keys under `/var/lib/gitea` on a 10 GiB Longhorn PVC. The init container generates a unique `secret_key` there only on first boot; if the key is subsequently lost while the config remains, startup fails rather than silently rotating it.

After committing and pushing, wait for Flux and the Deployment:

```sh
flux -n default get kustomizations forgejo
kubectl -n default rollout status deployment/forgejo
kubectl -n default get pvc forgejo
kubectl -n network get gateway envoy-internal
kubectl -n default get tcproute forgejo-ssh
```

Create the first admin from **your own terminal**. Replace the example email with your address; a random temporary password is printed to your terminal only (do not paste it into Git or share it):

```sh
kubectl -n default exec deployment/forgejo -- forgejo admin user create --username admin --email you@example.com --admin --random-password --random-password-length 24 --must-change-password
```

Sign in and change the temporary password when prompted. Add your SSH public key in Forgejo's user settings, then test and clone from your LAN or WireGuard connection:

```sh
ssh -T -p 2222 git@git.lucassummers.cc
git clone ssh://git@git.lucassummers.cc:2222/admin/repository.git
```

Replace `admin/repository` with your actual account and repository. Verify the SSH host key on first connection rather than blindly accepting it. SSH is not tunneled through Cloudflare or accessible publicly. Alternatively, use the HTTPS clone URL and a personal access token for Git credentials (especially if using two-factor authentication). You can create more users as admin; public self-registration is disabled.

Longhorn's replicas tolerate a node failure but are **not backups**. The 10 GiB claim consumes roughly three times that on the NVMe cluster as it fills; monitor capacity and arrange off-cluster backups of the PVC (including config, database, keys and repos) before relying on Forgejo for important code. Upgrade Forgejo major versions deliberately, after a backup.
