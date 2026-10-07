# NPI Registry Scraper: US Healthcare Provider Data (No API

Look up US healthcare providers from the CMS NPI Registry by name, specialty, city, or state. Returns NPI, credentials, specialty, license, and practice address. The official provider directory, no API key required.

**Run it on Apify:** [apify.com/themineworks/npi-registry-healthcare](https://apify.com/themineworks/npi-registry-healthcare)
**Docs, FAQ and pricing:** [themineworks.com/actors/npi-registry-healthcare](https://themineworks.com/actors/npi-registry-healthcare/)

**Price:** From $0.60 per 1,000 providers on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Search 8M+ US healthcare providers
* NPI, credentials, specialty, and license data
* Filter by name, specialty, city, or state
* Official CMS NPI Registry source
* Empty lookups are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/npi-registry-healthcare").call(run_input={
    "taxonomyDescription": "Dentist",
    "state": "CA",
    "city": "Los Angeles",
    "postalCode": "902*"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/npi-registry-healthcare').call({
    "taxonomyDescription": "Dentist",
    "state": "CA",
    "city": "Los Angeles",
    "postalCode": "902*"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~npi-registry-healthcare/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"taxonomyDescription": "Dentist", "state": "CA", "city": "Los Angeles", "postalCode": "902*"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 npi_registry_scraper.py --token YOUR_APIFY_TOKEN --taxonomy-description "Dentist" --state "CA" --city "Los Angeles" --postal-code "902*"
node npi_registry_scraper.mjs --token YOUR_APIFY_TOKEN --taxonomy-description "Dentist" --state "CA" --city "Los Angeles" --postal-code "902*"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `taxonomyDescription` | string |  | Provider specialty (for example Dentist, Cardiology, Physical Therapist, Pharmacy) |
| `state` | string |  | US state code (for example CA, NY, TX) |
| `city` | string |  | City to filter providers by, for example "Los Angeles" or "Chicago" |
| `postalCode` | string |  | ZIP code (supports wildcard, for example 902*) |
| `organizationName` | string |  | Organization/practice name (supports wildcard *), for example "Mayo Clinic" |
| `firstName` | string |  | Individual provider first name, for example "John" |
| `lastName` | string |  | Individual provider last name, for example "Smith" |
| `npiNumber` | string |  | Look up a specific 10-digit NPI directly, for example 1234567893 |
| `maxResults` | integer | `200` | Maximum providers to return (NPI Registry caps a single query at 1,200) |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `npi` | string | National Provider Identifier |
| `type` | string | Provider type: Individual or Organization |
| `name` | string | Provider name (full name for individuals, org name for organizations) |
| `credential` | string | Professional credentials (MD, DO, RN, etc.) |
| `status` | string | NPI status (Active or inactive) |
| `primary_specialty` | string | Primary specialty description |
| `taxonomy_code` | string | Primary taxonomy classification code |
| `license` | string | License number |
| `license_state` | string | State of licensure |
| `address` | string | Practice location street address |
| `city` | string | Practice location city |
| `state` | string | Practice location state |
| `postal_code` | string | Practice location postal code |
| `phone` | string | Practice location phone number |
| `enumeration_date` | string | Date NPI was issued |
| `last_updated` | string | Date record was last updated |
| `scraped_at` | string | Timestamp when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/npi-registry-healthcare
```

## FAQ

### What is an NPI number?

A National Provider Identifier is a unique 10-digit number assigned to every US healthcare provider. It is required for billing Medicare, Medicaid, and most private insurers. Every active US doctor, hospital, and clinic has one.

### Is the NPI registry free to access?

Yes. The NPPES (National Plan and Provider Enumeration System) registry is maintained by CMS and provides a free REST API with no authentication required.

### What fields are available per provider?

NPI number, enumeration type (individual vs organization), legal name, credential, primary taxonomy (specialty), all practice addresses, phone numbers, and authorized official information for organizations.

### Can I search by medical specialty?

Yes. The taxonomy_description parameter accepts specialty names like Cardiology, Family Medicine, or Orthopedic Surgery. Multiple specialties can be queried in separate calls and combined.

### What is the difference between Type 1 and Type 2 NPI?

Type 1 is for individual healthcare providers (a doctor, dentist, or therapist). Type 2 is for organizations (a hospital, clinic, or group practice). Both are searchable via the same API.

### How much does the NPI Registry Scraper cost?

From $0.60 per 1,000 providers on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [India Gov Data](https://themineworks.com/actors/india-data-gov-scraper/): Trade, prices, and thousands of datasets from data.gov.in
* [CourtListener Scraper](https://themineworks.com/actors/courtlistener-court-records/): US court opinions, dockets, and case law as structured JSON
* [Socrata Open Data](https://themineworks.com/actors/socrata-open-data/): Any government data portal: CDC, HHS, NYC, Texas, and hundreds more

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
