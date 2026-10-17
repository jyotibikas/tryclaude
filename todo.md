# tryclaude TODO

Last updated: 2026-10-17. A one-page "Hello, world!" site (`index.html`) exists
in the repo root and is committed and pushed to `main`. Whether GitHub Pages is
enabled and the live site loads has not been verified. The site has no real
content yet.

## Maintenance instructions

- Read the current user request and relevant project materials before updating
  this file. User instructions and applicable repository rules take precedence.
- Keep the format simple. Use `[ ]` for unfinished work and `[x]` for work that
  meets the stated task conditions. No task IDs or status tables are required.
- Write concrete tasks with observable outcomes. Split implementation and
  verification when they can be completed independently.
- Add short qualifiers when useful: `(in progress)`, `(needs verification)`,
  `(blocked: reason; unblock action)`, or `(deferred: reason)`.
- Record evidence in the progress paragraph beneath the relevant checklist:
  what was checked, when, and the result. Link to files or artifacts where useful.
  Label historical reports and user confirmations as such. Never invent results.
- Keep verification specific to its scope. A local test does not prove a live
  integration works; one device or environment does not prove another works.
- Keep each checkbox in one main section. The next-steps list is a short ordered
  summary referencing those sections, so it cannot develop conflicting statuses.
- After meaningful work, update affected checkboxes, section notes, next steps,
  and the date. If verification remains, leave that task unchecked and say why.
  Reopen tasks when evidence contradicts completion.
- Preserve unrelated tasks and user edits. Record reasons for deferral or
  cancellation; do not silently remove real work. Add newly discovered necessary
  tasks without treating them as authorization to expand the current request.
- Use checks appropriate to the project, including tests, artifact review,
  calculations, or manual walkthroughs. Never store credentials or secrets here.
- Keep notes concise and current. Ordinary discussion need not change the file.

## Next steps

1. Enable GitHub Pages and confirm the live site loads — Publish the site
2. Decide what the site is for and who it's for — Define the project
3. Replace the placeholder page with real content — Build the site

The placeholder page is ready to publish; the only dependency is turning on
Pages in the repository settings (the repo must be public on a free plan).

## 1. Define the project

- [ ] Describe the site's purpose and intended audience
- [ ] Decide what pages and content the site needs
- [ ] Agree on scope and exclusions

Not assessed. So far the goal is only "a simple GitHub Pages site that says
hello world for now."

## 2. Set up the foundation

- [x] Create the repository and connect it to GitHub (`origin`)
- [x] Add agent instructions (`AGENTS.md`, with `CLAUDE.md` importing it) and
      this checklist

2026-10-17: Repo `jyotibikas/tryclaude` exists with `main` tracking
`origin/main`. `AGENTS.md` and `CLAUDE.md` added; not yet committed.

## 3. Build the site

- [x] Create a placeholder `index.html` that says "Hello, world!"
- [ ] Replace the placeholder with real content (blocked: content not defined;
      see section 1)
- [ ] Review the page on a phone-width screen

2026-10-17: `index.html` committed in `b20f2c8` and pushed to `origin/main`.
Not yet viewed in a browser.

## 4. Publish the site

- [ ] Enable GitHub Pages (Settings → Pages → Deploy from a branch → `main`,
      `/ (root)`)
- [ ] Verify https://jyotibikas.github.io/tryclaude/ loads and shows the
      current page

Not verified: Pages settings haven't been checked and the URL hasn't been
loaded.

## 5. Final polish

- [ ] Update `README.md` to describe the site and link to it

`README.md` currently reads "hello github world".

## Blockers and decisions

- **Blocker:** none recorded
- **Open question:** What should the site contain beyond "Hello, world!"?
  Needed before section 3 can continue.
- **Decision:** 2026-10-17, serve the site from the repo root on `main` with
  plain HTML (no build step), to keep it simple.
