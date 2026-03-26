# 🤖 How to use RO-Crate Expert in Claude

To "install" this skill in Claude, you can use one of the two following methods:

## Method 1: Claude Projects (Web Interface)
This is the easiest way to give Claude the *knowledge* of the skill.

1.  **Create a Project**: Go to [Claude.ai](https://claude.ai) and create a new Project.
2.  **Upload the Knowledge**: Upload the following files from this toolkit:
    *   `.gemini/skills/ro-crate-expert/scripts/create_crate.py`
    *   `.gemini/skills/ro-crate-expert/scripts/inspect_crate.py`
    *   `.gemini/skills/odrl-expert/scripts/odrl_client.py`
    *   `.gemini/skills/ro-crate-expert/SKILL.md` (as a text file)
3.  **Set Project Instructions**: Paste the content of `SKILL.md` into the **Project Instructions** field.
4.  **Usage**: Ask Claude to generate the commands for you. You will still need to run the Python scripts in your local terminal unless you are using a tool that executes code for Claude.

## Method 2: Claude Desktop + MCP (Automated Execution)
This method allows Claude to actually *run* the commands for you using the **Model Context Protocol**.

1.  **Install MCP Shell Server**: Ensure you have a shell-enabled MCP server (like the standard `filesystem` or a `shell` server).
2.  **Configuration**: In your `claude_desktop_config.json`, ensure Claude has access to this project directory.
3.  **Add Instructions**: Provide Claude with the path to the `SKILL.md` file or its content so it knows how to invoke the scripts.
4.  **Workflow**:
    *   User: "Create an RO-Crate for this Dataverse DOI: [DOI]"
    *   Claude: *Automatically executes the python script via MCP*

---
### 🛠️ Key Commands for Claude to remember:
*   **Create**: `python3 .gemini/skills/ro-crate-expert/scripts/create_crate.py "[DOI]" --zip`
*   **Inspect**: `python3 .gemini/skills/ro-crate-expert/scripts/inspect_crate.py "[ZIP_PATH]"`
