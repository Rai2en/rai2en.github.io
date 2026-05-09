# AGENTS.md - Rai2en Hugo Blowfish blog guide

This file is the operating guide for AI agents working in this repository. Keep it current whenever the blog structure, commands, navigation, deployment flow, or recurring pitfalls change.

## Repository identity

- Repository: `Rai2en/rai2en.github.io`
- Local working clone used by Hermes: `/tmp/rai2en-blog`
- Site: `https://rai2en.github.io/`
- Static site generator: Hugo Extended
- Theme: Blowfish, checked out as `themes/blowfish/`
- Deployment: GitHub Pages from the `main` branch via GitHub Actions
- Primary language: English content with French UI/page translations being added
- Communication with the owner: concise French status updates are preferred

## Mandatory context before editing

- This is a Hugo Blowfish site. Load the Hermes skill `hugo-blowfish-blog` before modifying content, layouts, theme config, navigation, builds, or deployment.
- Do not deploy, push, or run a final production build without asking the owner whether there are other additions or modifications to include first.
- Work locally first, verify locally, then summarize clearly.
- Never expose secrets, tokens, passwords, API keys, private emails beyond what is already public in the repository, or credentials. Redact any accidental secret as `[REDACTED]`.
- Avoid em dash characters in prose. Use a normal hyphen instead.

## Current site structure

Important source directories:

```text
config/_default/              Hugo and Blowfish config
content/                      Markdown content
content/about/                About page, with EN and FR variants
content/posts/                Blog posts as page bundles
content/portfolio/            Portfolio landing page, formerly Projects
content/resume/               Resume page
content/tags/                 Tags taxonomy landing page
content/series/               Series taxonomy landing page
content/categories/           Categories taxonomy landing page
content/topics.md             Unified EN hub for Tags and Series
content/topics.fr.md          Unified FR hub for Tags and Series
layouts/_default/             Site layout overrides
layouts/partials/             Site partial overrides
static/img/                   Static images such as portfolio hero assets
assets/css/                   Blowfish custom CSS and color schemes
themes/blowfish/              Theme submodule, avoid direct edits unless intentional
public/                       Generated site output, do not stage casually
resources/_gen/               Generated Hugo image cache, do not stage casually
```

## Core configuration files

- `config/_default/hugo.toml`
  - Theme, baseURL, taxonomies, outputs, sitemap.
  - Taxonomies currently include `tags`, `categories`, `authors`, and `series`.
- `config/_default/params.toml`
  - Blowfish params, color scheme, homepage, article/list behavior, featured posts.
  - Current color scheme: `raizen`.
  - Default appearance: dark.
  - Homepage layout: profile.
- `config/_default/languages.en.toml`
  - English site title, author, social links, description.
- `config/_default/languages.fr.toml`
  - French language config and localized description.
- `config/_default/menus.en.toml`
  - English main and footer navigation.
- `config/_default/menus.fr.toml`
  - French main and footer navigation.
- `config/_default/markup.toml`
  - Markdown and syntax highlighting configuration.
- `config/_default/module.toml`
  - Hugo module/theme settings.

## Current navigation model

Main navigation is intended to be:

English:

```text
Posts -> /posts/
Topics -> /topics/
Portfolio -> /portfolio/
About -> /about/
```

French:

```text
Articles -> /fr/posts/
Sujets -> /fr/topics/
Portfolio -> /fr/portfolio/
À propos -> /fr/about/
```

Footer navigation currently mirrors the important entry points:

```text
Topics/Sujets
Portfolio
Categories/Catégories
```

## Portfolio section

- The old Projects section has been renamed to Portfolio.
- Source folder: `content/portfolio/`
- Main page: `content/portfolio/index.md`
- French counterpart: `content/portfolio/index.fr.md`
- Custom layout: `layouts/_default/projects.html`
- The layout name remains `projects` for now, even though the user-facing section is Portfolio.
- Old URL compatibility is preserved through an alias from `/projects/` to `/portfolio/`.
- Hero image currently uses `static/img/projects-hero.png`. The image filename still contains `projects` for compatibility with the existing layout.
- The portfolio layout includes curated sections for selected projects, public repos/research, and HTB writeups.

