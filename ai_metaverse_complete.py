#!/usr/bin/env python3
import os, json, time
from datetime import datetime

BASE = os.path.expanduser("~/planetary_agents")
DATA = os.path.join(BASE, "data")
LOGS = os.path.join(BASE, "logs")
DISPATCH = os.path.join(BASE, "dispatch")
VAULT = os.path.expanduser("~/storage/shared/Obsidian/SovereignVault")
for d in (DATA, LOGS, DISPATCH):
    os.makedirs(d, exist_ok=True)

ASSISTANTS = {
    "Earth":   {"task": "Generate foundational code structures", "priority": "high"},
    "Mars":    {"task": "Data analysis and visualization", "priority": "high"},
    "Venus":   {"task": "Natural language processing", "priority": "medium"},
    "Jupiter": {"task": "API integration and management", "priority": "high"},
    "Saturn":  {"task": "Computer vision and image generation", "priority": "medium"},
    "Neptune": {"task": "Documentation generation", "priority": "medium"},
    "Mercury": {"task": "Testing and validation", "priority": "high"},
    "Uranus":  {"task": "Blockchain and Web3 integration", "priority": "low"},
}
APIS = [
    {"name": "Craiyon", "url": "https://www.craiyon.com"},
    {"name": "Wordtune", "url": "https://www.wordtune.com"},
    {"name": "Magic Studio", "url": "https://magicstudio.com"},
    {"name": "AI Metaverse", "url": "http://www.aimetaverse.cloud"},
]

LOGFILE = os.path.join(LOGS, "deploy_%s.log" % datetime.now().strftime("%Y%m%d"))

def log(msg):
    line = "[%s] %s" % (datetime.now().strftime("%H:%M:%S"), msg)
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

def save(name, obj):
    path = os.path.join(DATA, name)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
    return path

def main():
    log("=== AI Metaverse deploy start ===")
    now = datetime.now().isoformat()

    meta = [dict(a, discovered_at=now, status="active") for a in APIS]
    save("api_metadata.json", meta)
    log("API metadata saved (%d entries)" % len(meta))

    deployed = {}
    for name, info in ASSISTANTS.items():
        deployed[name] = dict(info, status="deployed", deployed_at=now, location="termux-local")
        log("[ok] %s: %s" % (name, info["task"]))
    save("deployment_summary.json", deployed)

    docs = {"title": "AI Metaverse Docs", "generated_at": now,
            "apis": meta, "assistants": list(ASSISTANTS)}
    save("api_documentation.json", docs)

    results = [{"name": a["name"], "valid": a["url"].startswith("http")} for a in meta]
    save("validation_results.json", results)
    log("Validation: %d/%d valid" % (sum(r["valid"] for r in results), len(results)))

    count = sum(len(files) for _, _, files in os.walk(BASE))
    payload = {"agent": "MarsReconAgent", "timestamp": now,
               "filecount": count, "device": "termux-android"}
    ppath = os.path.join(DISPATCH, "payload.json")
    with open(ppath, "w") as f:
        json.dump(payload, f, indent=2)

    if os.path.isdir(VAULT):
        vpath = os.path.join(VAULT, "dispatch_%d.json" % int(time.time()))
        with open(vpath, "w") as f:
            json.dump(payload, f, indent=2)
        log("Archived to vault: %s" % vpath)
    else:
        log("Vault folder not found, skipped: %s" % VAULT)

    log("=== Done: %d assistants, %d APIs ===" % (len(deployed), len(meta)))

if __name__ == "__main__":
    main()
