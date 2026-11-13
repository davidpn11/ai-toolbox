"""Runs the cost-guard hooks against tests/cases.json in a temporary project and home folder.
Usage: python3 plugins/cost-guards/tests/test.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = {"read": "read_guard.py", "spawn": "spawn_guard.py"}
spec = json.load(open(os.path.join(HERE, "cases.json")))

with tempfile.TemporaryDirectory() as tmp:
    proj, home = os.path.join(tmp, "proj"), os.path.join(tmp, "home")
    os.makedirs(os.path.join(proj, ".claude", "agents"))
    os.makedirs(os.path.join(home, ".claude", "agents"))
    for name, lines in spec["files"].items():
        open(os.path.join(proj, name), "w").write("x\n" * lines)
    open(os.path.join(proj, "shot.png"), "wb").write(b"\x89PNG\0" + b"\n" * 900)
    for name, model in spec["agents"].items():  # half in the project, half global, like a real install
        where = proj if name != "scout" else home
        open(os.path.join(where, ".claude", "agents", name + ".md"), "w").write(
            f"---\nname: {name}\ndescription: test\nmodel: {model}\n---\n\nbody\n")
    failed = 0
    for case in spec["cases"]:
        env = {"PATH": os.environ["PATH"], "HOME": home, **case.get("env", {})}
        if "raw" in case:
            stdin = case["raw"]
        else:
            stdin = json.dumps({"cwd": proj, **case["input"]}).replace("$DIR", proj)
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "..", "hooks", HOOKS[case["hook"]])],
                           input=stdin, capture_output=True, text=True, env=env, cwd=proj)
        got = "allow"
        if r.stdout.strip():
            got = json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"]
        if r.returncode != 0 or got != case["want"]:
            failed += 1
            print(f"FAIL {case['hook']}: {case['name']}: want {case['want']}, got {got} (exit {r.returncode}) {r.stderr.strip()}")
    print(f"{len(spec['cases']) - failed}/{len(spec['cases'])} passed")
    sys.exit(1 if failed else 0)
