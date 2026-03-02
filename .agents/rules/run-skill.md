---
trigger: always_on
---

When running skill scripts, use: "venv\Scripts\activate && python <script>" to ensure the venv is used.
When creating temporary or scratch scripts, save them in the project's tmp/ directory (e.g., tmp/scratch.py), never to C:\ or the user's home folder.