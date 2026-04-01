# 🚀 Deploying Croissant Toolkit to GitHub

This guide explains how to package the **Croissant Toolkit** and its specialized skills for deployment on GitHub and how to set up the toolkit in a new environment with full **ODRL protection**.

## 📁 Repository Structure

Your GitHub repository should follow this structure to balance open access with secure, restricted capabilities:

```text
croissant-toolkit/
├── .gemini/
│   ├── skills/         # Publicly available Python skills (e.g., unf, translator)
│   └── vault/          # Encrypted skill archives (.zip) — Safe to commit!
├── docs/               # Documentation (like this guide)
├── data/               # Persistent data (ignore in .gitignore)
├── requirements.txt    # Python dependencies
└── README.md           # Main project overview
```

---

## 🛠️ Step 1: Initializing the Toolkit

Before pushing to GitHub, you must establish your **Decentralized Identity (DID)** locally.

1.  **Initialize the Wallet**: This generates your master private key in `~/.odrl/did.json`.
    ```bash
    python3 .gemini/skills/odrl-expert/scripts/odrl_client.py init
    ```
2.  **Create an Admin Identity**: This allows you to sign and protect skills before committing.

> [!CAUTION]
> **NEVER commit your `~/.odrl/` directory.** This folder contains your master private key. If you lose this key or it is stolen, you lose control of your vaulted skills.

---

## 🛡️ Step 2: Protecting Restricted Skills

Specialized or sensitive skills (like `policy-maker` or `fact-checker`) should be **vaulted** before pushing the repo back to GitHub.

1.  **Vault a Skill**: This action encrypts the skill's source code into a `.zip` in `.gemini/vault/` and removes the plaintext folder from `.gemini/skills/`.
    ```bash
    python3 .gemini/skills/odrl-expert/scripts/odrl_client.py vault-skill "policy-maker"
    ```
2.  **Commit the Vault**: Now, you can securely push the `.zip` to GitHub. The logic is inaccessible without your private key.

---

## 🏗️ Step 3: Deployment in a New Environment

To use the toolkit on a new machine or for a new team member:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/codata/croissant-toolkit.git
    cd croissant-toolkit
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Restore Identity**:
    - If you are moving your own workspace, copy your `~/.odrl/did.json` to the new machine.
    - If you are a new user, run `odrl_client.py init` and have the admin grant your DID the necessary permissions.
4.  **Unvault Skills**: Restore the restricted logic back to the workspace.
    ```bash
    python3 .gemini/skills/odrl-expert/scripts/odrl_client.py unvault-skill "policy-maker"
    ```

## 🧩 Usage as a Git Submodule

If you want to integrate the **Croissant Toolkit**'s capabilities into an existing project (e.g., [codata/ollama](https://github.com/codata/ollama)), the recommended approach is using **Git Submodules**. This ensures you can easily pull updates while maintaining your project's primary logic.

### 1. Add the Toolkit to Your Project
Run this from the root of your target repository:
```bash
git submodule add https://github.com/codata/croissant-toolkit.git .gemini/croissant-toolkit
git commit -m "Add Croissant Toolkit as a submodule"
```

### 2. Initialize in a New Clone
When someone clones your repository, they must initialize the submodule to fetch the toolkit's code:
```bash
git clone --recursive https://github.com/your-org/your-project.git
# OR if already cloned:
git submodule update --init --recursive
```

### 3. Orchestration from the Parent Repo
You can call the toolkit's skills directly from the submodule path while maintaining your parent repo's ODRL identity:
```bash
# Call the UNF skill from the submodule
python3 .gemini/croissant-toolkit/.gemini/skills/unf/scripts/unf_hash.py "Data coming from Ollama"

# Orchestrate ODRL policies from the submodule
python3 .gemini/croissant-toolkit/.gemini/skills/policy-maker/scripts/policy_generator.py --describe --asset "Ollama Model Config"
```

### 4. Updating the Toolkit
To stay up to date with the latest skills and security fixes in the main toolkit:
```bash
cd .gemini/croissant-toolkit
git pull origin main
cd ..
git add .gemini/croissant-toolkit
git commit -m "Update Croissant Toolkit submodule to latest version"
```

---

## 🏗️ Step 4: Using the Toolkit Skills

Once set up, you can orchestrate multi-step workflows across localized data assets and global metadata standards.

### Example: Semantic Consistency Check
Process a local term, translate it to English, and validate it against a cross-language fingerprint:

```bash
# 1. Generate the consistency policy
python3 .gemini/skills/policy-maker/scripts/policy_generator.py \
  --type consistency \
  --asset "Température" \
  --english-term "Temperature"

# 2. Execute the validated translation
python3 .gemini/skills/translator/scripts/translate.py "Température" --target "English" --unf
```

---

## 💡 Best Practices for GitHub Managers

*   **Audit Your Vault**: Periodically check that no plaintext folders for restricted skills exist in `.gemini/skills/` before committing.
*   **Version Control**: Tag your releases (e.g., `v1.0.0`) so that the state of the vault matches the state of the documentation.
*   **Zero-Trust CI/CD**: If using GitHub Actions, inject your ODRL secret keys securely via GitHub Secrets to run automated integrity tests.

---
**Maintained by**: CODATA & Gemini 3 Hackathon 🥐
