# BLACKTRACE // ZERO-DAY — Web Edition

A cinematic, harmless hacker-console prank that runs entirely in a web browser.

## Live GitHub Pages URL

After enabling GitHub Pages with the included GitHub Actions workflow, the site will be available at:

`https://aksadio.github.io/BLACKTRACE/`

## Deploy with GitHub Pages

1. Push this folder to the `Aksadio/BLACKTRACE` repository.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, choose **GitHub Actions**.
4. The included workflow `.github/workflows/pages.yml` will deploy `index.html` automatically.
5. Open the URL above after the workflow finishes.

## Local test

No server or package installation is required. Open `index.html` in a modern browser.

For best results, use a small local server from this folder:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Safety

This is a visual simulation. It does not scan networks, execute shell commands, access files, collect passwords, change system settings, or contact external servers. All network nodes, IP addresses, IDs, and terminal output are fictional and generated locally in the browser.
