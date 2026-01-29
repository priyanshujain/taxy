# Taxy - India Tax Regime Comparison System

Compare **Old Tax Regime vs New Tax Regime** for Indian taxpayers. Calculate effective tax liability under both regimes and get recommendations on which regime saves you more tax.

**Assessment Year:** 2026-27 (Financial Year: 2025-26)

## Features

- Complete salary structure support (Basic, HRA, LTA, Special Allowance, Bonus, etc.)
- All Section 10 exemptions (HRA, LTA, Driver Salary, Conveyance, Gratuity, Leave Encashment)
- All Chapter VI-A deductions (80C, 80CCD, 80D, 80E, 80G, 80TTA, etc.)
- Section 24 home loan interest deduction
- Senior citizen support (60-80 and 80+ with different slabs)
- HRA calculator with metro/non-metro logic
- Surcharge and cess calculation
- Side-by-side comparison with recommendation

## Tax Slabs (FY 2025-26)

### New Tax Regime (Default)
| Income Slab | Tax Rate |
|-------------|----------|
| Up to ₹4,00,000 | Nil |
| ₹4,00,001 - ₹8,00,000 | 5% |
| ₹8,00,001 - ₹12,00,000 | 10% |
| ₹12,00,001 - ₹16,00,000 | 15% |
| ₹16,00,001 - ₹20,00,000 | 20% |
| ₹20,00,001 - ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

**Rebate:** ₹60,000 if income ≤ ₹12,00,000
**Standard Deduction:** ₹75,000

### Old Tax Regime (Below 60 years)
| Income Slab | Tax Rate |
|-------------|----------|
| Up to ₹2,50,000 | Nil |
| ₹2,50,001 - ₹5,00,000 | 5% |
| ₹5,00,001 - ₹10,00,000 | 20% |
| Above ₹10,00,000 | 30% |

**Rebate:** ₹12,500 if income ≤ ₹5,00,000
**Standard Deduction:** ₹50,000

## Installation

```bash
# Clone the repository
git clone https://github.com/pjthepooh/taxy.git
cd taxy

# Install dependencies using uv
uv sync

# Or using pip
pip install python-dotenv
```

## Usage

1. **Copy the example configuration:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your salary details:**
   ```bash
   code .env  # or vim .env
   ```

3. **Run the comparison:**
   ```bash
   uv run python main.py
   ```

## Configuration

All configuration is done via the `.env` file. See `.env.example` for detailed documentation of each variable.

### Key Variables

| Variable | Description |
|----------|-------------|
| `BASIC_SALARY` | Annual basic salary |
| `HRA_RECEIVED` | House Rent Allowance from employer |
| `RENT_PAID_ANNUAL` | Actual rent paid per year |
| `CITY_TYPE` | `metro` or `non_metro` for HRA calculation |
| `BONUS` | Annual bonus/variable pay |
| `EPF_CONTRIBUTION_EMPLOYEE` | Your EPF contribution (80C) |
| `ELSS_INVESTMENT` | Tax saving mutual funds (80C) |
| `HEALTH_INSURANCE_SELF` | Health insurance premium (80D) |

### Deductions Available

**Old Regime Only:**
- Section 80C (₹1.5L limit) - EPF, PPF, ELSS, LIC, NSC, etc.
- Section 80CCD(1B) - Additional NPS (₹50K)
- Section 80D - Health Insurance
- Section 80E - Education Loan Interest
- Section 80G - Donations
- Section 80TTA/TTB - Savings Interest
- Section 24 - Home Loan Interest (Self-occupied)
- HRA, LTA exemptions

**Both Regimes:**
- Section 80CCD(2) - Employer NPS contribution (14% of Basic+DA)
- Standard Deduction (₹50K old / ₹75K new)
- Section 24 - Home Loan Interest (Let-out property)


## Project Structure

```
taxy/
├── .env                 # Your personal config (gitignored)
├── .env.example         # Template with documentation
├── main.py              # CLI interface
├── tax_calculator.py    # Core calculation logic
├── variables.py         # Loads config from .env
├── pyproject.toml       # Project dependencies
└── README.md
```

## Disclaimer

This tool is for educational and planning purposes only. Tax laws change frequently. Always consult a qualified tax professional or CA for actual tax filing. The author is not responsible for any errors in calculation or changes in tax laws.

## License

MIT
