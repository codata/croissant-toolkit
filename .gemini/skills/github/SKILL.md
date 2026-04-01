---
name: github
description: Secure GitHub Orchestrator for Croissant Toolkit. Connect any repository, discovery skills, and audit ODRL sovereignty status.
---

# 🐙 GitHub Skill

The **GitHub Skill** provides a secure bridge between the **Croissant Toolkit** and remote repositories. It allows for the discovery and orchestration of skills across the entire ecosystem, ensuring that **ODRL usage policies** are enforced regardless of where the skill is hosted.

## 🌟 Features

1.  **Repository Connection**: Connect to any public or private GitHub repository via the GitHub API.
2.  **Sovereignty Audit**: Automatically extracts the **Master Identity (DID)** from `AGENTS.md` to verify the repository owner.
3.  **Skill Discovery**: Automatically list open and restricted (vaulted) skills in a remote repository.
4.  **Secure Orchestration**: Acknowledge and verify decentralized identities (DIDs) during cross-repository skill invocation.

## 🛠️ Usage

### Connect and Audit a Repository
Get a security status and skill listing for a remote repository:

```bash
python3 .gemini/skills/github/scripts/github_orchestrator.py --status https://github.com/codata/croissant-toolkit
```

### Sync Skills (Upcoming)
Sync remote open skills directly to your local `.gemini/skills/` directory for immediate use.

## 📐 Authentication
To access private repositories or increase API rate limits:
1.  Generate a **Personal Access Token (classic)** on GitHub with `repo` scopes.
2.  Export it as an environment variable:
    ```bash
    export GITHUB_TOKEN="your-token-here"
    ```

---
**Restricted Logic**: Advanced repository synchronization and automated ODRL agreement negotiation are vaulted to prevent unauthorized redistribution of sovereign toolchains.
