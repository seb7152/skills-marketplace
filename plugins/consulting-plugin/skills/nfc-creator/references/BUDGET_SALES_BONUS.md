# Budget & Sales Bonus Reference

## Consultant Staffing (BUDGET Sheet - Row 26+)

| Column | Field | Required | Notes |
|--------|-------|----------|-------|
| B | Name | ✓ | Sophie Martin |
| C | Relation Type | ✗ | **Pré-remplie par formule - NE PAS MODIFIER** |
| E | Grade | ✓ | Senior Consultant |
| F | Office | ✓ | Paris |
| H | Work Type | ✓ | In the office |
| I | Billable Days | ✓ | 65 |
| R | Daily Rate (TJ) | ✓ | 950 |

## Available Grades (9)

Senior Manager, Manager, Senior Consultant, Consultant, Junior, SME Director, Engagement Director, Managing Director, Senior Industry Expert

## Sales Bonus Configuration (Lines 46-47)

Maximum: 3% total (split between Originated 50% + Managed 50%)

| Line | Cell | Field | Type | Range |
|------|------|-------|------|-------|
| 46 | C46 | Beneficiary 1 Email (Orig) | Email | Required |
| 46 | F46 | Percentage (Orig) | Decimal | 0.00-1.00 |
| 46 | G46 | Beneficiary 1 Email (Mgd) | Email | Required |
| 46 | J46 | Percentage (Mgd) | Decimal | 0.00-1.00 |
| 47 | C47 | Beneficiary 2 Email (Orig) | Email | Optional |
| 47 | F47 | Percentage (Orig) | Decimal | 0.00-1.00 |
| 47 | G47 | Beneficiary 2 Email (Mgd) | Email | Optional |
| 47 | J47 | Percentage (Mgd) | Decimal | 0.00-1.00 |

### Format Note
Use decimals: 0.01 for 1%, 0.005 for 0.5%, etc.
