import json
import sys
import os

def create_croissant_jsonld(metadata):
    """
    Creates a valid Croissant JSON-LD structure based on provided metadata.
    """
    context = {
        "@language": "en",
        "@vocab": "https://schema.org/",
        "cr": "http://mlcommons.org/croissant/",
        "sc": "https://schema.org/",
        "dct": "http://purl.org/dc/terms/",
        "conformsTo": "dct:conformsTo",
        "recordSet": "cr:recordSet",
        "field": "cr:field",
        "source": "cr:source",
        "fileObject": "cr:fileObject",
        "fileSet": "cr:fileSet",
        "dataType": { "@id": "cr:dataType", "@type": "@id" }
    }

    distribution_list = []
    record_set_list = []

    dataset = {
        "@context": context,
        "@type": "sc:Dataset",
        "name": metadata.get("name", "Untitled Dataset"),
        "description": metadata.get("description", "No description provided."),
        "url": metadata.get("url", "https://example.com/dataset"),
        "license": metadata.get("license", "CC-BY-4.0"),
        "dct:conformsTo": "http://mlcommons.org/croissant/1.0",
        "distribution": distribution_list,
        "recordSet": record_set_list
    }

    # Handle distribution
    for dist in metadata.get("distribution", []):
        dist_type = dist.get("type", "FileObject")
        if dist_type == "FileObject":
            distribution_list.append({
                "@type": "cr:FileObject",
                "name": dist.get("name"),
                "contentUrl": dist.get("contentUrl"),
                "encodingFormat": dist.get("encodingFormat"),
                "sha256": dist.get("sha256")
            })
        elif dist_type == "FileSet":
            distribution_list.append({
                "@type": "cr:FileSet",
                "name": dist.get("name"),
                "containedIn": dist.get("containedIn"),
                "encodingFormat": dist.get("encodingFormat"),
                "includes": dist.get("includes")
            })

    # Handle recordSets
    for rs in metadata.get("recordSet", []):
        fields_list = []
        record_set = {
            "@type": "cr:RecordSet",
            "name": rs.get("name"),
            "field": fields_list
        }
        for f in rs.get("field", []):
            field_source = {
                "fileObject": { "@id": f"#{f.get('source_file')}" } if f.get('source_file') else None,
                "fileSet": { "@id": f"#{f.get('source_set')}" } if f.get('source_set') else None,
                "field": f.get("source_field"),
                "extract": {
                    "column": f.get("extract_column"),
                    "fileProperty": f.get("extract_property")
                }
            }
            # Clean up None values in source
            clean_source = {k: v for k, v in field_source.items() if v is not None}
            if "extract" in clean_source:
                extract_dict = clean_source["extract"]
                if isinstance(extract_dict, dict):
                    clean_extract = {k: v for k, v in extract_dict.items() if v is not None}
                    if clean_extract:
                        clean_source["extract"] = clean_extract
                    else:
                        clean_source.pop("extract", None)
            
            field = {
                "@type": "cr:Field",
                "name": f.get("name"),
                "dataType": f.get("dataType"),
                "source": clean_source
            }
            
            fields_list.append(field)
        
        record_set_list.append(record_set)

    return dataset

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 serialize.py <METADATA_JSON_FILE> [OUTPUT_FILE]")
        # Example metadata structure
        example = {
            "name": "Example Dataset",
            "description": "A simple example",
            "url": "https://example.com",
            "distribution": [
                {"name": "data-file", "contentUrl": "data.csv", "encodingFormat": "text/csv"}
            ],
            "recordSet": [
                {
                    "name": "main",
                    "field": [
                        {"name": "label", "dataType": "sc:Text", "source_file": "data-file", "extract_column": "label"}
                    ]
                }
            ]
        }
        print("\nExample Input JSON:")
        print(json.dumps(example, indent=2))
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = "data/croissant"
    os.makedirs(output_dir, exist_ok=True)
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
        # If user provides a filename without a path, put it in the default dir
        if not os.path.dirname(output_file):
            output_file = os.path.join(output_dir, output_file)
    else:
        output_file = os.path.join(output_dir, "dataset-croissant.json")

    try:
        with open(input_file, 'r') as f:
            metadata = json.load(f)
        
        croissant_data = create_croissant_jsonld(metadata)
        
        with open(output_file, 'w') as f:
            json.dump(croissant_data, f, indent=2)
            
        print(f"Successfully serialized Croissant metadata to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
