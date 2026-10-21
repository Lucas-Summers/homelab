# Memos

Private notes at `https://notes.lucassummers.cc` via `envoy-internal` (LAN or WireGuard only). A single Memos replica stores its SQLite database and local attachments in `/var/opt/memos` on a 5 GiB Longhorn PVC. The `ACCESS` setting is pinned to private in `app/configmap.yaml`; changing it in the UI will not override the deployment-managed setting. Changes to this file take effect after restarting Memos.

After committing and pushing the manifests, check reconciliation and the pod:

```sh
flux -n default get kustomizations memos
kubectl -n default rollout status deployment/memos
kubectl -n default get pvc memos
kubectl -n default get httproute memos
```

Add a router DNS host entry for `notes.lucassummers.cc` pointing to the internal Envoy VIP `192.168.8.11` if your router provides LAN DNS (or use the cluster's internal DNS). Open the URL from the LAN or WireGuard and create the first account, which becomes the Memos host admin. Then check the admin settings and disable self-registration if enabled; private access controls anonymous reading, not account creation.

Longhorn's replicas help survive a node failure, but **they are not backups**. Arrange backups of the entire `/var/opt/memos` volume, including the SQLite database and local attachments, before keeping important notes. Keep Memos at one replica with SQLite, and back up before upgrading.
