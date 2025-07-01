# Integrating with Axel

[Axel](https://github.com/futuroptimist/axel) is a personal LLM accelerator that organizes repositories and suggests quests across them. Pairing flywheel with Axel helps keep multiple projects spinning in sync.

## Quick start

1. Clone Axel next to this repository:
   ```bash
   git clone https://github.com/futuroptimist/axel
   ```
2. Add this repository to Axel's repo list:
   ```bash
   python -m axel.repo_manager add https://github.com/futuroptimist/flywheel
   ```
3. View the list with:
   ```bash
   python -m axel.repo_manager list
   ```

See `axel/README.md` for more details on managing repos and future roadmap items.
