#!/usr/bin/env python3
"""
India Tax Regime Comparison System - CLI Interface
Assessment Year: 2026-27 (Financial Year: 2025-26)

Run this file to compare tax under Old vs New Tax Regime.
"""

from tax_calculator import compare_regimes, TaxBreakdown, LIMITS
import variables as v


# ANSI Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def format_currency(amount: float) -> str:
    """Format amount in Indian currency style."""
    if amount < 0:
        return f"-₹{abs(amount):,.0f}"
    return f"₹{amount:,.0f}"


def format_lakhs(amount: float) -> str:
    """Format amount in lakhs."""
    lakhs = amount / 100000
    return f"₹{lakhs:.2f}L"


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{title.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.END}")


def print_section(title: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}┌{'─' * 68}┐{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}│ {title:<66} │{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}└{'─' * 68}┘{Colors.END}")


def print_row(label: str, old_value: str, new_value: str, highlight: bool = False):
    """Print a comparison row."""
    color = Colors.YELLOW if highlight else ''
    end = Colors.END if highlight else ''
    print(f"  {color}{label:<40} {old_value:>13} {new_value:>13}{end}")


def print_single_row(label: str, value: str):
    """Print a single value row."""
    print(f"  {label:<40} {value:>27}")


def print_dict_rows(title: str, old_dict: dict, new_dict: dict):
    """Print dictionary items as rows."""
    all_keys = set(old_dict.keys()) | set(new_dict.keys())
    if not all_keys:
        return

    print(f"\n  {Colors.UNDERLINE}{title}{Colors.END}")
    for key in sorted(all_keys):
        old_val = format_currency(old_dict.get(key, 0)) if key in old_dict else "-"
        new_val = format_currency(new_dict.get(key, 0)) if key in new_dict else "-"
        print(f"    {key:<38} {old_val:>13} {new_val:>13}")


