import json

def open_access_policy(asset, assigner):
    return {
        "@context": "http://www.w3.org/ns/odrl.jsonld",
        "@type": "Offer",
        "uid": "http://example.org/policy/open-access",
        "permission": [{
            "target": asset,
            "action": "use",
            "assigner": assigner
        }]
    }

def restricted_access_policy(asset, assigner, credential_type="github"):
    """
    Example of a policy that requires specific verifiable credentials.
    In OAC, this is often expressed with constraints.
    """
    return {
        "@context": "http://www.w3.org/ns/odrl.jsonld",
        "@type": "Offer",
        "uid": "http://example.org/policy/restricted",
        "permission": [{
            "target": asset,
            "action": "use",
            "assigner": assigner,
            "constraint": [{
                "leftOperand": f"http://odrl.dev.codata.org/voc/vc/{credential_type}",
                "operator": "eq",
                "rightOperand": "verified"
            }]
        }]
    }

def print_template(name, **kwargs):
    if name == "open":
        print(json.dumps(open_access_policy(kwargs.get("asset", "did:oydid:asset"), kwargs.get("assigner", "did:oydid:assigner")), indent=2))
    elif name == "restricted":
        print(json.dumps(restricted_access_policy(kwargs.get("asset", "did:oydid:asset"), kwargs.get("assigner", "did:oydid:assigner"), kwargs.get("vc", "github")), indent=2))
    else:
        print(f"[ODRL Expert] Template '{name}' not found.")

if __name__ == '__main__':
    # Add a simple CLI for templates
    import argparse
    parser = argparse.ArgumentParser(description="ODRL Policy Templates")
    parser.add_argument("name", choices=["open", "restricted"])
    parser.add_argument("--asset", default="did:oydid:asset")
    parser.add_argument("--assigner", default="did:oydid:assigner")
    parser.add_argument("--vc", default="github")
    
    args = parser.parse_args()
    print_template(args.name, asset=args.asset, assigner=args.assigner, vc=args.vc)
