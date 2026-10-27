# Uptime Kuma

Kuma is available on the LAN at `https://status.${SECRET_DOMAIN}`. Its SQLite data is on the `uptime-kuma` Longhorn PVC. AutoKuma syncs the checks in `app/monitors.yaml` into Kuma and keeps its mapping on the `autokuma` PVC.

## First-time setup

1. **Before pushing**, choose a password locally by editing the SOPS secret from the repository root:
    ```sh
    SOPS_AGE_KEY_FILE=age.key sops edit kubernetes/apps/default/uptime-kuma/app/secret.sops.yaml
    ```
    Replace `stringData.PASSWORD` with your chosen password. The encrypted file currently holds a random password, not one you know.
2. Push/reconcile Flux, visit `https://status.${SECRET_DOMAIN}`, and create Kuma's first admin account with username **`lucas`** and the **same password** from step 1. Kuma does not bootstrap its admin account via an environment variable.
3. AutoKuma will connect with that account and sync the monitors. If it does not, restart it with `kubectl -n default rollout restart deployment/autokuma` and check `kubectl -n default logs deployment/autokuma`.
4. In Kuma, configure a notification channel and attach it to the monitors if you want alerts. No email or external notification destination is assumed here.

Public HTTP monitors cover the website, blog, and Echo through Cloudflare. Private HTTP monitors use Kubernetes Services, so they test the applications rather than the internal gateway/TLS. The CLI Proxy API has a TCP check because it does not expose a public endpoint; this only checks that its port accepts connections. Pi-hole's check covers the web UI, not DNS queries. Router and Cloudflare's dashboard are not cluster-hosted services and are not monitored here. Edit `app/monitors.yaml` to change the checks; AutoKuma reconciles them after the ConfigMap update.

Kuma runs **inside** the cluster: if the whole cluster or your home internet connection is down, it cannot send alerts. Use an external uptime service for independent availability monitoring. Back up the Kuma PVC if you want to retain history, status pages, and notification settings.
