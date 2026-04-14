# Dataset Scripts

Scripts for generating the seed data used by CivicLens.

## Files

| File | What it does |
|---|---|
| `prepare_fcc_dataset.py` | Generates `fcc_dataset.json` with amendments, comments, users, and vote data |
| `fcc_dataset.json` | Output JSON — also needs to be copied to `civiclens-backend/src/main/resources/` |

## What's in the Dataset

- **7 amendments** based on real U.S. federal regulatory topics (net neutrality, clean air, broadband, healthcare privacy, etc.)
- **~220 comments** with stance (support/oppose/neutral) and sentiment labels
- **20 synthetic users** with different personas
- **Vote counts** generated based on stance and sentiment

## How to Regenerate

If you change anything in the Python script:

```bash
cd scripts
python prepare_fcc_dataset.py
copy fcc_dataset.json ..\civiclens-backend\src\main\resources\fcc_dataset.json
```

Then restart the backend with a fresh database so the seeder runs again.

## Adding New Data

All data is defined as Python dicts inside `prepare_fcc_dataset.py`. To add a new amendment, follow the same structure as the existing ones and add it to the `all_amendments` list in `main()`. Valid categories: `HEALTHCARE`, `EDUCATION`, `INFRASTRUCTURE`, `DIGITAL_PRIVACY`, `ENVIRONMENT`, `TAXATION`, `DEFENSE`, `OTHER`.

