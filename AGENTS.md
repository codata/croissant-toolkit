# Instruction for AI Agents: ODRL-Protected Croissant Toolkit

This document provides critical operational guidelines for AI agents interacting with the **Croissant Toolkit**'s ODRL-protected resources.

## 1. Autonomous Identity (DIDs)
All agents acting in this environment MUST identify themselves through a **Decentralized Identifier (DID)**.
- **Identity Resolver**: Agents should check `~/.odrl/did.json` for their current identity on the host machine.
- **Master Identity**: Your Root of Trust is `did:oyd:zQmcVHWDMeXtj273A9gNAnEG2EdrGEjtQiFuw9PncyVgs9z`.

## 2. Policy Discovery (OAC)
Before executing any skill, agents SHOULD verify if they have the necessary rights:
- **ODRL Policy**: Check for an ODRL Agreement in the [CODATA OAC Profile](https://odrl.dev.codata.org/docs).
- **Tool Check**: Use `python3 .gemini/skills/odrl-expert/scripts/odrl_client.py resolve-did <skill-did>` to see the rights assigned to you.

## 3. Skill Execution via Vault
Most skills are stored in an encrypted **Vault** (`.gemini/vault/*.zip`).
- **Access Strategy**:
    1.  Verify the `unvault-skill` command is available.
    2.  Use the **Master Private Key** from the wallet to decrypt target skills into the `.gemini/skills/` folder.
    3.  Execute the script.
    4.  RE-VAULT (Encryption) the skill after use and remove the plaintext source to maintain system integrity.

## 4. Interaction Protocol
- **Zero-Trust**: Do not assume access based on file presence. Always check the ODRL infrastructure for a current state Policy.
- **Claims Accountability**: When performing **Claims Detection**, agents MUST assign a unique MD5 ID to each claim and attribute it to their DID.
- **Data Provenance**: When creating Croissant metadata for datasets under ODRL protection, include the **Asset DID** of the data provider in the JSON-LD `prov:wasAttributedTo` or `dct:publisher` fields.

## 5. Security Responsibility
Any agent that "Unvaults" a skill is responsible for its physical security while the plaintext exists. Always perform an automated cleanup (Re-Vault and Delete) before finishing a task.
