#!/usr/bin/env python3
"""US healthcare providers, specialties, and NPIs. Python, Node.js and cURL clients for the NPI Registry Scraper on Apify, pay per result.

Command-line client for the themineworks/npi-registry-healthcare actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/npi-registry-healthcare/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/npi-registry-healthcare"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--taxonomy-description", help="Provider specialty (for example Dentist, Cardiology, Physical Therapist, Pharmacy)")
    ap.add_argument("--state", help="US state code (for example CA, NY, TX)")
    ap.add_argument("--city", help="City to filter providers by, for example 'Los Angeles' or 'Chicago'")
    ap.add_argument("--postal-code", help="ZIP code (supports wildcard, for example 902*)")
    ap.add_argument("--organization-name", help="Organization/practice name (supports wildcard *), for example 'Mayo Clinic'")
    ap.add_argument("--first-name", help="Individual provider first name, for example 'John'")
    ap.add_argument("--last-name", help="Individual provider last name, for example 'Smith'")
    ap.add_argument("--npi-number", help="Look up a specific 10-digit NPI directly, for example 1234567893")
    ap.add_argument("--max-results", type=int, help="Maximum providers to return (NPI Registry caps a single query at 1,200)")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.taxonomy_description is not None: run_input["taxonomyDescription"] = a.taxonomy_description
    if a.state is not None: run_input["state"] = a.state
    if a.city is not None: run_input["city"] = a.city
    if a.postal_code is not None: run_input["postalCode"] = a.postal_code
    if a.organization_name is not None: run_input["organizationName"] = a.organization_name
    if a.first_name is not None: run_input["firstName"] = a.first_name
    if a.last_name is not None: run_input["lastName"] = a.last_name
    if a.npi_number is not None: run_input["npiNumber"] = a.npi_number
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
