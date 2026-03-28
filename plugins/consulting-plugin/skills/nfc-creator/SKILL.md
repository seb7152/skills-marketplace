---
name: nfc-creator
description: Create and configure New Contract Forms (NFC) for SIA Partners. Interactive questionnaire for client info, project details, consultant staffing, and Sales Bonus configuration. Generates complete Excel files with pre-filled defaults. **Requires an Excel template file to be provided.**
---

# NFC Creator

Create **New Contract Forms (NFC)** - Excel files with automated client data, consultant staffing, and margin calculations.

---

## ⚠️ Important: Template Required

**This skill does NOT include an embedded template** (too large ~60MB). You must provide an Excel template file when using this skill.

### Where to get a template:
1. Download from your network drive or shared storage
2. Use an existing NFC file from a similar project
3. Example templates: `New_Contract_Form_FIM_BeNeLux_ME_July25.xlsm` or similar

### How to provide the template:
```bash
python nfc_main.py /path/to/your/template.xlsm
```

Or set environment variable:
```bash
export NFC_TEMPLATE_PATH=/path/to/your/template.xlsm
python nfc_main.py
```

---

## Quick Start

Just say to Claude:

```
"I need to create an NFC for [Client Name] using this template [upload file or path]"
```

Claude will:
1. Ask for required info (client, project, start date)
2. Offer to add Sales Bonus (optional)
3. Offer to add consultants (optional)
4. Generate an Excel file based on your template
5. Show a summary

---

## What Gets Pre-filled

These values are automatically filled in every NFC:

- **Hub**: FIM
- **Billing Company**: Sia Partners France
- **Billing BU**: FPR
- **Currency**: EUR
- **Basis**: Schedule (Fixed Fee)
- **Minimum Time**: Half day
- **Sales Manager**: Sébastien Grandperret
- **PM**: Sébastien Grandperret
- **Sales Bonus Max**: 3%

---

## Required Information

When creating an NFC, you'll be asked for:

- **Client Name** (required)
- **Project Name** (required)
- **Start Date** (required, format: DD/MM/YYYY)

---

## Optional: Sales Bonus

Configure who gets how much (max 3% total):
- Up to 2 beneficiaries
- Split between Originated (50%) and Managed (50%)
- Format: 0.01 for 1%, 0.005 for 0.5%, etc.

Example:
```
Sébastien Grandperret: 1% Originated + 1% Managed = 2%
Paul Dubois:          0.5% Originated + 0.5% Managed = 1%
Total: 3% ✓
```

---

## Optional: Add Consultants

For each consultant, provide:

- **Name** (required)
- **Grade** (required - must match your template's grade list)
- **Billable Days** (required, 0.5-365)
- **Daily Rate** (required, EUR)
- **Office** (optional, default: Paris)
- **Work Type** (optional, default: In the office)

---

## Reference Documents

For detailed field mappings and configurations, see:

- **references/ADMIN_INFO_FIELDS.md** - All ADMIN INFO fields explained
- **references/BUDGET_SALES_BONUS.md** - Budget and Sales Bonus details

---

## Output

You get an Excel file with:

- ✅ All your data pre-filled from your template
- ✅ All SIA defaults applied
- ✅ Consultant staffing configured
- ✅ Margins calculated (if template includes them)
- ✅ Ready to validate and send

File naming: `NCF_YY-MM_ClientName.xlsm`

---

## Examples

### With Template File
```
"Create NFC for Acme Corp, project: Digital Transformation, 
starts 01/04/2026. Template: New_Contract_Form_FIM.xlsm"
```

### With Consultants
```
"NFC for TechCorp, Cloud Migration, 15/04/2026 using FIM template.
Add: Sophie Martin (Senior Consultant, 65 days, 950€),
Marc Dupont (Consultant, 50 days, 800€)"
```

---

## Template Structure

Your template should include:

- **ADMIN INFO** sheet - Client and project information
- **BUDGET** sheet - Consultant staffing and rates
- **a. ADR_Target** sheet - Pricing reference table (lookup source)
- **b. data** sheet - Grade mapping table

Grades in your template (examples):
- Senior Consultant
- Consultant
- Manager
- Senior Manager
- Engagement Director
- etc.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing ADR" in budget | Check that `b. data` sheet has grade mappings and `a. ADR_Target` has matching rates |
| Template not found | Verify file path is correct and accessible |
| Date format error | Use DD/MM/YYYY format exactly |

---

## Tips

✅ Use interactive mode - Claude will ask what you need
✅ Reference documents have all field details  
✅ Pre-filled defaults save time
✅ Files are generated immediately
✅ Test with a sample template first to validate your setup

---

**Ready to create an NFC? Upload your template and let's go!** 🚀
