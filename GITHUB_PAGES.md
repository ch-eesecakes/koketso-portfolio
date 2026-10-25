# Publish on GitHub Pages

The website is configured for GitHub Pages, with direct email, phone, Instagram and TikTok links. The enquiry form is paused. No Google Apps Script, Render account, email password or Node server is required for this version.

## Initial setup

1. Create an empty **public** GitHub repository named `koketso-portfolio` (GitHub Free supports Pages for public repositories).
2. Upload the contents of the prepared GitHub ZIP into the repository root. Extract it first; do not upload the ZIP as a single file. Include the hidden `.github` folder because it contains the publishing workflow.
3. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
4. Open **Actions → Publish portfolio to GitHub Pages → Run workflow**, select `main` and run it. Subsequent pushes to `main` publish automatically.
5. When deployment succeeds, use the link shown in **Settings → Pages**. The usual address is `https://YOUR-USERNAME.github.io/koketso-portfolio/`.

The repository root must contain `build_template.py`, `site/`, `dist/` and `.github/`; do not put these inside another `koketso-portfolio` folder. The workflow publishes **only `dist/`**.

## Privacy

Do not upload `.env`, `.git/`, `.venv/`, app passwords or private tokens. The prepared ZIP contains none of them. Original photographs stay in the local workspace; the published website uses optimised copies.

## Future changes

Edit `content.json`, the section HTML files or `site/` locally, then run `python3 build_template.py --static-hosting` and `python3 check_site.py`. Push the changed source and generated assets. Relative asset links support GitHub's repository subdirectory.

The local backend and Google mail setup are separate future work. They are not required to launch this static portfolio.

Official guide: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
