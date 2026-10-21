# Linkding

A private bookmark manager at `https://links.lucassummers.cc` via `envoy-internal` only. The standard image uses SQLite and stores its database under `/etc/linkding/data` on a single-pod Longhorn PVC. No initial account or password is baked into the deployment.

After committing and pushing, wait for Flux and the Deployment:

```sh
flux -n default get kustomizations linkding
kubectl -n default rollout status deployment/linkding
kubectl -n default get pvc linkding
```

Create the initial administrator from your own terminal (the command prompts for email and a password; do not put the password in a command or Git):

```sh
kubectl -n default exec -it deployment/linkding -- python manage.py createsuperuser --username admin
```

Then sign in at `https://links.lucassummers.cc`. The hostname only resolves internally (home LAN or WireGuard). The standard image does not include local HTML archiving; use a `-plus` image if you later decide you need it. Linkding blocks fetching metadata from private-network bookmark URLs by default as an SSRF precaution. Longhorn replicas cover a node failure but **are not backups**; arrange off-cluster backups of the database and assets before relying on it.
