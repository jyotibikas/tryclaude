# tryclaude TODO

Last updated: 2026-10-18. A one-page "Hello, world!" site (`index.html`) exists
in the repo root and is committed and pushed to `main`. Whether GitHub Pages is
enabled and the live site loads has not been verified. The site has no real
content yet. `reactiveAgent.py` calls the Claude API (section 6); `run_agent`
and `AgentWithMemory` pass type checks and offline tests, but no live run has
been confirmed.

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
4. Run `reactiveAgent.py` live and record the results — Claude API experiments

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

## 6. Claude API experiments

- [x] Set up a Python environment with the Anthropic SDK (`.venv`,
      `requirements.txt`)
- [x] Move `ask_claude` and `run_agent` in `reactiveAgent.py` to
      `claude-sonnet-5-5`
- [x] Fix Pylance type errors in `run_agent`
- [x] Stop `run_agent` on refusals, `max_tokens` and other non-final stop
      reasons instead of resending the same request
- [x] `AgentWithMemory.chat`: read only text blocks from the reply instead of
      `response.content[0].text`, and raise `max_tokens` from 4096 to 16000
- [x] `AgentWithMemory.chat`: stop recursing with `chat("")` after a tool call,
      which adds an empty user message (now a loop capped at `max_iterations`)
- [x] `AgentWithMemory.chat`: save the full reply content to history instead of
      only its text, which drops thinking blocks
- [ ] Run `reactiveAgent.py` against the live API and record the results
      (needs verification)
- [ ] Ignore generated output (`investment.txt`) in `.gitignore`

2026-10-18: `anthropic` 1.15.0 installed in `.venv`. `basicAgentsAndTools.py`
was renamed to `reactiveAgent.py`, which now also holds `ask_claude`;
`setupAndTest.py` was removed. `helloworld.py` holds a single print statement.
An offline test with a fake client confirmed `run_agent` keeps thinking blocks
in history, returns after a tool call plus final answer, and makes only one call
on `max_tokens` or `refusal`. `investment.txt` exists, so Test 1 may have been
run, but no live run has been confirmed or reviewed. After the
`AgentWithMemory` text and `max_tokens` fixes, Pylance shows no problems in
`reactiveAgent.py`. After replacing the `chat("")` recursion with a loop, an
offline test with a fake client confirmed a tool call plus answer followed by a
second turn adds no empty user messages, history alternates user/assistant, and
endless tool calls stop at `max_iterations`. After saving full replies, the same
test confirmed every assistant turn keeps its thinking block and later requests
send it back. The class hasn't been run live.

## Blockers and decisions

- **Blocker:** none recorded
- **Open question:** What should the site contain beyond "Hello, world!"?
  Needed before section 3 can continue.
- **Decision:** 2026-10-17, serve the site from the repo root on `main` with
  plain HTML (no build step), to keep it simple.
