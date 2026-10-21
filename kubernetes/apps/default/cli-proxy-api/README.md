# CLIProxyAPI for Open WebUI

This is an **unofficial** Codex OAuth bridge, not an OpenAI API entitlement from a ChatGPT subscription. Use it only for personal experiments; model access and authentication can change. The proxy is a ClusterIP service with an ingress policy allowing only Open WebUI pods. Its management API is disabled. The proxy client key is in a SOPS-encrypted Kubernetes Secret; OAuth tokens are created only by the login command and stay on the `cli-proxy-api` Longhorn PVC, not in Git or Open WebUI.

After committing and pushing the manifests, wait for Flux to apply them:

```sh
flux -n default get kustomizations cli-proxy-api open-webui
kubectl -n default rollout status deployment/cli-proxy-api
kubectl -n default rollout status deployment/open-webui
kubectl -n default get pvc cli-proxy-api
```

From your own terminal, start Codex device authorization (no ingress or port-forward required):

```sh
kubectl -n default exec -it deployment/cli-proxy-api -- /CLIProxyAPI/CLIProxyAPI --config /CLIProxyAPI/config/config.yaml --codex-device-login
```

Follow the instructions displayed **in your terminal** and approve the code in your own browser. Never paste a code, callback URL, token, or Secret here or into Git. This command writes credentials to `/root/.cli-proxy-api` on the Longhorn PVC; the running proxy should detect the new credential. If device authorization is unavailable for your account, stop here rather than exposing the proxy; the browser callback flow requires a separately planned localhost-only port-forward.

After login, add an OpenAI-compatible connection in Open WebUI at Admin → Settings → Connections. Use `http://cli-proxy-api.default.svc.cluster.local:8317/v1` and the proxy client key from the SOPS-encrypted Secret, **not** an OpenAI API key. To copy the key from your own terminal, run `kubectl -n default get secret cli-proxy-api-secret -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d; echo`. Do not paste the key into Git, logs, screenshots, or chat. Open WebUI stores connection settings in its database; its Deployment does not set OpenAI connection defaults. Refresh `https://chat.lucassummers.cc` and select one of the listed models.

The OAuth PVC has three Longhorn replicas, but replicas are not backups. Back up the credential directory and Open WebUI data off-cluster before relying on them. Keep Open WebUI accounts private: anyone allowed to chat through this connection can use your subscription quota.