When editing the portfolio:

- Preserve clickable project titles and concrete evidence links.
- Prefer French UX copy for portfolio CTAs and section headings unless the owner requests full English.
- Keep technical abbreviations like HTB, CVE, OSCP, OWASP unchanged.
- Good CTA labels include `Explorer les projets`, `Voir GitHub`, `Lire l'étude de cas`, `Ouvrir le repo`.

## Tags and Series model

Tags and Series are unified only in navigation, not technically merged.

Keep this intact:

```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  author = "authors"
  series = "series"
```

Current hub pages:

- `content/topics.md` -> `/topics/`
- `content/topics.fr.md` -> `/fr/topics/`

Current hub layout:

- `layouts/_default/taxonomy-hub.html`

The hub layout must show two distinct blocks:

- Tags, from `.Site.Taxonomies.tags`
- Series, from `.Site.Taxonomies.series`

Important Hugo template pitfall:

- Inside `range $name, $taxonomy := .Site.Taxonomies.series`, the dot changes to the taxonomy collection. Use root context like `$.Site.Language.Lang` for language checks.

Do not remove `/tags/` or `/series/`. The hub should link to the raw taxonomy pages for users who want them.

## Multilingual and translation behavior

The site has EN and FR language config.

Current language-related files:

```text
config/_default/languages.en.toml
config/_default/languages.fr.toml
config/_default/menus.en.toml
config/_default/menus.fr.toml
layouts/partials/translations.html
```

The site overrides Blowfish's default `translations.html` partial so the language selector appears whenever more than one site language exists, not only when the current page has a direct translation.

Expected language selector behavior:

- If a page has a direct translation via `translationKey`, link to that translated page.
- If no direct translation exists, fall back to the language home page.
- Show display labels like `EN` and `FR`.

Paired pages should use stable `translationKey` values. Current known keys:

```text
about
posts
portfolio
topics
```

Add lightweight localized versions for new major navigation pages so the language selector has useful targets.

## Content conventions

Posts live as Hugo page bundles:

```text
content/posts/<slug>/
  index.md
  cover.png
  img/
```

For new posts:

- Use `content/posts/<slug>/index.md`.
- Always include or generate `cover.png` if no PNG is provided.
- Preferred cover dimensions: `1280x640`.
- Use dark cyber/security visual direction for generated thumbnails.
- Common front matter fields:

```yaml
---
title: "Post Title"
date: 2026-01-01
draft: true
summary: "Short description for cards."
tags: ["tag"]
categories: ["Category"]
series: ["Series Name"]
showTableOfContents: true
tocPosition: right
---
```

Writing conventions:

- No em dash characters.
- Prefer clear, concrete cybersecurity language.
- Keep titles and Selected work entries clickable when they refer to repos, posts, or sections.
- Do not invent dates, employers, certifications, or claims. Use only repository content or verified public sources.
- When writing visible portfolio copy, avoid generic SaaS/marketing language. The site should read like a cybersecurity portfolio for recruiters: concrete, sober, natural, and oriented toward evidence of practical skills. Avoid formulations such as `polished hub`, `seamless experience`, `discover insights`, `clear readable interface`, `unlock`, `empower`, `showcase`, and `explore content`. Prefer sentences that clearly explain what the owner did, what the reader will find, and which skills the work demonstrates. For portfolio-facing pages, prefer French copy unless the owner explicitly asks for English.

## Local development commands

Preferred preview server:

```bash
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/ --disableFastRender --ignoreCache --renderToMemory
```

Use `--renderToMemory` so stale tracked `public/` output does not override source-rendered pages.

Clean local validation build without deploying:

```bash
rm -rf /tmp/rai2en-build-test
hugo --gc --ignoreCache --destination /tmp/rai2en-build-test
```

After any build or server run, clean generated output from the working tree:

