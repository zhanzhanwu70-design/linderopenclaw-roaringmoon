#!/usr/bin/env python3
"""Measure agent 'bubble' rate from OpenClaw session transcripts.

Read-only. Follows the DeLM definition (arXiv:2606.10662): bubble = agent
wall-clock time spent NOT advancing the solution.

Methodology notes (matters — earlier naive version was wrong):
  * Sessions are split into TURNS (a turn = user message -> assistant final).
    A cron session file can span days; that idle gap is NOT agent bubble.
  * Parallel tool calls overlap, so bubble = UNION of [call_start, result_end]
    intervals, not their sum. Summing double-counts concurrent waits.
  * Tool result that never arrives (interrupted turn) contributes no interval.
  * Within a turn, bubble is classified as:
      relay   : waiting on another agent/session (sessions_send/yield/spawn)
      barrier : waiting on a local tool that took > SLOW_TOOL_MS
      local   : waiting on a fast local tool
  * Turns longer than MAX_TURN_S are excluded from the aggregate (clock skew,
    suspended machines, or a turn spanning a scheduled gap).

Usage: measure_bubble.py [max_turn_s] [agents,comma]
"""
import glob
import json
import os
import subprocess
import sys
from collections import defaultdict

AGENTS_DIR = "/home/amr/.openclaw/agents"
SLOW_TOOL_MS = 5000
MAX_TURN_S = 3600
CROSS_AGENT_TOOLS = {"sessions_send", "sessions_yield", "sessions_spawn", "sessions_list", "subagents"}


def read_file(path):
    try:
        cmd = ["zstdcat", path] if path.endswith(".zst") else ["cat", path]
        return subprocess.run(cmd, capture_output=True, timeout=90).stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def ts_ms(t):
    if not t:
        return None
    try:
        date, _, time = t.replace("Z", "").partition("T")
        y, mo, d = (int(x) for x in date.split("-"))
        p = time.split("+")[0].split(":")
        h, mi = int(p[0]), int(p[1])
        sec = float(p[2]) if len(p[2:]) else 0.0
        return int((y * 12 + mo) * 31 + d) * 86400000 + int((h * 3600 + mi * 60 + sec) * 1000)
    except Exception:
        return None


def parse_msgs(text):
    out = []
    for line in text.splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") != "message":
            continue
        m = d.get("message")
        if not isinstance(m, dict):
            continue
        ts = ts_ms(d.get("timestamp"))
        role = m.get("role")
        calls, results = [], []
        if role == "toolResult":
            cid = m.get("toolCallId")
            if cid:
                results.append((cid, m.get("toolName")))
        else:
            for it in (m.get("content") or []):
                if not isinstance(it, dict):
                    continue
                if it.get("type") == "toolCall":
                    calls.append((it.get("id"), it.get("name")))
                elif it.get("type") == "toolResult":
                    cid = it.get("toolCallId")
                    if cid:
                        results.append((cid, it.get("toolName")))
        out.append({"ts": ts, "role": role, "calls": calls, "results": results})
    return out


def merge(intervals):
    """Union of [start,end] intervals -> total ms + merged list."""
    if not intervals:
        return 0, []
    iv = sorted(intervals)
    merged = [list(iv[0])]
    for s, e in iv[1:]:
        if s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return sum(e - s for s, e in merged), merged


def split_turns(msgs):
    """Yield turn dicts delimited by user messages."""
    turns = []
    cur = None
    for m in msgs:
        if m["role"] == "user" and m["ts"]:
            if cur:
                turns.append(cur)
            cur = {"msgs": [m]}
        elif cur is not None:
            cur["msgs"].append(m)
    if cur:
        turns.append(cur)
    return turns


