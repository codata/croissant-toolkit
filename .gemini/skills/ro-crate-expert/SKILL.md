---
name: ro-crate-expert
description: Specialized in creating RO-Crate packages from Dataverse metadata, with integrated ODRL-based DID (Decentralized Identifier) attribution and provenance via the ro-crate-py library.
---

# RO-Crate Expert Skill

The **RO-Crate Expert** skill bridges Dataverse Research Repositories with the **RO-Crate** standard, utilizing the **ODRL Expert** for decentralized identity and the [RO-Crate 1.1 Specification](https://www.researchobject.org/ro-crate/1.1/) for data packaging.

## 🌟 Key Features

1.  **Dataverse Integration**: Pull Schema.org and OAI_ORE metadata from Dataverse using persistent IDs (DOIs).
2.  **DID Attribution**: Generate a unique OOYDID (via ODRL) for the dataset, ensuring its identity is globally resolvable.
3.  **Automated File Downloads**: Discover dataset files via OAI_ORE and download them directly into the RO-Crate package.
4.  **RO-Crate Packaging**: Convert metadata and downloaded files into the standard RO-Crate format using the `rocrate-py` library.
5.  **Provenance (PROV)**: Embed the DID of the asset in the `prov:wasAttributedTo` field for cryptographically verified source identification.
6.  **Digital DID Documents**: Create the "digitally signed file" (DID Package) containing the DID's public and private keys, resolvable to JSON in the universal resolver.

## 🛠️ Setup

Before using the skill, ensure the `rocrate` library is installed. This project includes a local copy of `ro-crate-py`:

```bash
pip install -e ro-crate-py
```

## 🛠️ Usage

### Generate an RO-Crate from Dataverse
Uses the Dataverse API to fetch metadata, creates a new DID for the crate, and packages the result using the `rocrate-py` library.

```bash
python3 .gemini/skills/ro-crate-expert/scripts/create_crate.py "https://demo.dataverse.org/dataset.xhtml?persistentId=doi:10.70122/FK2/TTSEXH" --zip
```

### Inspect Crate for Provenance
Reads a ZIP package, extracts the asset's DID, and resolves its full provenance information via the ODRL expert.

```bash
python3 .gemini/skills/ro-crate-expert/scripts/inspect_crate.py "data/rocrate_${DID}.zip"
```

### Resulting Artifacts
- **`ro-crate-metadata.json`**: The core RO-Crate metadata generated via `rocrate-py`.
- **`did_signature.json`**: The "digitally signed file" (DID Package) comprising the asset's decentralized identity credentials.
- **`data/rocrate_${DID}.zip`**: A compressed package containing all files and metadata, named after the generated DID.
- **`data/rocrate_output/`**: The directory containing all research object components.

## 🔒 Security Architecture
Identity management is handled nativesly by the **ODRL Expert**. The resulting package includes an OOYDID that can be resolved via the [Universal Resolver](https://odrl.dev.codata.org/api/did/resolve/).

---
**Repository**: [ResearchObject/ro-crate-py](https://github.com/ResearchObject/ro-crate-py)