def print_comparison_table(old: TaxBreakdown, new: TaxBreakdown):
    """Print detailed comparison table."""

    print_header("INDIA TAX REGIME COMPARISON")
    print(f"{Colors.CYAN}Assessment Year: 2026-27 (Financial Year: 2025-26){Colors.END}")
    print(f"{Colors.CYAN}Age Category: {v.age_category.replace('_', ' ').title()}{Colors.END}")

    # Column Headers
    print_section("COMPARISON")
    print(f"\n  {'PARTICULARS':<40} {'OLD REGIME':>13} {'NEW REGIME':>13}")
    print(f"  {'─' * 40} {'─' * 13} {'─' * 13}")

    # Gross Salary
    print_row("Gross Salary",
              format_currency(old.gross_salary),
              format_currency(new.gross_salary))

    # Exemptions
    print_dict_rows("Section 10 Exemptions", old.exemptions, new.exemptions)
    print_row("Total Exemptions",
              format_currency(old.total_exemptions),
              format_currency(new.total_exemptions),
              highlight=True)

    # Income from Salary
    print(f"\n  {'─' * 66}")
    print_row("Income from Salary",
              format_currency(old.income_from_salary),
              format_currency(new.income_from_salary))

    # Section 16 Deductions
    print_dict_rows("Section 16 Deductions", old.section_16_deductions, new.section_16_deductions)
    print_row("Total Section 16",
              format_currency(old.total_section_16),
              format_currency(new.total_section_16),
              highlight=True)

    # Net Salary Income
    print(f"\n  {'─' * 66}")
    print_row("Net Salary Income",
              format_currency(old.net_salary_income),
              format_currency(new.net_salary_income))

    # House Property Income
    if old.income_from_house_property != 0 or new.income_from_house_property != 0:
        print_row("Income from House Property",
                  format_currency(old.income_from_house_property),
                  format_currency(new.income_from_house_property))

    # Other Income
    if old.other_income > 0 or new.other_income > 0:
        print_row("Other Income",
                  format_currency(old.other_income),
                  format_currency(new.other_income))

    # Gross Total Income
    print(f"\n  {'─' * 66}")
    print_row("GROSS TOTAL INCOME",
              format_currency(old.gross_total_income),
              format_currency(new.gross_total_income),
              highlight=True)

    # Chapter VI-A Deductions
    print_dict_rows("Chapter VI-A Deductions", old.chapter_via_deductions, new.chapter_via_deductions)
    print_row("Total Chapter VI-A",
              format_currency(old.total_chapter_via),
              format_currency(new.total_chapter_via),
              highlight=True)

    # Taxable Income
    print(f"\n  {'─' * 66}")
    print_row("TAXABLE INCOME",
              format_currency(old.taxable_income),
              format_currency(new.taxable_income),
              highlight=True)

    # Tax Calculation
    print_section("TAX CALCULATION")
    print(f"\n  {'PARTICULARS':<40} {'OLD REGIME':>13} {'NEW REGIME':>13}")
    print(f"  {'─' * 40} {'─' * 13} {'─' * 13}")

    print_row("Tax on Income",
              format_currency(old.tax_on_income),
              format_currency(new.tax_on_income))

    print_row("Less: Rebate u/s 87A",
              format_currency(old.rebate_87a),
              format_currency(new.rebate_87a))

    print_row("Tax after Rebate",
              format_currency(old.tax_after_rebate),
              format_currency(new.tax_after_rebate))

    if old.surcharge > 0 or new.surcharge > 0:
        print_row("Add: Surcharge",
                  format_currency(old.surcharge),
                  format_currency(new.surcharge))

    print_row("Add: Health & Education Cess (4%)",
              format_currency(old.cess),
              format_currency(new.cess))

    print(f"\n  {'─' * 66}")
    print_row("TOTAL TAX PAYABLE",
              format_currency(old.total_tax),
              format_currency(new.total_tax),
              highlight=True)

    # Effective Tax Rate
    print(f"\n  {'─' * 66}")
    print_row("Effective Tax Rate",
              f"{old.effective_tax_rate:.2f}%",
              f"{new.effective_tax_rate:.2f}%")

    # TDS Already Paid
    if v.tds_deducted > 0 or v.advance_tax_paid > 0:
        total_paid = v.tds_deducted + v.advance_tax_paid
        print(f"\n  {'─' * 66}")
        print_single_row("TDS Deducted", format_currency(v.tds_deducted))
        print_single_row("Advance Tax Paid", format_currency(v.advance_tax_paid))
        old_balance = old.total_tax - total_paid
        new_balance = new.total_tax - total_paid
        print_row("Balance Tax Payable / (Refund)",
                  format_currency(old_balance),
                  format_currency(new_balance),
                  highlight=True)

    # Recommendation
    print_section("RECOMMENDATION")

    savings = old.total_tax - new.total_tax

    if savings > 0:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}✓ NEW TAX REGIME is better for you!{Colors.END}")
        print(f"  {Colors.GREEN}  You save {format_currency(savings)} by choosing New Regime{Colors.END}")
    elif savings < 0:
        print(f"\n  {Colors.GREEN}{Colors.BOLD}✓ OLD TAX REGIME is better for you!{Colors.END}")
        print(f"  {Colors.GREEN}  You save {format_currency(abs(savings))} by choosing Old Regime{Colors.END}")
    else:
        print(f"\n  {Colors.YELLOW}Both regimes result in the same tax liability.{Colors.END}")
        print(f"  {Colors.YELLOW}New Regime is simpler with fewer compliance requirements.{Colors.END}")

    # Summary Box
    print_section("SUMMARY")
    print(f"""
  ┌───────────────────────────────────────────────────────────────────┐
  │  {Colors.BOLD}OLD REGIME{Colors.END}                                                       │
  │    Gross Salary:     {format_lakhs(old.gross_salary):>12}                              │
  │    Total Deductions: {format_lakhs(old.total_exemptions + old.total_section_16 + old.total_chapter_via):>12}                              │
  │    Taxable Income:   {format_lakhs(old.taxable_income):>12}                              │
  │    Total Tax:        {format_lakhs(old.total_tax):>12}                              │
  ├───────────────────────────────────────────────────────────────────┤
  │  {Colors.BOLD}NEW REGIME{Colors.END}                                                       │
  │    Gross Salary:     {format_lakhs(new.gross_salary):>12}                              │
  │    Total Deductions: {format_lakhs(new.total_exemptions + new.total_section_16 + new.total_chapter_via):>12}                              │
  │    Taxable Income:   {format_lakhs(new.taxable_income):>12}                              │
  │    Total Tax:        {format_lakhs(new.total_tax):>12}                              │
  └───────────────────────────────────────────────────────────────────┘
""")


