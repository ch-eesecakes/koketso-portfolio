# Publish on GitHub Pages

The website is configured for GitHub Pages, with an enquiry form and direct email, phone, Instagram and TikTok links. The form uses Web3Forms once its access key is configured. No Google Apps Script, Render account, email password or Node server is required for this version.

## Initial setup

1. Create an empty **public** GitHub repository named `koketso-portfolio` (GitHub Free supports Pages for public repositories).
2. Upload the contents of the prepared GitHub ZIP into the repository root. Extract it first; do not upload the ZIP as a single file. Include the hidden `.github` folder because it contains the publishing workflow.
3. Open **Settings → Pages** and set **Source** to **GitHub Actions**.
4. Open **Actions → Publish portfolio to GitHub Pages → Run workflow**, select `main` and run it. Subsequent pushes to `main` publish automatically.
5. When deployment succeeds, use the link shown in **Settings → Pages**. The usual address is `https://YOUR-USERNAME.github.io/koketso-portfolio/`.

The repository root must contain `build_template.py`, `site/`, `dist/` and `.github/`; do not put these inside another `koketso-portfolio` folder. The workflow publishes **only `dist/`**.

## Fix `Get Pages site failed` / `Not Found`

If `actions/configure-pages@v5` fails with this error, check the repository's Pages configuration:

1. Open [this repository's Pages settings](https://github.com/ch-eesecakes/koketso-portfolio/settings/pages) using an account with repository admin or maintainer access.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**. Wait for the setting to save.
3. Open [the publishing workflow](https://github.com/ch-eesecakes/koketso-portfolio/actions/workflows/pages.yml), select the failed run and choose **Re-run all jobs**. Alternatively, choose **Run workflow** on `main`.
4. After the run succeeds, open `https://ch-eesecakes.github.io/koketso-portfolio/`.

If Pages is unavailable, check the repository visibility and account plan: GitHub Free supports Pages in public repositories. If you cannot change the source, ask a repository administrator to configure it.

The workflow already grants `pages: write` and `id-token: write`. Adding `enablement: true` alone is not a fix: automatic enablement requires a separate token with suitable permissions, rather than the default `GITHUB_TOKEN`. Selecting the source in Settings avoids needing that extra secret. See the [configure-pages input definitions](https://github.com/actions/configure-pages/blob/v5/action.yml).

## Connect the enquiry form

1. Request a [Web3Forms access key](https://web3forms.com/#start) using the email address that should receive enquiries, and complete its email verification.
2. In `contact.html`, paste the key into the `value` of the hidden input named `access_key`. This is a public form key intended for browser use, not an email password or private API token.
3. Change `contact-form-note` to `Send an enquiry directly from this website.`
4. Run `python3 build_template.py --static-hosting` and `python3 check_site.py`, then push the changes to `main`.
5. After deployment, send a test enquiry and confirm that it reaches the intended inbox.

Until a key is configured, the form remains visible and directs visitors to email or call. Failed submissions keep the visitor's message so they can retry. Successful submissions clear the form and show a confirmation. JavaScript is required for the inline submission experience.

## Privacy

Do not upload `.env`, `.git/`, `.venv/`, app passwords or private tokens. The prepared ZIP contains none of them. Original photographs stay in the local workspace; the published website uses optimised copies.

## Future changes

Edit `content.json`, the section HTML files or `site/` locally, then run `python3 build_template.py --static-hosting` and `python3 check_site.py`. Push the changed source and generated assets. Relative asset links support GitHub's repository subdirectory.

The local backend and Google mail setup are separate future work. They are not required to launch this static portfolio.

Official guide: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
