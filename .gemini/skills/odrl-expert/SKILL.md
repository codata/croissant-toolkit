---
name: odrl-expert
description: Specialized in ODRL (Open Digital Rights Language) policies, decentralized identifiers (DIDs), and verifiable credentials (VCs) for data infrastructure. Integrated with the CA4EOSC ODRL-infra.
---

# ODRL Expert Skill

The ODRL Expert skill enables precise management of digital rights policies using the [ODRL V2.2](https://www.w3.org/TR/odrl-model/) standard, integrated with [Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) and [Verifiable Credentials (VCs)](https://www.w3.org/TR/vc-data-model/).

## Core Concepts
- **ODRL Policy**: A JSON-LD document defining permissions (allowances), prohibitions (restrictions), and duties (obligations).
- **DID (Decentralized Identifier)**: Used for identifying all participants (Assigner, Assignee) and assets.
- **VC (Verifiable Credential)**: Used to prove attributes required by policies.
- **OAC Profile**: A specialized ODRL profile used in the `odrl-infra`.

## Persistence & Infrastructure Restriction
This skill now enforces a security layer across your entire toolkit. Every skill (Fact Checker, Editor, etc.) is registered as an **ODRL Asset** and restricted by a core **Policy Agreement**. 
- **Identity-First Access**: No skill can be executed without a valid DID from your wallet.
- **Infrastructure Logging**: Every protection action is recorded on the ODRL infrastructure for auditability.

## The ODRL Wallet
Your identity keys are stored locally and securely in:
- `~/.odrl/did.json`: Contains your master DID and **Private Key**.

## The Skill Vault (Encryption)
To prevent unauthorized access to skill source code on disk, you can archive skills into the **ODRL Vault**.
- **Encryption**: Skills are bundled into a ZIP archive protected by your **Master Private Key** as the password.
- **Workflow**:
    1.  `vault-skill`: Compresses the skill folder and deletes the plaintext source.
    2.  `unvault-skill`: Uses your private key to extract the skill back into the toolkit for use/updating.

## Usage

### 1. Initialize Your Wallet
Creates your unique OOYDID identity if it doesn't exist.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py init
```

### 2. Vault a Skill (Encrypt)
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py vault-skill "editor"
```

### 3. Unvault a Skill (Decrypt & Restore)
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py unvault-skill "editor"
```

### 4. Resolve a DID
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py resolve-did did:oyd:zQmcVH...
```

## Related Resources
- **Repository**: [CA4EOSC/odrl-infra](https://github.com/CA4EOSC/odrl-infra)
- **API Documentation**: [CODATA ODRL](https://odrl.dev.codata.org/docs)
- **ODRL Information Model**: [W3C Spec](https://www.w3.org/TR/odrl-model/)
