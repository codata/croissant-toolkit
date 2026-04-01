---
name: login
description: ODRL Secure Login Interface. Uses authorization keys from ~/.odrl/authorize.did to automatically unpackage protected skills from the vault.
---

# 🛡️ ODRL Login Skill

The **ODRL Login** skill provides a streamlined, automated way to authorize your toolkit workspace. It acts as an orchestrator for the **Vault**, allowing users with a valid `authorize.did` file to restore all restricted capabilities in a single command.

## 🌟 Features

1.  **Automated Authorization**: Automatically looks for the Master Private Key in `~/.odrl/authorize.did`.
2.  **Bulk Unvaulting**: Scans `.gemini/vault/*.zip` and attempts to restore all skills using the authorized key.
3.  **Conflict Resolution**: Uses `-o` (overwrite) to ensure that existing, potentially stale skill logic is replaced by the authorized, fresh version from the vault.
4.  **Security Integration**: Designed for use in **Environment Setup** or **CI/CD** contexts where manual unvaulting of every individual skill is impractical.

## 🛠️ Usage

### Log In and Unvault Skills
Restore all restricted skills to the `.gemini/skills/` directory using your authorization key:

```bash
python3 .gemini/skills/login/scripts/login_orchestrator.py
```

## 🏗️ Requirements
- **Location**: Your DID authorization file MUST be at `~/.odrl/authorize.did`.
- **Format**: The file must be a valid JSON-LD DID document following the **OOYDID** structure, containing a `keys.private_key` field.

---
**Zero-Trust Protocol**: This skill is **Public** to allow bootstrapping, but the actual logic of the "Unvaulted" skills remains protected until the correct key is provided.
