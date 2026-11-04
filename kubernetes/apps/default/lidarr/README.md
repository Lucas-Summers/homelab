# Lidarr → qBittorrent → Jellyfin

Lidarr and qBittorrent share the `think2` media SSD at `/data`. Lidarr's library root is `/data/media/music`; qBittorrent's music download directory is `/data/torrents/music`. Jellyfin mounts the same `/data/media/music` path read-only. These directories are prepared by the deployments only after the media SSD mount is verified.

After Flux deploys Lidarr, finish these settings in the applications' web UIs (their config and credentials live in persistent app data, not in Git):

1. At `https://lidarr.${SECRET_DOMAIN}`, complete Lidarr's first-run authentication setup. Under **Settings → Media Management**, add `/data/media/music` as the root folder. Enable **Use Hardlinks instead of Copy** under advanced settings if you want to keep seeding while importing without duplicating files. Download and library paths are on the same filesystem.
2. In qBittorrent, create a `lidarr` category with save path `/data/torrents/music`. In Lidarr **Settings → Download Clients**, add qBittorrent using host `qbittorrent.default.svc.cluster.local`, port `8080`, category `lidarr`, and the existing qBittorrent UI credentials. Do not put Lidarr itself behind the VPN: only qBittorrent uses Gluetun.
3. In Prowlarr **Settings → Apps**, add Lidarr at `http://lidarr.default.svc.cluster.local:8686` using Lidarr's API key from **Settings → General**; use `http://prowlarr.default.svc.cluster.local:9696` as the Prowlarr server URL if prompted. Sync the desired music indexers.
4. In Jellyfin **Dashboard → Libraries → Add Media Library**, choose **Music** and add folder `/data/media/music`. Imported music will then appear in Jellyfin after a library scan.

Do not configure remote path mappings: both apps see the same `/data` paths. No credentials or API keys are stored in the manifests. Until the UI steps are completed, Lidarr is deployed and the directories are ready, but downloads and Jellyfin's Music library are not automatically configured.
