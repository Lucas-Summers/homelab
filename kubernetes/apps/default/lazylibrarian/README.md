# LazyLibrarian → qBittorrent → library

LazyLibrarian shares the `think2` media SSD with qBittorrent at `/data`. The ebook library is `/data/media/books`, the audiobook library is `/data/media/audiobooks`, and downloads are under `/data/torrents/books`. The deployment creates these folders only after verifying the media SSD is mounted. Its `/config` lives on a Longhorn PVC.

After Flux deploys it, complete setup in the web UIs (credentials and API keys stay in persistent app data, not Git):

1. Open `https://books.${SECRET_DOMAIN}/home` and configure authentication in **Settings → Web Interface** before sharing the address. Under the book/audiobook settings, set the ebook destination to `/data/media/books` and the audiobook library folder to `/data/media/audiobooks`. Leave new-author and new-audiobook statuses at **Skipped** until you choose what to monitor, to avoid requesting entire back catalogs.
2. In qBittorrent, create a `lazylibrarian` category with save path `/data/torrents/books`. In LazyLibrarian **Settings → Downloaders**, enable qBitTorrent with host `qbittorrent.default.svc.cluster.local`, port `8080`, the existing Web UI credentials, and label `lazylibrarian`. Set the downloader directory to `/data/torrents/books`. If you intend to keep seeding, enable **Keep seeding** and **Keep Original Files** so imports don't move the files qBittorrent is seeding.
3. In Prowlarr **Settings → Apps**, add **LazyLibrarian**. Use `http://lazylibrarian.default.svc.cluster.local:5299` as the LazyLibrarian server URL and `http://prowlarr.default.svc.cluster.local:9696` as the Prowlarr server URL _as seen by LazyLibrarian_. Find LazyLibrarian's API key under **Settings → Web Interface**. Test and save; select the relevant ebook and audiobook sync categories, then run **Sync App Indexers**. Prowlarr will configure eligible Newznab/Torznab providers in LazyLibrarian.
4. Add the two library paths to a reader/player of your choice (for example, Jellyfin's existing read-only media mount can see `/data/media/audiobooks`). No Jellyfin or audiobook player library is created automatically.

Both apps see the same `/data` paths, so no remote path mappings are needed. Only qBittorrent runs behind the VPN. LazyLibrarian manages both ebooks and audiobooks in this one instance; Seerr does not request books.
