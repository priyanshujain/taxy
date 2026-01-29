"""
India Tax Regime Comparison System - Variables File
Assessment Year: 2026-27 (Financial Year: 2025-26)

Reads values from .env file. Copy .env.example to .env and fill in your values.
All values default to 0 if not set in environment.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_float(key: str, default: float = 0) -> float:
    """Get float value from environment variable."""
    return float(os.getenv(key, default))


def get_int(key: str, default: int = 0) -> int:
    """Get int value from environment variable."""
    return int(os.getenv(key, default))


def get_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    return os.getenv(key, str(default)).lower() in ('true', '1', 'yes')


def get_str(key: str, default: str = "") -> str:
    """Get string value from environment variable."""
    return os.getenv(key, default)


# =============================================================================
# PERSONAL INFORMATION
# =============================================================================

# Age category: "below_60", "senior" (60-80), "super_senior" (above 80)
age_category: str = get_str("AGE_CATEGORY", "below_60")

# City type for HRA calculation: "metro" (Delhi, Mumbai, Chennai, Kolkata) or "non_metro"
city_type: str = get_str("CITY_TYPE", "non_metro")

# =============================================================================
# SALARY COMPONENTS (Annual Amounts in INR)
# =============================================================================

# Basic Components
basic_salary: float = get_float("BASIC_SALARY")
dearness_allowance: float = get_float("DEARNESS_ALLOWANCE")  # DA

# House Rent Allowance
hra_received: float = get_float("HRA_RECEIVED")
rent_paid_annual: float = get_float("RENT_PAID_ANNUAL")  # Actual rent paid per year

# Travel & Conveyance
lta_received: float = get_float("LTA_RECEIVED")  # Leave Travel Allowance
lta_claimed: float = get_float("LTA_CLAIMED")  # Actual travel expenses claimed
conveyance_allowance: float = get_float("CONVEYANCE_ALLOWANCE")  # For official duties
conveyance_actual_expenses: float = get_float("CONVEYANCE_ACTUAL_EXPENSES")

# Special Allowances
special_allowance: float = get_float("SPECIAL_ALLOWANCE")  # Fully taxable
medical_allowance: float = get_float("MEDICAL_ALLOWANCE")  # Fully taxable
transport_allowance: float = get_float("TRANSPORT_ALLOWANCE")  # For commute

# For Disabled Employees (Transport Allowance)
is_disabled: bool = get_bool("IS_DISABLED")  # If True, transport allowance exempt up to Rs 3,200/month

# Children Related Allowances
children_education_allowance: float = get_float("CHILDREN_EDUCATION_ALLOWANCE")  # Max exempt: Rs 100/month/child
hostel_allowance: float = get_float("HOSTEL_ALLOWANCE")  # Max exempt: Rs 300/month/child
number_of_children: int = get_int("NUMBER_OF_CHILDREN")  # Max 2 for exemption purposes

# Work Related Allowances
helper_allowance: float = get_float("HELPER_ALLOWANCE")  # For hiring helper (Driver salary, etc.)
helper_actual_expenses: float = get_float("HELPER_ACTUAL_EXPENSES")  # Actual amount spent
uniform_allowance: float = get_float("UNIFORM_ALLOWANCE")  # For uniform purchase/maintenance
uniform_actual_expenses: float = get_float("UNIFORM_ACTUAL_EXPENSES")  # Actual amount spent

# Food/Meal Benefits
meal_allowance: float = get_float("MEAL_ALLOWANCE")  # Food vouchers/Sodexo
number_of_working_days: int = get_int("NUMBER_OF_WORKING_DAYS", 220)

# Performance Pay
bonus: float = get_float("BONUS")
commission: float = get_float("COMMISSION")
overtime_pay: float = get_float("OVERTIME_PAY")

# =============================================================================
# RETIREMENT BENEFITS (Usually received on retirement/resignation)
# =============================================================================

gratuity_received: float = get_float("GRATUITY_RECEIVED")  # Exempt up to Rs 20L (old) / Rs 5L (new)
leave_encashment_received: float = get_float("LEAVE_ENCASHMENT_RECEIVED")  # Exempt up to Rs 25L
is_government_employee: bool = get_bool("IS_GOVERNMENT_EMPLOYEE")

# =============================================================================
# EMPLOYER CONTRIBUTIONS
# =============================================================================

employer_epf_contribution: float = get_float("EMPLOYER_EPF_CONTRIBUTION")
employer_nps_contribution: float = get_float("EMPLOYER_NPS_CONTRIBUTION")
employer_superannuation_contribution: float = get_float("EMPLOYER_SUPERANNUATION_CONTRIBUTION")

# Note: Combined limit of Rs 7.5L for EPF + NPS + Superannuation. Excess is taxable.

# =============================================================================
# SECTION 16 - DEDUCTIONS FROM SALARY
# =============================================================================

# Standard Deduction: Auto-calculated (Rs 50,000 old / Rs 75,000 new)
professional_tax_paid: float = get_float("PROFESSIONAL_TAX_PAID")  # Max Rs 2,500
entertainment_allowance: float = get_float("ENTERTAINMENT_ALLOWANCE")  # Only for Govt employees

# =============================================================================
# SECTION 10 - EXEMPTIONS
# =============================================================================

other_section_10_exemptions: float = get_float("OTHER_SECTION_10_EXEMPTIONS")

# =============================================================================
# CHAPTER VI-A DEDUCTIONS (OLD REGIME ONLY, except 80CCD(2))
# =============================================================================

# Section 80C (Combined limit Rs 1,50,000)
epf_contribution_employee: float = get_float("EPF_CONTRIBUTION_EMPLOYEE")
ppf_contribution: float = get_float("PPF_CONTRIBUTION")
life_insurance_premium: float = get_float("LIFE_INSURANCE_PREMIUM")
elss_investment: float = get_float("ELSS_INVESTMENT")
nsc_investment: float = get_float("NSC_INVESTMENT")
sukanya_samriddhi: float = get_float("SUKANYA_SAMRIDDHI")
tax_saver_fd: float = get_float("TAX_SAVER_FD")
tuition_fees: float = get_float("TUITION_FEES")
home_loan_principal: float = get_float("HOME_LOAN_PRINCIPAL")
scss_investment: float = get_float("SCSS_INVESTMENT")
other_80c: float = get_float("OTHER_80C")

# Section 80CCC - Pension Fund (within 80C limit)
pension_fund_contribution: float = get_float("PENSION_FUND_CONTRIBUTION")

# Section 80CCD(1) - Employee NPS Contribution (within 80C limit)
employee_nps_contribution: float = get_float("EMPLOYEE_NPS_CONTRIBUTION")

# Section 80CCD(1B) - Additional NPS (Over and above 80C, max Rs 50,000)
additional_nps_contribution: float = get_float("ADDITIONAL_NPS_CONTRIBUTION")

# Section 80CCD(2) - Employer NPS (ALLOWED IN BOTH REGIMES, up to 14% of basic+DA)
# This is auto-calculated from employer_nps_contribution

# Section 80D - Health Insurance Premium
health_insurance_self: float = get_float("HEALTH_INSURANCE_SELF")  # Max Rs 25,000 / Rs 50,000 if senior
health_insurance_parents: float = get_float("HEALTH_INSURANCE_PARENTS")  # Max Rs 25,000 / Rs 50,000
preventive_health_checkup: float = get_float("PREVENTIVE_HEALTH_CHECKUP")  # Max Rs 5,000
parents_are_senior_citizen: bool = get_bool("PARENTS_ARE_SENIOR_CITIZEN")

# Section 80DD - Disabled Dependent
disabled_dependent_expenses: float = get_float("DISABLED_DEPENDENT_EXPENSES")  # Rs 75,000 / Rs 1,25,000
is_severe_disability: bool = get_bool("IS_SEVERE_DISABILITY")

# Section 80DDB - Medical Treatment for Specified Diseases
medical_treatment_expenses: float = get_float("MEDICAL_TREATMENT_EXPENSES")  # Rs 40,000 / Rs 1,00,000

# Section 80E - Education Loan Interest (No upper limit, max 8 years)
education_loan_interest: float = get_float("EDUCATION_LOAN_INTEREST")

# Section 80EE - Home Loan Interest (First-time buyers)
home_loan_interest_80ee: float = get_float("HOME_LOAN_INTEREST_80EE")  # Max Rs 50,000

# Section 80EEA - Additional Home Loan Interest (Affordable housing)
home_loan_interest_80eea: float = get_float("HOME_LOAN_INTEREST_80EEA")  # Max Rs 1,50,000

# Section 80EEB - Electric Vehicle Loan Interest
ev_loan_interest: float = get_float("EV_LOAN_INTEREST")  # Max Rs 1,50,000

# Section 80G - Donations
donations_100_percent: float = get_float("DONATIONS_100_PERCENT")  # PM Relief Fund, etc.
donations_50_percent: float = get_float("DONATIONS_50_PERCENT")  # Other approved funds

# Section 80GG - Rent Paid (If NOT receiving HRA)
rent_paid_no_hra: float = get_float("RENT_PAID_NO_HRA")  # Max Rs 60,000/year

# Section 80TTA - Interest on Savings Account (Non-Senior Citizens)
savings_account_interest: float = get_float("SAVINGS_ACCOUNT_INTEREST")  # Max Rs 10,000

# Section 80TTB - Interest Income for Senior Citizens
senior_citizen_interest_income: float = get_float("SENIOR_CITIZEN_INTEREST_INCOME")  # Max Rs 50,000

# Section 80U - Person with Disability (Self)
self_disability_claim: bool = get_bool("SELF_DISABILITY_CLAIM")
self_severe_disability: bool = get_bool("SELF_SEVERE_DISABILITY")

# =============================================================================
# SECTION 24 - HOME LOAN INTEREST DEDUCTION
# =============================================================================

home_loan_interest_self_occupied: float = get_float("HOME_LOAN_INTEREST_SELF_OCCUPIED")  # Max Rs 2,00,000
home_loan_interest_let_out: float = get_float("HOME_LOAN_INTEREST_LET_OUT")  # No limit
rental_income_annual: float = get_float("RENTAL_INCOME_ANNUAL")
pre_construction_interest: float = get_float("PRE_CONSTRUCTION_INTEREST")
construction_completed: bool = get_bool("CONSTRUCTION_COMPLETED")

# =============================================================================
# OTHER INCOME
# =============================================================================

interest_income_other: float = get_float("INTEREST_INCOME_OTHER")  # FD interest, etc.
other_income: float = get_float("OTHER_INCOME")

# =============================================================================
# TAX ALREADY PAID
# =============================================================================

tds_deducted: float = get_float("TDS_DEDUCTED")
advance_tax_paid: float = get_float("ADVANCE_TAX_PAID")
