# Raizen | Blog

> Personal cybersecurity portfolio and technical blog focused on offensive security, vulnerability research, CTF writeups, and practical security labs.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-deployed-00f5d2?style=for-the-badge&logo=github)](https://rai2en.github.io/)
[![Hugo](https://img.shields.io/badge/Hugo-0.123.0-ff4088?style=for-the-badge&logo=hugo)](https://gohugo.io/)
[![Blowfish](https://img.shields.io/badge/Theme-Blowfish-7c3aed?style=for-the-badge)](https://blowfish.page/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

## Overview

This repository powers [rai2en.github.io](https://rai2en.github.io/), a static website built with Hugo and the Blowfish theme. It serves as a public portfolio for cybersecurity research, technical writeups, lab projects, and practical notes.

The site is designed to document real learning paths and hands-on security work, including Hack The Box machines, CVE analysis, offensive security tooling, Active Directory labs, web application testing, and defensive hardening projects.

## Live site

Production URL:

```text
https://rai2en.github.io/
```

## Content focus

The blog is organized around several technical tracks:

- HTB writeups - attack chains, enumeration, exploitation, privilege escalation, and lessons learned.
- CVE deep dives - vulnerability analysis, exploitation context, mitigations, and defensive guidance.
- CyberLabs - portfolio-grade security projects based on realistic lab environments.
- Tools and techniques - practical notes on offensive security tooling, recon, network analysis, and methodology.
- Professional portfolio pages - selected work, resume, contact information, and project summaries.

## Featured sections

- Posts: https://rai2en.github.io/posts/
- Projects: https://rai2en.github.io/projects/
- Series: https://rai2en.github.io/series/
- Tags: https://rai2en.github.io/tags/
- About: https://rai2en.github.io/about/

## Technology stack

| Area | Technology |
| --- | --- |
| Static site generator | [Hugo Extended](https://gohugo.io/) |
| Theme | [Blowfish](https://blowfish.page/) |
| Styling | Custom CSS, dark cyberpunk theme, responsive cards |
| Search | Hugo JSON output and Blowfish search integration |
| Deployment | GitHub Actions and GitHub Pages |
| Content format | Markdown with Hugo front matter |

## Repository structure

```text
.
├── assets/                 # Custom CSS, images, logo, favicon, and theme overrides
├── config/_default/        # Hugo and Blowfish configuration files
├── content/                # Site content: posts, pages, series, tags, projects
│   ├── about/              # About page
│   ├── posts/              # Technical articles and writeups
│   ├── projects/           # Portfolio project index
│   ├── resume/             # Resume page
│   └── series/             # Series landing pages
├── layouts/                # Optional Hugo layout overrides
├── static/                 # Static files served as-is
├── themes/blowfish/        # Blowfish theme
├── .github/workflows/      # GitHub Pages build and deployment workflow
└── README.md
```

## Local development

### Prerequisites

- Hugo Extended `0.123.0` or compatible
- Git
- Dart Sass, if you are working on theme styles

### Run locally

```bash
git clone --recurse-submodules https://github.com/Rai2en/rai2en.github.io.git
cd rai2en.github.io
hugo server -D --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/ --disableFastRender
```

Then open:

```text
http://127.0.0.1:1313/
```

### Clean build

```bash
rm -rf resources/_gen public .hugo_build.lock
hugo --gc --ignoreCache
```

### Production build

```bash
hugo --gc --minify
```

## Deployment

Deployment is handled by GitHub Actions through `.github/workflows/gh-pages.yml`.

The workflow runs on:

- Pushes to `main`
- Manual `workflow_dispatch` runs from the GitHub Actions tab

Pipeline steps:

1. Install Hugo Extended
2. Install Dart Sass
3. Checkout repository with submodules
4. Build the site with Hugo
5. Upload the generated `public/` artifact
6. Deploy to GitHub Pages

## Content conventions

Each long-form post is stored as a page bundle:

```text
content/posts/<slug>/
├── index.md
├── cover.png
└── img/
```

Common front matter fields:

```yaml
---
title: "Post Title"
date: 2026-01-01
summary: "Short description for listing cards."
tags: ["tag"]
categories: ["category"]
series: ["Series Name"]
showTableOfContents: true
tocPosition: right
---
```

## Quality and security standards

- Sensitive tokens, credentials, hostnames, and personal data should be removed or replaced with `[REDACTED]` before publishing.
- Writeups should prioritize reproducibility, clear methodology, and defensive takeaways.
- CVE and exploit content should include mitigation guidance and responsible framing.
- Generated assets should be optimized and kept consistent with the site visual system.

## Author

Rai2en - Security Researcher and Offensive Security Enthusiast

- GitHub: https://github.com/Rai2en
- LinkedIn: https://www.linkedin.com/in/crispus-houessou/
- X: https://x.com/0xR4zn
- Website: https://rai2en.github.io/

## License

This repository is released under the MIT License. See [LICENSE](LICENSE) for details.
