# NFC Creator - Template Setup Guide

## Overview

The NFC Creator skill does **NOT include an embedded Excel template** because templates are typically 50-100MB+ in size and contain sensitive pricing data.

Instead, the skill works with any Excel template you provide, making it flexible for different clients, hubs, and configurations.

---

## Template Requirements

Your template must be a **New Contract Form** Excel file with these sheets:

### Required Sheets:
1. **ADMIN INFO** (Sheet 2)
   - Client information
   - Project details
   - Contact information
   - Sales Bonus configuration
   
2. **BUDGET** (Sheet 3)
   - Consultant staffing
   - Rates and billing
   - Margin calculations

3. **a. ADR_Target** (Sheet 7)
   - Pricing reference table
   - Office × Grade × BU combinations
   - Daily/Hourly rates
   - **Note**: Can be very large (50-100MB+ for complete data)

4. **b. data** (Sheet 8)
   - Grade mapping table
   - Maps full grade names to abbreviations
   - Example: "Senior Consultant" → "SC"

### Optional Sheets:
- c. forex
- d. grade
- Recalculated Rate
- List of level
- Operating Model
- EMAIL
- BUDGET EXP
- ADMIN INFO EXP
- And others...

---

## How to Use

### Option 1: Command Line with Template Path

```bash
export NFC_TEMPLATE_PATH=/path/to/your/template.xlsm
python nfc_main.py
```

### Option 2: Pass Template as Argument

```bash
python nfc_main.py /path/to/your/template.xlsm
```

### Option 3: Set Environment Variable (Persistent)

```bash
# Linux/Mac
echo "export NFC_TEMPLATE_PATH=/path/to/template.xlsm" >> ~/.bashrc
source ~/.bashrc

# Windows (PowerShell)
[Environment]::SetEnvironmentVariable("NFC_TEMPLATE_PATH", "C:\path\to\template.xlsm", "User")
```

---

## Getting a Template

### Where to Find Templates:

1. **From SIA Network Drive**
   - `/shared/sia-partners/templates/contracts/`
   - Ask your manager or template owner

2. **From Recent Project**
   - Use an existing NCF file from a similar project
   - Example: `NCF_25-01_ClientName.xlsm`

3. **Reference Templates**
   - `New_Contract_Form_FIM_BeNeLux_ME_July25.xlsm`
   - `New_Contract_Form_Template_Generic.xlsm`

4. **Request from Admin**
   - Contact your local admin team
   - They maintain the master templates

---

## Troubleshooting Template Issues

### Error: "Template not found"

```
❌ Erreur: Template non trouvé: /path/to/template.xlsm
```

**Solution:**
1. Check the path is correct
2. Verify the file exists: `ls -la /path/to/template.xlsm`
3. Ensure you have read permissions: `chmod +r /path/to/template.xlsm`

### Error: "Missing ADR" in Generated NFC

**Cause:** The `a. ADR_Target` sheet doesn't contain the grade/office/BU combination needed.

**Solution:**
1. Check `b. data` sheet has the grade you're using
2. Verify `a. ADR_Target` has matching entries
3. Update the template with correct pricing data

Example: If adding "Senior Consultant" from "Paris" for "FPR" BU:
- `b. data` must have: "Senior Consultant" → "SC"
- `a. ADR_Target` must have: "ParisSCFPR" entry with pricing

### Error: "Template is invalid/corrupted"

**Solution:**
1. Try opening the template in Excel/LibreOffice
2. Save it again to ensure it's valid
3. Check file size - if > 100MB, it may have too much data

---

## Template Customization

### Modifying Grade Mapping (b. data)

The `b. data` sheet maps full grade names to abbreviations:

| Column A (Input)       | Column B (Output) |
|------------------------|-------------------|
| Senior Partner         | SP                |
| Partner                | P                 |
| Associate Partner      | AP                |
| Senior Consultant      | SC                |
| Consultant             | C                 |
| ... (add your grades)  | ...               |

**To add a new grade:**
1. Open the template in Excel
2. Go to `b. data` sheet
3. Add row: `Your Grade Name` | `ABBREVIATION`
4. Save the file

### Modifying Pricing (a. ADR_Target)

The `a. ADR_Target` sheet is a **lookup table** with this structure:

| Column L (Key)    | Column M (Daily ADR) | Column N (Daily Cost) | ... |
|-------------------|---------------------|----------------------|-----|
| ParisSPC&L        | 1500                | 750                  |     |
| ParisPC&L         | 1200                | 600                  |     |
| ParisSCC&L        | 950                 | 475                  |     |

Format: `OFFICE + GRADE_ABBREV + BU`

Example: `"Paris" + "SC" + "FPR"` = `"ParisSCFPR"`

**To add pricing:**
1. Open the template
2. Go to `a. ADR_Target` sheet
3. Add row with key and pricing
4. Save the file

---

## Best Practices

✅ **Do:**
- Store templates in version control
- Keep one master template per hub/market
- Update pricing regularly
- Document changes to templates
- Test templates with sample NCF creation

❌ **Don't:**
- Embed templates in the skill code
- Use outdated pricing data
- Share templates without review
- Modify critical formulas in ADMIN INFO or BUDGET
- Store client-specific sensitive data

---

## Performance Tips

### For Large Templates (>50MB):

1. **Use a reduced version for testing**
   - Create a small template with sample data
   - Use full template only for final generation

2. **Optimize a. ADR_Target**
   - Remove unused Office/Grade/BU combinations
   - Archive old pricing data to separate sheet

3. **Store templates locally**
   - Cache templates on your machine
   - Avoid network delays

---

## Security Considerations

- Templates may contain **pricing and margin data** - keep secure
- Don't share templates with external parties
- Use version control with proper access controls
- Mark sensitive templates as confidential

---

## Support

For template-related issues:
1. Check this guide first
2. Verify with template owner
3. Ask your admin team
4. Contact SIA Partners support

---

**Questions? Check the template setup guide or ask your team!**
