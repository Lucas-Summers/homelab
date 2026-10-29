# Jellyfin on think2

The media library is on the existing USB SSD mounted by `talos/node/think2/40-media.yaml` at `/var/mnt/media`. A Git push does **not** apply Talos config. From the `talos/` directory, run `topf apply --nodes-filter '^think2$'` and confirm its diff. Then run `talosctl --talosconfig talosconfig -n 192.168.8.21 get volumestatus e-media` and `talosctl --talosconfig talosconfig -n 192.168.8.21 ls /var/mnt/media`. Confirm the volume is ready on the USB partition before pushing the Jellyfin manifests.

Jellyfin is pinned to `think2`, mounts the SSD read-only at `/data`, and only serves the internal gateway at `https://tv.lucassummers.cc`. Its startup init container checks that `/var/mnt/media` is a different filesystem from `/var/mnt` before creating:

- `/data/media/movies` and `/data/media/tv` — Jellyfin library folders.
- `/data/torrents/movies` and `/data/torrents/tv` — future download categories.

Set the movie and TV libraries to `/data/media/movies` and `/data/media/tv` in the Jellyfin setup wizard, and create the admin password immediately. Config is on a retained Longhorn PVC; cache/transcodes use ephemeral storage. The SSD is not replicated: back up both the library and the Longhorn config. If the SSD goes offline, the pod must not download media onto the system disk.

Later, use the same SSD root as a single `/data` mount for Radarr/Sonarr and the downloader, so imports can hardlink rather than copy across filesystems. Keep qBittorrent off until a VPN route and fail-closed behavior have been verified. For Jellyfin requests, use Seerr (supports Jellyfin) rather than older Overseerr releases.
