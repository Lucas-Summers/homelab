# Headlamp

Headlamp is available at `https://cluster.${SECRET_DOMAIN}` through the internal gateway (WireGuard/LAN). Sign in with a Kubernetes bearer token; access to the UI is limited to the permissions of that token. The chart's default Headlamp service account has `cluster-admin` privileges.

After Headlamp is deployed, generate a short-lived login token from a machine with `kubectl` access to the cluster:

```sh
kubectl -n kube-system create token headlamp --duration=1h
```

Paste the token into Headlamp's login screen. Treat it as an admin credential; do not commit or share it. The previous HTTP Basic Auth policy is no longer used. Once the policy is removed from the cluster, the old password Secret can also be removed with `kubectl -n kube-system delete secret headlamp-basic-auth`.