```bash
git restore public resources 2>/dev/null || true
python3 - <<'PY'
import subprocess, os, shutil
raw = subprocess.check_output(['git','ls-files','-o','--exclude-standard','-z','--','public','resources'])
items = [x.decode() for x in raw.split(b'\0') if x]
for p in items:
    if os.path.isdir(p):
        shutil.rmtree(p, ignore_errors=True)
    else:
        try:
            os.remove(p)
        except FileNotFoundError:
            pass
print('removed_untracked_build_artifacts', len(items))
PY
```

Status check:

```bash
git status --short
git diff --name-status
```

## Verification checklist

For navigation or layout changes:

1. Run a local Hugo build to a temp destination.
2. Confirm expected HTML files exist in the temp destination.
3. Start or reuse a preview server with `--renderToMemory`.
4. Check important URLs with curl.
5. Use browser inspection or screenshots for visual changes.
6. Restore `public/` and `resources/` after validation.
7. Summarize changed source files only.

Current key URLs to verify after navigation changes:

```text
/
/posts/
/topics/
/portfolio/
/projects/              alias to /portfolio/
/about/
/fr/posts/
/fr/topics/
/fr/portfolio/
/fr/about/
/tags/
/series/
```

Quick curl probe:

```bash
for u in / /portfolio/ /projects/ /topics/ /fr/portfolio/ /fr/topics/; do
  printf '\n== %s ==\n' "$u"
  curl -s -o /tmp/curlpage -w '%{http_code} %{redirect_url}\n' "http://127.0.0.1:1313$u"
  grep -Eo '<title>[^<]+|Portfolio|Topics|Sujets|Tags|Series|FR|EN' /tmp/curlpage | head -20
done
```

Expected current local build counts after the Portfolio, Topics, and FR work:

```text
EN pages: about 145
FR pages: about 18
```

Counts may change as content grows, but a sudden large drop usually indicates a Hugo config or content date issue.

## Deployment discipline

Do not push or deploy automatically unless the owner explicitly asks.

Before final deploy:

1. Ask the owner whether there are other additions or modifications to include.
2. Run local verification.
3. Restore generated `public/` and `resources/` churn.
4. Stage source files only.
5. Commit and push.
6. Watch GitHub Actions.
7. Verify the live site contains the expected change.

Typical final sequence, only after approval:

```bash
hugo --gc --ignoreCache
git restore public resources 2>/dev/null || true
# remove untracked public/resources artifacts as shown above
git status --short
git add AGENTS.md README.md config content layouts assets static archetypes .github
git commit -m "Update blog navigation and localization"
git push
gh run list --repo Rai2en/rai2en.github.io --branch main --limit 5
gh run watch <run-id> --repo Rai2en/rai2en.github.io --exit-status
```

## Common pitfalls

- Hugo pages dated in the future may appear in `hugo list all` but not render if `buildFuture = false`.
- A leaf page like `content/topics.md` is safer for a custom standalone hub than an empty section bundle if no child pages exist.
- Running `hugo --gc`, even with `--destination /tmp/...`, can still modify `resources/_gen` in the working tree.
- `public/` and `resources/_gen/` are generated artifacts. Restore or clean them unless the owner explicitly wants generated output tracked.
- Do not edit files under `themes/blowfish/` for site-specific changes. Override in `layouts/`, `assets/`, or `config/` instead.
- If a preview looks stale, find and stop the exact old Hugo server PID, then relaunch with `--ignoreCache --renderToMemory`.
- Avoid broad `pkill -9`; inspect exact PIDs first.
- Commit messages containing `&` can be problematic in shell commands. Use `and` instead.

## Current uncommitted feature set to preserve

At the time this file was created, the working tree includes an uncommitted batch that should be preserved unless the owner asks to revert it:

- Projects renamed to Portfolio in navigation and content path.
- `/projects/` kept as alias to `/portfolio/`.
- Tags and Series merged into a single visible `Topics`/`Sujets` hub while taxonomies remain distinct.
- EN/FR language configuration and menus added.
- Language selector partial overridden for always-available language switching.
- Lightweight FR pages added for About, Posts, Portfolio, and Topics.
- README updated to reflect Portfolio and Topics.

If you make future structural changes, update this section or replace it with the new stable state after commit.
