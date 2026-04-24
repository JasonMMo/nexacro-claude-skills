# Legacy GitLab Repo Archival Notice

**Phase 3 of Plan 1** (`docs/superpowers/plans/2026-04-23-nexacro-fullstack-starter-plan1.md`) calls for adding a migration banner to each of the 8 legacy GitLab sample repositories, then archiving them after 1–2 sprints of observation.

This document provides the **copy-paste template** and the **per-repo mapping** so the archival can be executed from the GitLab web UI (no API access required from Claude).

---

## 1. When to run this phase

Run Phase 3 **only after**:

- `JasonMMo/nexacroN-fullstack` is publicly reachable at the URL above
- Tag `v0.3.0-dual-lane` is visible on GitHub (dual-lane axiom proven)
- Tag `v1.8.0` on `nexacro-claude-skills` is published and marketplace installation works end-to-end

Today (2026-04-24) the first two conditions are met. The third lands with the Phase 4 release below.

---

## 2. Migration banner — paste at the **top** of each legacy README

```markdown
> ## 📢 This repository has moved
>
> As of **2026-04-24**, the 8 GitLab `nexacron-*` sample repositories have been
> consolidated into a single monorepo with a Claude Code installer plugin:
>
> - **Monorepo:** https://github.com/JasonMMo/nexacroN-fullstack
> - **Installer plugin:** https://github.com/JasonMMo/nexacro-claude-skills
>   (plugin `nexacro-fullstack-starter`, v0.1.0 / skills v1.8.0)
>
> ### How to get the runner that used to live here
>
> ```
> /plugin marketplace add JasonMMo/nexacro-claude-skills
> /plugin install nexacro-fullstack-starter@nexacro-claude-skills
> /nexacro-fullstack-starter
>   PROJECT_NAME=my-project
>   JDK=<JDK_FOR_THIS_REPO>
>   FRAMEWORK=<FRAMEWORK_FOR_THIS_REPO>
>   BACKEND_URL=http://localhost:8080
> ```
>
> The plugin will sparse-clone only the runner you asked for and substitute
> project-specific tokens — no 8-way manual diff required.
>
> ### Why we did this
>
> Previously, adding one endpoint meant editing up to 8 repos. After consolidation
> the business tree is shared across runners (`shared-business/{jakarta,javax}`),
> and the installer picks the right Spring/servlet/JDK combination from a single
> source of truth (`assets/matrix.json`).
>
> **This repository will be archived on 2026-05-15** (≈3 weeks from posting).
> Clone any local history you still need before that date.
```

---

## 3. Per-repo parameter cheatsheet

When pasting the banner into each repo's `README.md`, replace `<JDK_FOR_THIS_REPO>` and `<FRAMEWORK_FOR_THIS_REPO>` with the values from this table (matching `assets/matrix.json`):

| Legacy repo (expected GitLab name) | `JDK`  | `FRAMEWORK`        | Runner in monorepo                  | Status      |
|------------------------------------|--------|--------------------|--------------------------------------|-------------|
| `nexacron-boot-jakarta`            | `17`   | `boot`             | `boot-jdk17-jakarta`                 | ✅ proven   |
| `nexacron-boot-javax`              | `8`    | `boot`             | `boot-jdk8-javax`                    | ✅ proven   |
| `nexacron-mvc-jakarta`             | `17`   | `mvc`              | `mvc-jdk17-jakarta`                  | 🏗 scaffold  |
| `nexacron-mvc-javax`               | `8`    | `mvc`              | `mvc-jdk8-javax`                     | 🏗 scaffold  |
| `nexacron-egov5-boot-jakarta`      | `17`   | `egov5-boot`       | `egov5-boot-jdk17-jakarta`           | 🏗 scaffold  |
| `nexacron-egov4-boot-javax`        | `8`    | `egov4-boot`       | `egov4-boot-jdk8-javax`              | 🏗 scaffold  |
| `nexacron-egov4-mvc-javax`         | `8`    | `egov4-mvc`        | `egov4-mvc-jdk8-javax`               | 🏗 scaffold  |
| `nexacron-webflux-jakarta`         | `17`   | `webflux`          | `webflux-jdk17-jakarta`              | 🏗 scaffold  |

> **"✅ proven"** = runner fully built & smoke-tested at v1.8.0 release time.
> **"🏗 scaffold"** = directory exists in the monorepo with a `README.md`; implementation ships in follow-up v1.8.x point releases reusing the business trees from the two proven lanes.

The plugin's compatibility matcher rejects invalid combinations with a clear message, so even if a user copies the wrong JDK/FRAMEWORK from a future repo the installer will refuse and suggest the right pair.

---

## 4. Archival steps (GitLab web UI, per repo)

1. Edit `README.md` → paste banner from Section 2 at the very top (before any existing content).
2. Commit as `docs: add migration notice to nexacroN-fullstack monorepo`.
3. **Do NOT archive yet** — leave the repo writable for 2–3 weeks so anyone tracking the branch picks up the banner on next pull.
4. On or after **2026-05-15**:
   - Settings → General → Advanced → **Archive project**.
   - Repository will become read-only. History stays reachable via direct URL.
5. After all 8 repos are archived, update the root README of this plugin repo to note "legacy GitLab repos archived".

---

## 5. Verification

After banner-pasting, the following should be true without any code changes:

- [ ] All 8 legacy `README.md` files start with a `> ## 📢 This repository has moved` block.
- [ ] The monorepo link in each banner resolves to a 200 OK on GitHub.
- [ ] The plugin install command in each banner works end-to-end against a scratch directory (dry-run script in this repo at `scripts/dryrun_plugin_install.py` can be reused for CI gating).

When those three are green, Phase 3 is operationally complete; the actual `Archive project` button click happens on schedule.

---

## 6. Rollback

If the consolidation turns out to be broken for a specific runner, **do not un-archive**. Instead:

1. Land the fix in `JasonMMo/nexacroN-fullstack`, bump the monorepo tag (e.g., `v0.3.1`).
2. Publish a new plugin point release (`v1.8.x`) that pins the new monorepo ref.
3. Keep the legacy archival in place — the fix flows through the plugin, not through un-archiving.
