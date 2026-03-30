---
name: unf
description: Universal Numeric Fingerprint (UNF) generator. Computes a format-agnostic, system-independent hash for data vectors, dataframes, and files based on the Dataverse UNF v6 specification.
---

# ♾️ UNF Skill

The **UNF (Universal Numeric Fingerprint)** skill provides a robust mechanism for generating consistent data identifiers. Unlike traditional file hashes (like MD5 or SHA-256), a UNF is **format-agnostic**—meaning the same data values will produce the same hash regardless of whether they are stored in CSV, Parquet, SAS, or Stata.

## 🌟 Key Features

1.  **Atomic Hashing**: Compute fingerprints for single values or character strings.
2.  **Vector Hashing**: Fingerprint entire data columns (Polars Series).
3.  **Format Invariance**: Identical data in different file formats (e.g., CSV vs. Parquet) yields the same UNF.
4.  **Column-Order Invariance**: Dataframes with reordered columns produce the same hash.
5.  **Dataverse Alignment**: Designed for parity with the canonical Dataverse UNF implementation.

## 🛠️ Components

- `unf_hash.py`: CLI tool to compute a UNF for a string or file.
- `dartfx-unf`: High-performance Python implementation using the Polars engine.

## 🚀 Usage

### Hash a simple string
```bash
python3 .gemini/skills/unf/scripts/unf_hash.py "Data for fingerprinting"
```

### Hash a data file (CSV, Parquet, etc.)
```bash
python3 .gemini/skills/unf/scripts/unf_hash.py data/dataset.csv
```

### Get a detailed JSON report
```bash
python3 .gemini/skills/unf/scripts/unf_hash.py --json data/dataset.parquet
```

## 📐 Specification
- **Version**: UNF v6
- **Reference**: [Dataverse UNF v6 Guide](https://guides.dataverse.org/en/latest/developers/unf/unf-v6.html)
- **Engine**: [dartfx-unf](https://github.com/DataArtifex/dartfx-unf)
