import json
import sys
import os

# Import NLP Expert logic if available
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../nlp_expert/scripts'))
    from extract_entities import extract_entities
except ImportError:
    extract_entities = None

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

    creator_list = metadata.get("creator", [])
    if not isinstance(creator_list, list):
        creator_list = [creator_list]
        
    publisher_list = metadata.get("publisher", [])
    if not isinstance(publisher_list, list):
        publisher_list = [publisher_list]
        
    spatial_list = metadata.get("spatialCoverage", [])
    if not isinstance(spatial_list, list):
        spatial_list = [spatial_list]
        
    temporal_list = metadata.get("temporalCoverage", [])
    if not isinstance(temporal_list, list):
        temporal_list = [temporal_list]

    dataset = {
        "@context": context,
        "@type": "sc:Dataset",
        "name": metadata.get("name", "Untitled Dataset"),
        "description": metadata.get("description", "No description provided."),
        "url": metadata.get("url", "https://example.com/dataset"),
        "license": metadata.get("license", "CC-BY-4.0"),
        "dct:conformsTo": "http://mlcommons.org/croissant/1.0",
        "distribution": distribution_list,
        "recordSet": record_set_list,
        "creator": creator_list,
        "publisher": publisher_list,
        "spatialCoverage": spatial_list,
        "temporalCoverage": temporal_list
    }

    # Enrich with NLP if requested
    if metadata.get("apply_nlp") and extract_entities:
        print(f"> Applying NLP analysis for: {dataset['name']}")
        entities = extract_entities(f"{dataset['name']} {dataset['description']}")
        if entities:
            # Map Schema.org entities to Dataset fields
            elements = entities.get("itemListElement", [])
            for el in elements:
                # Handle cases where el is a ListItem or direct entity
                item = el.get("item") if isinstance(el.get("item"), dict) else el
                etype = item.get("@type")
                ename = item.get("name")
                
                if etype in ["Person", "Organization", "CollegeOrUniversity", "EducationalOrganization"]:
                    role_type = "sc:Person" if etype == "Person" else "sc:Organization"
                    if ename not in [c.get("name") if isinstance(c, dict) else c for c in creator_list]:
                        creator_list.append({"@type": role_type, "name": ename})
                elif etype in ["Place", "City", "Country"]:
                    if ename not in spatial_list:
                        spatial_list.append(ename)
                elif etype in ["Event", "Date", "Duration"]:
                    date_val = item.get("startDate") or item.get("name")
                    if date_val not in temporal_list:
                        temporal_list.append(date_val)

    # Clean up empty optional fields
    if not creator_list: dataset.pop("creator", None)
    if not publisher_list: dataset.pop("publisher", None)
    if not spatial_list: dataset.pop("spatialCoverage", None)
    if not temporal_list: dataset.pop("temporalCoverage", None)

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
    
    apply_nlp = "--nlp" in sys.argv
    
    # Filter out flags from potential output_file argument
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    
    if args:
        output_file = args[0]
        # If user provides a filename without a path, put it in the default dir
        if not os.path.dirname(output_file):
            output_file = os.path.join(output_dir, output_file)
    else:
        output_file = os.path.join(output_dir, "dataset-croissant.json")

    try:
        with open(input_file, 'r') as f:
            metadata = json.load(f)
        
        if apply_nlp:
            metadata["apply_nlp"] = True
            
        croissant_data = create_croissant_jsonld(metadata)
        
        with open(output_file, 'w') as f:
            json.dump(croissant_data, f, indent=2)
            
        print(f"Successfully serialized Croissant metadata to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
