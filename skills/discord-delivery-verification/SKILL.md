---
name: "discord-delivery-verification"
description: "Verify Discord sends landed when receipts are ambiguous: split parts, char/line limits, channel-read proof."
---

# Discord delivery verification

Use this when an OpenClaw Discord send must be proven delivered: after a long or multi-part message, when a receipt reports more than one platform part, when a peer claims "published successfully" but you have not confirmed it, or when a segment appears to be missing.

## Steps

1. Establish the real limits before interpreting any split. Read `docs/gateway/config-channels.md` for the `maxLinesPerMessage` and `textChunkLimit` entries, grep the bundled `dist/` for the symbols `DISCORD_TEXT_CHUNK_LIMIT` and `DEFAULT_MAX_LINES`, then read the live `channels.discord` config for per-account `textChunkLimit` and `maxLinesPerMessage` overrides. Done when you can state both the hard character limit and the line limit, and whether this installation overrides either.
   - Discord enforces a hard character limit (2,000 by default) **and** a line limit (`maxLinesPerMessage`, default 17). Either one triggers a split, so a dense URL list can split well before the character limit.
   - Never attribute a split to a limit you have not read. One ~1,100-character split was first misread as a character cap; the line limit was the actual cause, and the wrong explanation survived into notes before being corrected.

2. Record what the send reported, and treat it as a claim. Capture `primaryPlatformMessageId`, `deliveryStatus`, and `payloadOutcomes.resultCount` for every part. Done when each reported part has an id you can search for in the channel.
   - `resultCount` above 1 means the platform posted more than one message for a single send; one tool response does not imply one platform message.
   - A peer's "published, deliveryStatus sent" report is also a claim. Verify it independently instead of forwarding it as proof.

3. Read the target channel's actual message list with the sending account's token, through the Discord REST endpoint `channels/<id>/messages?limit=N`. Keep the token inside the script and never print it; print only id, timestamp, character count, and the first ~80 characters. Done when you hold the real messages posted around the send time.
   - Reading another agent's channel through the message tool is unavailable; the REST read is the reliable path.
   - When the channel is yours and delivery must be confirmed, the same REST read gives the ground truth for every message id.
   - **A read that did not succeed proves nothing.** `403` means this account cannot see the channel (no VIEW_CHANNEL for it), `401` means the credential or header is wrong (the scheme must be `Bot`, not `Bearer`). Either way the read is **INCONCLUSIVE**, never evidence that a message is absent. Report INCONCLUSIVE and get a reader that has access; do not conclude "not sent" from a read you could not perform.
   - **An empty match set is not a pass.** When you compare the segments you expect against the segments you found, finding zero candidates means the comparison was inconclusive, not that the content is verified. Guard the pass condition on a non-empty found-set, and never let an empty comparison print "verified".
   - **When a correction is needed, make it shorter than the original.** REST `PATCH /channels/<id>/messages/<mid>` shares the 2,000-character cap with the message tool, so a correction that adds words can fail outright. Replace the wrong text with a shorter correct version, then re-read to confirm the change landed.

4. Locate every segment, including one that does not begin with your headline. Match candidates on a prefix, a suffix, and a distinctive content token; concatenate the segments in order and compare against the source text with a hash. Done when the concatenation is byte-identical to the source and every expected URL is present in the original order.
   - A split point can land inside a list, so the following segment may start with an arbitrary fragment such as `**補漏**`. Matching only the opening text silently loses the tail and makes a complete delivery look truncated.

5. Re-read with a larger limit and widen the match to suffix tokens whenever the number of located segments is fewer than the expected split count. Done when the located segments account for the entire source text, or you can name the specific missing segment.

6. Report the evidence rather than the intention. For each platform message state its id, character count, line count, `deliveryStatus`, and the hash comparison result, and name any segment you could not locate. Done when a reader can tell sent from not-sent without re-running anything.
   - Include which channel you read and which ids were confirmed, so the evidence stays reproducible after the fact.
