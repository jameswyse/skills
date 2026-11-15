---
name: homelab
description: Use when a task needs another of the user's machines or a self-hosted service, such as SSH or file transfer to a fleet machine, or Proxmox, TrueNAS, DNS, UniFi, or media-server operations.
---

# Homelab access

The homelab repository owns access instructions, host inventory, and service
integrations. Follow it instead of personal SSH configuration or memory.

1. Use the checkout at `~/Projects/homelab`. If it is missing, report that and
   stop. Do not clone it without authorisation.
2. Read its `AGENTS.md`. Apply its update rule before relying on the docs, and
   report a blocked update rather than working from stale instructions.
3. Follow its routing to the host, runbook, or stack reference for the task.
   Connect to hosts in its fleet configuration only through `scripts/fleet`. For
   other hosts, follow that host's notes. Never accept a new or changed host key.

Reading documentation and running read-only commands are within an access
request. Changes on another machine or service need authorisation for that
action. Infrastructure changes also follow the homelab repository's change-note
rules.
