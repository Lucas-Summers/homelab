# Pi-hole

Pi-hole is an opt-in ad-blocking DNS server at `192.168.8.14` (TCP and UDP port 53). Its web UI is available via the **internal** gateway at `https://dns.lucassummers.cc/admin/`. It does not replace CoreDNS, k8s-gateway, router DNS, or DHCP.

- Reserve `192.168.8.14` outside the router's DHCP pool before using it; the Cilium LoadBalancer IP must not collide with another LAN device.
- Pi-hole forwards uncached, unblocked queries to the router at `192.168.8.1`. This preserves the router's local host records. **Do not configure the router itself to forward DNS to Pi-hole**, or the two will create a DNS loop. Point individual devices directly to `192.168.8.14` to opt in.
- To retrieve the generated web password locally: `sops decrypt kubernetes/apps/network/pihole/app/secret.sops.yaml | yq -r '.stringData.FTLCONF_webserver_api_password'`. Do not commit or paste the decrypted value.
- Test with `dig @192.168.8.14 example.com` and `dig @192.168.8.14 docs.lucassummers.cc` before configuring devices. A secondary non-Pi-hole resolver on a client may bypass ad blocking.
- The Longhorn PVC retains configuration across pod restarts and node moves, but is not a backup.