def print_tax_slabs():
    """Print tax slab information."""
    print_section("TAX SLABS (FY 2025-26)")

    print(f"\n  {Colors.BOLD}NEW TAX REGIME (Default){Colors.END}")
    print(f"  {'Income Slab':<25} {'Tax Rate':>10}")
    print(f"  {'─' * 25} {'─' * 10}")
    print(f"  {'Up to ₹4,00,000':<25} {'Nil':>10}")
    print(f"  {'₹4,00,001 - ₹8,00,000':<25} {'5%':>10}")
    print(f"  {'₹8,00,001 - ₹12,00,000':<25} {'10%':>10}")
    print(f"  {'₹12,00,001 - ₹16,00,000':<25} {'15%':>10}")
    print(f"  {'₹16,00,001 - ₹20,00,000':<25} {'20%':>10}")
    print(f"  {'₹20,00,001 - ₹24,00,000':<25} {'25%':>10}")
    print(f"  {'Above ₹24,00,000':<25} {'30%':>10}")
    print(f"\n  {Colors.CYAN}Rebate: ₹60,000 if income ≤ ₹12,00,000{Colors.END}")
    print(f"  {Colors.CYAN}Standard Deduction: ₹75,000{Colors.END}")

    print(f"\n  {Colors.BOLD}OLD TAX REGIME (Below 60 Years){Colors.END}")
    print(f"  {'Income Slab':<25} {'Tax Rate':>10}")
    print(f"  {'─' * 25} {'─' * 10}")
    print(f"  {'Up to ₹2,50,000':<25} {'Nil':>10}")
    print(f"  {'₹2,50,001 - ₹5,00,000':<25} {'5%':>10}")
    print(f"  {'₹5,00,001 - ₹10,00,000':<25} {'20%':>10}")
    print(f"  {'Above ₹10,00,000':<25} {'30%':>10}")
    print(f"\n  {Colors.CYAN}Rebate: ₹12,500 if income ≤ ₹5,00,000{Colors.END}")
    print(f"  {Colors.CYAN}Standard Deduction: ₹50,000{Colors.END}")

    if v.age_category == 'senior':
        print(f"\n  {Colors.BOLD}OLD TAX REGIME (Senior Citizen: 60-80 Years){Colors.END}")
        print(f"  {'Income Slab':<25} {'Tax Rate':>10}")
        print(f"  {'─' * 25} {'─' * 10}")
        print(f"  {'Up to ₹3,00,000':<25} {'Nil':>10}")
        print(f"  {'₹3,00,001 - ₹5,00,000':<25} {'5%':>10}")
        print(f"  {'₹5,00,001 - ₹10,00,000':<25} {'20%':>10}")
        print(f"  {'Above ₹10,00,000':<25} {'30%':>10}")

    if v.age_category == 'super_senior':
        print(f"\n  {Colors.BOLD}OLD TAX REGIME (Super Senior Citizen: 80+ Years){Colors.END}")
        print(f"  {'Income Slab':<25} {'Tax Rate':>10}")
        print(f"  {'─' * 25} {'─' * 10}")
        print(f"  {'Up to ₹5,00,000':<25} {'Nil':>10}")
        print(f"  {'₹5,00,001 - ₹10,00,000':<25} {'20%':>10}")
        print(f"  {'Above ₹10,00,000':<25} {'30%':>10}")


