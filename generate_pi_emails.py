import argparse
import json
import pandas as pd
import re
from pathlib import Path


def create_domain(institution: str) -> str:
    """Convert institution name to a simple email domain."""
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", institution).lower()
    return f"{cleaned}.edu" if cleaned else "example.edu"


def generate_email_permutations(first_name: str, last_name: str, domain: str) -> list[str]:
    """Return common academic email permutations."""
    first = first_name.lower()
    last = last_name.lower()
    initial = first[0] if first else ""
    return [
        f"{first}.{last}@{domain}",
        f"{initial}{last}@{domain}",
        f"{initial}.{last}@{domain}",
    ]


def placeholder_validate_email(email: str) -> bool:
    """Placeholder for future email validation."""
    # TODO: integrate with Hunter API or SMTP check
    return True


def main(json_path: Path, output_csv: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    projects = data if isinstance(data, list) else data.get("results", [])
    for project in projects:
        title = project.get("projectTitle", "")
        url = project.get("projectDetailUrl", "")
        org = project.get("organization", {}).get("org_name", "")
        domain = create_domain(org)
        for pi in project.get("principalInvestigators", []):
            full_name = pi.get("fullName", "")
            first = pi.get("first_name", "")
            last = pi.get("last_name", "")
            emails = generate_email_permutations(first, last, domain)
            for email in emails:
                rows.append({
                    "Full Name": full_name,
                    "Institution": org,
                    "Project Title": title,
                    "Project Detail URL": url,
                    "Email": email,
                })

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"Saved {len(df)} email permutations to {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PI email permutations from NIH JSON data")
    parser.add_argument("json_file", type=Path, help="Path to NIH JSON file")
    parser.add_argument("--output", type=Path, default=Path("nih_pi_emails.csv"), help="CSV output path")
    args = parser.parse_args()
    main(args.json_file, args.output)
