# Loading New Skills in Gemini CLI

The **Gemini CLI** is a dynamic, agentic interface that automatically discovers capabilities from the local workspace. To extend the agent's intelligence with a new skill, follow these integration steps.

## 1. Directory Structure

The CLI specifically looks for skills in the `.gemini/skills/` directory. Every new skill MUST follow this structure to be discoverable:

```text
.gemini/skills/my-new-skill/
├── SKILL.md              <-- This is the intelligence contract
└── scripts/              <-- This is the execution logic
    ├── my_tool.py
    └── test_my_tool.py   <-- Optional: recognized by 'test-all'
```

## 2. Defining the Intelligence Contract (`SKILL.md`)

The `SKILL.md` file serves as the documentation the Gemini agent reads to understand **when** and **how** to use your skill. It MUST include a YAML frontmatter:

```markdown
---
name: my-new-skill
description: Describe EXACTLY what this skill does and when the agent should pick it.
---

# My New Skill Documentation
Add usage examples and command line patterns here.
```

The agent uses the `description` field to map a user's natural language request to your scripts.

## 3. Registering the Skill

The Gemini CLI does not require a manual registry. Discovery happens at runtime:
1.  **Direct Command**: You can force the agent to use it:
    ```bash
    gemini "Use the my-new-skill to perform [ACTION]"
    ```
2.  **Autonomous Trigger**: If your `SKILL.md` description is clear, the agent will pick it automatically for relevant tasks.

## 4. Restoring Skills from the Vault

Many skills in the Croissant Toolkit are provided in an encrypted **Vault** (`.gemini/vault/*.zip`) for security. These skills are NOT available to the CLI until they are "Unvaulted":

```bash
# Decrypt the skill into the .gemini/skills/ directory
python3 .gemini/skills/odrl-expert/scripts/odrl_client.py unvault-skill "skill-name"
```

Once unvaulted, the `.gemini/skills/<skill-name>/SKILL.md` becomes visible, and the agent automatically "learns" its capabilities.

## 5. Verifying Installation

To ensure the CLI has correctly loaded the skill, you can ask for a system check:

```bash
gemini "Run all tests and verify my-new-skill is healthy"
```
This triggers the `test-all` skill which discovers and executes any `test_*.py` files in your new skill's `scripts/` folder.
