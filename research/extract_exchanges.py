#!/usr/bin/env python3
"""Extract multi-agent exchanges (sessions_send call -> target reply) from OpenClaw transcripts.

Read-only. Scans ~/.openclaw/agents/*/sessions/*.jsonl* and pairs each
sessions_send toolCall with its matching toolResult (role="toolResult",
toolCallId=<call id>). Trajectory files are skipped (they duplicate session files).

Output JSONL: one record per exchange.
  {"source_agent", "target", "timestamp", "prompt", "reply", "status", "session_file"}
"""
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter

AGENTS_DIR = "/home/amr/.openclaw/agents"
OUT = "/home/amr/.openclaw/workspace-roaringmoon/research/exchanges.jsonl"


def read_file(path):
    try:
        cmd = ["zstdcat", path] if path.endswith(".zst") else ["cat", path]
        p = subprocess.run(cmd, capture_output=True, timeout=40)
        return p.stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def flatten(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for it in content:
            if not isinstance(it, dict):
                continue
            if it.get("type") == "text":
                parts.append(it.get("text", ""))
        return "\n".join(parts)
    return json.dumps(content, ensure_ascii=False)


def reply_text_from_result(content):
    """sessions_send tool results are JSON blobs; pull the human-readable reply out."""
    raw = flatten(content)
    try:
        obj = json.loads(raw)
    except Exception:
        return raw, "nonjson"
    if isinstance(obj, dict):
        status = obj.get("status") or obj.get("deliveryStatus") or "unknown"
        for key in ("reply", "message", "text", "response", "result"):
            val = obj.get(key)
            if isinstance(val, str) and val.strip():
                return val, status
        # nested payloads
        for key in ("result", "payload", "data"):
            val = obj.get(key)
            if isinstance(val, dict):
                for k2 in ("reply", "message", "text"):
                    v2 = val.get(k2)
                    if isinstance(v2, str) and v2.strip():
                        return v2, status
        return raw, status
    return raw, "unknown"


def main():
    all_files = sorted(glob.glob(os.path.join(AGENTS_DIR, "*", "sessions", "*.jsonl*")))
    files = [f for f in all_files if ".trajectory." not in f]
    sys.stderr.write("scanning %d session files (%d trajectory skipped)\n" % (len(files), len(all_files) - len(files)))
    records = []
    stats = Counter()
    for f in files:
        text = read_file(f)
        if not text or "sessions_send" not in text:
            continue
        stats["files_with_sends"] += 1
        messages = []
        for line in text.splitlines():
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") == "message" and isinstance(d.get("message"), dict):
                messages.append((d.get("timestamp"), d["message"]))
        calls = {}
        results = {}
        for ts, m in messages:
            role = m.get("role")
            if role == "toolResult" and m.get("toolName") == "sessions_send":
                results[m.get("toolCallId")] = (ts, m.get("content"))
                continue
            content = m.get("content")
            if role == "assistant" and isinstance(content, list):
                for it in content:
                    if isinstance(it, dict) and it.get("type") == "toolCall" and it.get("name") == "sessions_send":
                        calls[it.get("id")] = (ts, it.get("arguments", {}) or {})
        if not calls:
            continue
        src = f.split(os.sep)[-3]
        for tcid, (ts, args) in calls.items():
            prompt = args.get("message") or ""
            target = args.get("sessionKey") or args.get("agentId") or args.get("label") or "?"
            if tcid not in results:
                stats["send_no_result"] += 1
                continue
            rts, rcontent = results[tcid]
            reply, status = reply_text_from_result(rcontent)
            if not reply.strip():
                stats["empty_reply"] += 1
                continue
            stats["status_" + str(status)] += 1
            records.append({
                "source_agent": src,
                "target": str(target),
                "timestamp": ts,
                "reply_timestamp": rts,
                "prompt": prompt,
                "reply": reply,
                "status": status,
                "session_file": os.path.basename(f),
            })
            stats["exchanges"] += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    sys.stderr.write("stats: %s\n" % dict(stats))
    sys.stderr.write("wrote %d exchanges -> %s\n" % (len(records), OUT))


if __name__ == "__main__":
    main()
