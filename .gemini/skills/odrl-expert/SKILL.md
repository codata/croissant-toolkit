---
name: odrl-expert
description: Specialized in ODRL (Open Digital Rights Language) policies, decentralized identifiers (DIDs), and verifiable credentials (VCs) for data infrastructure.
---

# ODRL Expert Skill & Data Sovereignty

The **ODRL Expert** skill provides the technical foundation for **Data Sovereignty** within the Gemini CLI ecosystem. By combining decentralized identity (DIDs) with machine-readable usage policies (ODRL), it ensures that data and functional capabilities (skills) remain under the explicit control of their owners.

## 🛡️ Support for Data Sovereignty

Data sovereignty is the principle that data is subject to the laws and governance of the structures where it is collected or owned. This skill supports it through:

1.  **Decentralized Identity (DIDs)**: No central authority controls your identity. Your master key is stored locally in `~/.odrl/did.json`.
2.  **Explicit Usage Policies**: Using ODRL V2.2, you can define exactly who (Assignee) can do what (Action) with which asset (Target).
3.  **Encrypted Skill Vault**: Restricted skills are encrypted on disk using your private key, ensuring that even if the hardware is compromised, the high-value "restricted" logic remains inaccessible without authorization.
4.  **Auditability**: Every protection action is recorded on the ODRL infrastructure, providing a verifiable "chain of custody" for data and tool access.

## 🛠️ Available Methods (Client API)

### 1. `init`
Initializes your local ODRL wallet and generates your master **OOYDID** identity.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py init --email "your@email.com"
```

### 2. `introduce`
Introduce yourself and display your Decentralized Identity (DID).
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py introduce
```

### 3. `create-user`
Generates a new DID and security certificate for a specific user or agent.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py create-user "username" --email "user@email.com"
```

### 3. `resolve-did`
Resolves a DID string into its public document and attributes.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py resolve-did did:oyd:zQmcVH...
```

### 4. `vault-skill` (Encryption)
Encrypts a skill's source code into a ZIP archive using your private key and removes the plaintext directory.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py vault-skill "skill_name"
```

### 5. `unvault-skill` (Decryption)
Restores an encrypted skill from the vault back to the toolkit using your private key.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py unvault-skill "skill_name"
```

### 6. `revoke`
Officially revokes a DID on the infrastructure to prevent further authorized use.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py revoke did:oyd:zQmcVH...
```

### 7. `codata-brand` (Subskill)
Generates high-fidelity PDF reports with the official CODATA logo (from `codata.org/wp-content...`) automatically applied to every page. This ensures content matches the professional data sovereignty branding.
```bash
python3 .gemini/skills/odrl-expert/scripts/codata_branding.py --file input.html --output data/branded_report.pdf
```

### 8. `protect` (Policy Agreement)
Registers a skill or data asset as a protected entity and links it to a specific policy agreement.
```bash
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py protect "asset_name"
```

## 📐 Policy Templates
Standard templates are available in `.gemini/skills/odrl-expert/scripts/policy_templates.py` for:
- **Research Use Only**: Restricts actions to non-commercial analysis.
- **Attribution Required**: Mandates that the Assigner be credited in all outputs.
- **Time-Limited Access**: Automatically expires permissions after a set date.

---
**Repository**: [CA4EOSC/odrl-infra](https://github.com/CA4EOSC/odrl-infra)
