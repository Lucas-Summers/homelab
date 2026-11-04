# Headlamp password

Headlamp is available at `https://cluster.${SECRET_DOMAIN}` over the internal gateway (WireGuard/LAN). Its Envoy Gateway `SecurityPolicy` requires HTTP Basic authentication; Headlamp then uses its own `cluster-admin` service account, so anyone who knows the password has full control of the cluster.

**Before syncing/deploying this app**, create the password Secret in `kube-system`. Envoy Gateway requires an htpasswd-style SHA hash stored under the `.htpasswd` key (not the `auth` key used by NGINX). Run this from a machine with `kubectl` access to the cluster; it prompts for your chosen password without putting it on the command line or in Git:

```sh
python3 - <<'PY'
import base64
import getpass
import hashlib
import json
import subprocess

password = getpass.getpass("Headlamp password: ")
if len(password) < 16 or password != getpass.getpass("Confirm password: "):
    raise SystemExit("Passwords must match and be at least 16 characters")
digest = base64.b64encode(hashlib.sha1(password.encode()).digest()).decode()
secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {"name": "headlamp-basic-auth", "namespace": "kube-system"},
    "type": "Opaque",
    "stringData": {".htpasswd": f"lucas:{{SHA}}{digest}\n"},
}
subprocess.run(["kubectl", "apply", "-f", "-"], input=json.dumps(secret), text=True, check=True)
PY
```

After Flux reconciles Headlamp, visit the URL and sign in as `lucas` with that password. No Kubernetes token is needed in the browser. To rotate the password, rerun the command. To check that the route is protected, visit it without credentials: it should respond with HTTP 401, **not** load Headlamp.

This Secret is created outside GitOps: back up the password and recreate the Secret before restoring this app on a new cluster. Never put the plaintext password or `.htpasswd` file in Git. Cluster admins can still access the Headlamp pod through Kubernetes; the gateway password protects only the web route.
