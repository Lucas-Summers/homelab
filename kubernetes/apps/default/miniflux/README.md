# Miniflux

Miniflux is available privately at `https://feed.lucassummers.cc` behind the internal Envoy gateway. PostgreSQL data is stored on a Longhorn volume. Add `feed.lucassummers.cc` to the router's local DNS hosts pointing at `192.168.8.11` if needed.

The initial username is `lucas`. Retrieve the generated password locally from the encrypted secret:

```sh
sops decrypt kubernetes/apps/default/miniflux/app/secret.sops.yaml | yq -r '.stringData.ADMIN_PASSWORD'
```

Change the admin password in Miniflux after your first login. The `CREATE_ADMIN` setting only creates the account if it does not already exist; changing the generated password in Git will not reset an existing account. The PostgreSQL password is set when the database is first initialized, so do not rotate the database Secret without also updating the database role. Back up PostgreSQL separately; Longhorn replicas are not backups.
