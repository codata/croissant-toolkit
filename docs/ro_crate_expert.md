# 📦 RO-Crate Expert Skill

The **RO-Crate Expert** skill bridges Dataverse Research Repositories with the **RO-Crate** (Research Object Crate) standard. It allows for the production of FAIR (Findable, Accessible, Interoperable, Reusable) research data objects.

## 🌟 Key Features

*   **Dataverse Integration**: Pull Schema.org and OAI_ORE metadata from Dataverse using persistent IDs (DOIs).
*   **DID Attribution**: Generate a unique OOYDID (via **ODRL Expert**) for every dataset, ensuring its identity is globally resolvable.
*   **Automated File Downloads**: Discover dataset files via OAI_ORE and download them directly into the RO-Crate package.
*   **RO-Crate Packaging**: Convert metadata and downloaded files into the standard RO-Crate format using the `rocrate-py` library.
*   **Provenance (PROV)**: Embed the DID of the asset in the `prov:wasAttributedTo` field for cryptographically verified source identification.
*   **Digital DID Documents**: Create the "digitally signed file" (DID Package) containing the DID's public and private keys, resolvable to JSON in the universal resolver.

## 🛠️ Usage

### Generate an RO-Crate from Dataverse
To fetch metadata and package it into an RO-Crate:

```bash
python3 .gemini/skills/ro-crate-expert/scripts/create_crate.py "https://demo.dataverse.org/dataset.xhtml?persistentId=doi:..." --zip
```

### Inspect Crate for Provenance
Reads a ZIP package, extracts the asset's DID, and resolves its full provenance information via the ODRL expert:

```bash
python3 .gemini/skills/ro-crate-expert/scripts/inspect_crate.py "data/rocrate_${DID}.zip"
```

## 🔒 Security Architecture
Identity management is handled nativesly by the **ODRL Expert**. The resulting package includes an OOYDID that can be resolved via the [Universal Resolver](https://odrl.dev.codata.org/api/did/resolve/).

---
**Reference**: [RO-Crate 1.1 Specification](https://www.researchobject.org/ro-crate/1.1/)