def print_deduction_limits():
    """Print deduction limits summary."""
    print_section("DEDUCTION LIMITS REFERENCE")

    print(f"\n  {Colors.BOLD}Section 10 Exemptions{Colors.END}")
    print(f"  {'─' * 50}")
    print(f"  {'HRA [10(13A)]':<35} {'As per formula':>15}")
    print(f"  {'LTA [10(5)]':<35} {'Actual expenses':>15}")
    print(f"  {'Children Education [10(14)(ii)]':<35} {'₹100/month/child':>15}")
    print(f"  {'Hostel [10(14)(ii)]':<35} {'₹300/month/child':>15}")
    print(f"  {'Helper/Driver [10(14)(i)]':<35} {'Actual expenses':>15}")
    print(f"  {'Gratuity [10(10)] - Old':<35} {'₹20,00,000':>15}")
    print(f"  {'Gratuity [10(10)] - New':<35} {'₹5,00,000':>15}")
    print(f"  {'Leave Encashment [10(10AA)]':<35} {'₹25,00,000':>15}")

    print(f"\n  {Colors.BOLD}Chapter VI-A Deductions (Old Regime Only){Colors.END}")
    print(f"  {'─' * 50}")
    print(f"  {'80C (Combined)':<35} {'₹1,50,000':>15}")
    print(f"  {'80CCD(1B) - Additional NPS':<35} {'₹50,000':>15}")
    print(f"  {'80CCD(2) - Employer NPS (Both)':<35} {'14% of Basic+DA':>15}")
    print(f"  {'80D - Self/Family':<35} {'₹25,000/₹50,000':>15}")
    print(f"  {'80D - Parents':<35} {'₹25,000/₹50,000':>15}")
    print(f"  {'80DD - Disabled Dependent':<35} {'₹75,000/₹1,25,000':>15}")
    print(f"  {'80DDB - Medical Treatment':<35} {'₹40,000/₹1,00,000':>15}")
    print(f"  {'80E - Education Loan Interest':<35} {'No limit':>15}")
    print(f"  {'80EE - Home Loan Interest':<35} {'₹50,000':>15}")
    print(f"  {'80EEA - Add. Home Loan':<35} {'₹1,50,000':>15}")
    print(f"  {'80EEB - EV Loan Interest':<35} {'₹1,50,000':>15}")
    print(f"  {'80G - Donations':<35} {'50%/100%':>15}")
    print(f"  {'80GG - Rent (No HRA)':<35} {'₹60,000/year':>15}")
    print(f"  {'80TTA - Savings Interest':<35} {'₹10,000':>15}")
    print(f"  {'80TTB - Senior Interest':<35} {'₹50,000':>15}")

    print(f"\n  {Colors.BOLD}Section 24 - Home Loan Interest{Colors.END}")
    print(f"  {'─' * 50}")
    print(f"  {'Self-Occupied (Old Regime)':<35} {'₹2,00,000':>15}")
    print(f"  {'Let-Out Property (Both)':<35} {'No limit':>15}")


def main():
    """Main function to run the tax comparison."""
    # Check if any salary component is set
    if v.basic_salary == 0:
        print(f"\n{Colors.RED}⚠ No salary data found!{Colors.END}")
        print(f"\nPlease update the values in {Colors.BOLD}variables.py{Colors.END} file.")
        print("\nExample:")
        print("  basic_salary = 1200000  # ₹12 Lakh per year")
        print("  hra_received = 480000   # ₹4.8 Lakh per year")
        print("  ... and so on")
        print_deduction_limits()
        return

    # Calculate and compare
    old_regime, new_regime = compare_regimes()

    # Print comparison
    print_comparison_table(old_regime, new_regime)

    # Print tax slabs
    print_tax_slabs()


if __name__ == "__main__":
    main()
