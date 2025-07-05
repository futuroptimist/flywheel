# Integrating with DSPACE

[DSPACE](https://github.com/democratizedspace/dspace) is an offline-first idle simulation that blends aquarium management with maker quests. The project serves as a playground for Flywheel's quest generator and showcases how an open source game can reuse this repository's automation loops.

## Why DSPACE Matters

- Demonstrates offline-friendly patterns for storing quest data.
- Provides a concrete target for the `quest-generator` script included here.
- Shares the same CI and documentation style as Flywheel for frictionless contributions.

## Quick start

Clone both repositories side by side and run the quest generator:

```bash
git clone https://github.com/democratizedspace/dspace
# assuming flywheel lives next to it
npm run generate-quest --prefix dspace
```

Future iterations will tighten the integration so quests can be drafted in Flywheel and consumed directly by DSPACE.