def analyze_turn(turn):
    msgs = turn["msgs"]
    times = [m["ts"] for m in msgs if m["ts"]]
    if len(times) < 2:
        return None
    t0, t1 = min(times), max(times)
    wall = t1 - t0
    if wall <= 0 or wall > MAX_TURN_S * 1000:
        return None

    call_at = {}
    call_name = {}
    for m in msgs:
        for cid, nm in m["calls"]:
            if m["ts"]:
                call_at[cid] = m["ts"]
                call_name[cid] = nm

    relay_iv, barrier_iv, local_iv = [], [], []
    n_results = 0
    for m in msgs:
        for cid, nm in m["results"]:
            start = call_at.get(cid)
            if start is None or not m["ts"]:
                continue
            dur = m["ts"] - start
            if dur < 0:
                continue
            n_results += 1
            if nm in CROSS_AGENT_TOOLS:
                relay_iv.append((start, m["ts"]))
            elif dur >= SLOW_TOOL_MS:
                barrier_iv.append((start, m["ts"]))
            else:
                local_iv.append((start, m["ts"]))

    relay, _ = merge(relay_iv)
    barrier, _ = merge(barrier_iv)
    local, _ = merge(local_iv)
    total, _ = merge(relay_iv + barrier_iv + local_iv)
    return {
        "wall": wall,
        "bubble": total,
        "relay": relay,
        "barrier": barrier,
        "local": local,
        "results": n_results,
        "calls": len(call_at),
    }


def main():
    global MAX_TURN_S
    max_turn = int(sys.argv[1]) if len(sys.argv) > 1 else MAX_TURN_S
    agents = (sys.argv[2] if len(sys.argv) > 2 else "roaringmoon").split(",")
    MAX_TURN_S = max_turn

    turns_all = []
    for a in agents:
        for f in sorted(glob.glob(os.path.join(AGENTS_DIR, a, "sessions", "*.jsonl*"))):
            msgs = parse_msgs(read_file(f))
            for t in split_turns(msgs):
                r = analyze_turn(t)
                if r:
                    r["agent"] = a
                    turns_all.append(r)

    if not turns_all:
        print("no usable turns")
        return
    agg = defaultdict(float)
    for r in turns_all:
        for k in ("wall", "bubble", "relay", "barrier", "local"):
            agg[k] += r[k]
        agg["results"] += r["results"]
        agg["calls"] += r["calls"]

    wall = agg["wall"] or 1
    print(f"agents={agents}  turns analyzed: {len(turns_all)}  (turn cap {max_turn}s)")
    print(f"total active turn time: {agg['wall']/3600000:.2f} h")
    print(f"tool calls: {int(agg['calls'])}   tool results: {int(agg['results'])}")
    print()
    print("BUBBLE DECOMPOSITION (union of wait intervals, no double-count)")
    print(f"  total bubble     {agg['bubble']/3600000:8.2f} h  ({agg['bubble']/wall*100:5.1f}% of active turn time)")
    print(f"    relay (cross-agent) {agg['relay']/3600000:6.2f} h  ({agg['relay']/wall*100:5.1f}%)")
    print(f"    barrier (>5s local) {agg['barrier']/3600000:6.2f} h  ({agg['barrier']/wall*100:5.1f}%)")
    print(f"    local fast tool   {agg['local']/3600000:6.2f} h  ({agg['local']/wall*100:5.1f}%)")
    print()
    turns_all.sort(key=lambda r: -r["bubble"])
    print(f"{'wall_s':>9}{'bubble_s':>11}{'bubble%':>9}{'relay_s':>10}{'barrier_s':>11}{'calls':>7}{'results':>9}")
    for r in turns_all[:15]:
        print(f"{r['wall']/1000:>9.1f}{r['bubble']/1000:>11.1f}"
              f"{(r['bubble']/r['wall']*100 if r['wall'] else 0):>8.1f}%"
              f"{r['relay']/1000:>10.1f}{r['barrier']/1000:>11.1f}{int(r['calls']):>7}{int(r['results']):>9}")
    # distribution
    buckets = defaultdict(int)
    for r in turns_all:
        p = r["bubble"] / r["wall"] * 100 if r["wall"] else 0
        b = "0-10%" if p < 10 else "10-30%" if p < 30 else "30-60%" if p < 60 else "60-90%" if p < 90 else "90-100%"
        buckets[b] += 1
    print()
    print("turn distribution by bubble%:")
    for b in ("0-10%", "10-30%", "30-60%", "60-90%", "90-100%"):
        n = buckets.get(b, 0)
        print(f"  {b:<8} {n:>5} turns  ({n/len(turns_all)*100:4.1f}%)")


if __name__ == "__main__":
    main()
