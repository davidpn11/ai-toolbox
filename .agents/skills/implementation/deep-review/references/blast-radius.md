# Blast radius

Find what a change breaks somewhere else, before it ships. Listing the callers is not the job; grep does that in a second. The job is the breakage grep won't show you.

## Don't trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it's true. So find the one or two facts the whole thing depends on and prove them by running code.

For each fact the change's safety depends on, get it as far down this ladder as is cheap, and say where it stopped:

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, or the library's own source.
3. You showed the bad case can't happen. You walked the failure step by step and it doesn't reach.
4. You ran it. A script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app.

Any safety fact you can't get to step 4, say so. Don't write it up as settled. Step 4 is usually one small script that imports the same library the app ships and calls the exact function you're worried about.

## Steps

1. Read the change: the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff doesn't spell out. Pull the PR and commits.
2. Find the one fact it's safe because of. Most risky-looking changes are safe because of a single fact ("this call only drops already-dead cache entries"). Find it. If it holds, most risky cases clear at once.
3. Look where grep stops. Read the source of the library you call, its pinned version, any local patch. Work out when things run: microtasks, unmount and teardown, framework scheduling. Follow what a symbol search misses: the JSON an API returns, a DB column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. Be honest about each risk: a real chance of happening and a real cost if it does. Keep confirmed risks; list checked-and-cleared ones separately. Cite a real `file:line`. A search that finds nothing is still an answer. Never make up a caller or an API.
5. Prove the one fact. Write a script or test that runs the real code, run it, and paste what happened. If you can't prove it cheaply, mark it unproven.

## Hand back

- **What it does.** What changed, including the part that isn't obvious.
- **The one fact it's safe because of.** State it, the ladder step reached, and the proof, or "unproven".
- **Risks.** Only the real ones: how it breaks, `file:line`, likelihood, cost, how to check.
- **Cleared.** What you checked and why it's fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Do not invoke `/deep-review` or `/code-review`, or spawn additional agents: perform this review directly.
