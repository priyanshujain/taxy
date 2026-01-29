"""
India Tax Regime Comparison System
Assessment Year: 2026-27 (Financial Year: 2025-26)

Compares Old Tax Regime vs New Tax Regime and calculates effective tax.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import variables as v


# =============================================================================
# TAX SLABS AND LIMITS (FY 2025-26 / AY 2026-27)
# =============================================================================

# New Tax Regime Slabs (FY 2025-26) - Same for all ages
NEW_REGIME_SLABS = [
    (400000, 0.00),    # 0 - 4L: 0%
    (800000, 0.05),    # 4L - 8L: 5%
    (1200000, 0.10),   # 8L - 12L: 10%
    (1600000, 0.15),   # 12L - 16L: 15%
    (2000000, 0.20),   # 16L - 20L: 20%
    (2400000, 0.25),   # 20L - 24L: 25%
    (float('inf'), 0.30),  # Above 24L: 30%
]

# Old Tax Regime Slabs - Below 60 years
OLD_REGIME_SLABS_BELOW_60 = [
    (250000, 0.00),    # 0 - 2.5L: 0%
    (500000, 0.05),    # 2.5L - 5L: 5%
    (1000000, 0.20),   # 5L - 10L: 20%
    (float('inf'), 0.30),  # Above 10L: 30%
]

# Old Tax Regime Slabs - Senior Citizen (60-80 years)
OLD_REGIME_SLABS_SENIOR = [
    (300000, 0.00),    # 0 - 3L: 0%
    (500000, 0.05),    # 3L - 5L: 5%
    (1000000, 0.20),   # 5L - 10L: 20%
    (float('inf'), 0.30),  # Above 10L: 30%
]

# Old Tax Regime Slabs - Super Senior Citizen (Above 80 years)
OLD_REGIME_SLABS_SUPER_SENIOR = [
    (500000, 0.00),    # 0 - 5L: 0%
    (1000000, 0.20),   # 5L - 10L: 20%
    (float('inf'), 0.30),  # Above 10L: 30%
]

# Limits
LIMITS = {
    # Standard Deduction
    'standard_deduction_old': 50000,
    'standard_deduction_new': 75000,

    # Section 10 Exemptions
    'gratuity_old': 2000000,  # Rs 20 Lakh
    'gratuity_new': 500000,   # Rs 5 Lakh
    'leave_encashment': 2500000,  # Rs 25 Lakh
    'children_education_per_child_monthly': 100,  # Rs 100/month
    'hostel_per_child_monthly': 300,  # Rs 300/month
    'max_children_for_exemption': 2,
    'transport_disabled_monthly': 3200,  # Rs 3,200/month
    'meal_per_meal': 50,  # Rs 50 per meal

    # Chapter VI-A
    '80c_limit': 150000,
    '80ccd_1b_limit': 50000,
    '80ccd_2_percent': 0.14,  # 14% of Basic + DA
    '80d_self_normal': 25000,
    '80d_self_senior': 50000,
    '80d_parents_normal': 25000,
    '80d_parents_senior': 50000,
    '80d_preventive': 5000,
    '80dd_normal': 75000,
    '80dd_severe': 125000,
    '80ddb_normal': 40000,
    '80ddb_senior': 100000,
    '80ee_limit': 50000,
    '80eea_limit': 150000,
    '80eeb_limit': 150000,
    '80gg_monthly': 5000,
    '80tta_limit': 10000,
    '80ttb_limit': 50000,
    '80u_normal': 75000,
    '80u_severe': 125000,

    # Section 24
    'home_loan_interest_self_occupied': 200000,

    # Combined Employer Contribution Limit
    'employer_contribution_combined': 750000,  # Rs 7.5 Lakh

    # Rebate
    'rebate_87a_old_limit': 500000,
    'rebate_87a_old_amount': 12500,
    'rebate_87a_new_limit': 1200000,
    'rebate_87a_new_amount': 60000,

    # Surcharge thresholds
    'surcharge_50l': 5000000,
    'surcharge_1cr': 10000000,
    'surcharge_2cr': 20000000,
    'surcharge_5cr': 50000000,

    # Cess
    'cess_rate': 0.04,
}


@dataclass
class TaxBreakdown:
    """Stores detailed tax calculation breakdown."""
    regime: str
    gross_salary: float = 0

    # Exemptions
    exemptions: Dict[str, float] = field(default_factory=dict)
    total_exemptions: float = 0

    # Income from Salary
    income_from_salary: float = 0

    # Section 16 Deductions
    section_16_deductions: Dict[str, float] = field(default_factory=dict)
    total_section_16: float = 0

    # Net Salary Income
    net_salary_income: float = 0

    # Income from House Property
    income_from_house_property: float = 0

    # Other Income
    other_income: float = 0

    # Gross Total Income
    gross_total_income: float = 0

    # Chapter VI-A Deductions
    chapter_via_deductions: Dict[str, float] = field(default_factory=dict)
    total_chapter_via: float = 0

    # Taxable Income
    taxable_income: float = 0

    # Tax Calculation
    tax_on_income: float = 0
    rebate_87a: float = 0
    tax_after_rebate: float = 0
    surcharge: float = 0
    cess: float = 0
    total_tax: float = 0

    # Effective Tax Rate
    effective_tax_rate: float = 0


def calculate_hra_exemption() -> float:
    """Calculate HRA exemption under Section 10(13A)."""
    if v.hra_received == 0 or v.rent_paid_annual == 0:
        return 0

    basic_plus_da = v.basic_salary + v.dearness_allowance

    # Three conditions for HRA exemption
    actual_hra = v.hra_received
    rent_minus_10_percent = v.rent_paid_annual - (0.10 * basic_plus_da)

    if v.city_type == "metro":
        percent_of_salary = 0.50 * basic_plus_da
    else:
        percent_of_salary = 0.40 * basic_plus_da

    # Exemption is minimum of the three
    exemption = max(0, min(actual_hra, rent_minus_10_percent, percent_of_salary))
    return exemption


def calculate_gross_salary() -> float:
    """Calculate total gross salary."""
    gross = (
        v.basic_salary +
        v.dearness_allowance +
        v.hra_received +
        v.lta_received +
        v.conveyance_allowance +
        v.special_allowance +
        v.medical_allowance +
        v.transport_allowance +
        v.children_education_allowance +
        v.hostel_allowance +
        v.helper_allowance +
        v.uniform_allowance +
        v.meal_allowance +
        v.bonus +
        v.commission +
        v.overtime_pay +
        v.gratuity_received +
        v.leave_encashment_received +
        v.entertainment_allowance
    )

    # Employer contributions (taxable portion if exceeds limit)
    employer_total = (
        v.employer_epf_contribution +
        v.employer_nps_contribution +
        v.employer_superannuation_contribution
    )
    if employer_total > LIMITS['employer_contribution_combined']:
        gross += employer_total - LIMITS['employer_contribution_combined']

    return gross


def calculate_exemptions_old_regime() -> Dict[str, float]:
    """Calculate Section 10 exemptions for Old Tax Regime."""
    exemptions = {}

    # HRA Exemption [10(13A)]
    hra_exempt = calculate_hra_exemption()
    if hra_exempt > 0:
        exemptions['HRA Exemption [10(13A)]'] = hra_exempt

    # LTA Exemption [10(5)]
    lta_exempt = min(v.lta_received, v.lta_claimed)
    if lta_exempt > 0:
        exemptions['LTA Exemption [10(5)]'] = lta_exempt

    # Children Education Allowance [10(14)(ii)]
    num_children = min(v.number_of_children, LIMITS['max_children_for_exemption'])
    education_exempt = min(
        v.children_education_allowance,
        num_children * LIMITS['children_education_per_child_monthly'] * 12
    )
    if education_exempt > 0:
        exemptions['Children Education [10(14)(ii)]'] = education_exempt

    # Hostel Allowance [10(14)(ii)]
    hostel_exempt = min(
        v.hostel_allowance,
        num_children * LIMITS['hostel_per_child_monthly'] * 12
    )
    if hostel_exempt > 0:
        exemptions['Hostel Allowance [10(14)(ii)]'] = hostel_exempt

    # Helper Allowance [10(14)(i)]
    helper_exempt = min(v.helper_allowance, v.helper_actual_expenses)
    if helper_exempt > 0:
        exemptions['Helper/Driver [10(14)(i)]'] = helper_exempt

    # Uniform Allowance [10(14)(i)]
    uniform_exempt = min(v.uniform_allowance, v.uniform_actual_expenses)
    if uniform_exempt > 0:
        exemptions['Uniform Allowance [10(14)(i)]'] = uniform_exempt

    # Conveyance Allowance [10(14)]
    conveyance_exempt = min(v.conveyance_allowance, v.conveyance_actual_expenses)
    if conveyance_exempt > 0:
        exemptions['Conveyance [10(14)]'] = conveyance_exempt

    # Transport Allowance for Disabled [10(14)]
    if v.is_disabled:
        transport_exempt = min(
            v.transport_allowance,
            LIMITS['transport_disabled_monthly'] * 12
        )
        if transport_exempt > 0:
            exemptions['Transport (Disabled) [10(14)]'] = transport_exempt

    # Meal Voucher Exemption (Rs 50/meal, 2 meals/day)
    meal_exempt = min(
        v.meal_allowance,
        LIMITS['meal_per_meal'] * 2 * v.number_of_working_days
    )
    if meal_exempt > 0:
        exemptions['Meal Voucher Exemption'] = meal_exempt

    # Gratuity Exemption [10(10)]
    gratuity_exempt = min(v.gratuity_received, LIMITS['gratuity_old'])
    if gratuity_exempt > 0:
        exemptions['Gratuity [10(10)]'] = gratuity_exempt

    # Leave Encashment [10(10AA)]
    if v.is_government_employee:
        leave_exempt = v.leave_encashment_received  # Fully exempt for govt
    else:
        leave_exempt = min(v.leave_encashment_received, LIMITS['leave_encashment'])
    if leave_exempt > 0:
        exemptions['Leave Encashment [10(10AA)]'] = leave_exempt

    # Other Section 10 Exemptions
    if v.other_section_10_exemptions > 0:
        exemptions['Other Section 10 Exemptions'] = v.other_section_10_exemptions

    return exemptions


def calculate_exemptions_new_regime() -> Dict[str, float]:
    """Calculate Section 10 exemptions for New Tax Regime."""
    exemptions = {}

    # Transport Allowance for Disabled [10(14)] - Allowed in New Regime
    if v.is_disabled:
        transport_exempt = min(
            v.transport_allowance,
            LIMITS['transport_disabled_monthly'] * 12
        )
        if transport_exempt > 0:
            exemptions['Transport (Disabled) [10(14)]'] = transport_exempt

    # Conveyance for official duties - Allowed in New Regime
    conveyance_exempt = min(v.conveyance_allowance, v.conveyance_actual_expenses)
    if conveyance_exempt > 0:
        exemptions['Conveyance (Official) [10(14)]'] = conveyance_exempt

    # Gratuity Exemption [10(10)] - Rs 5 Lakh in New Regime
    gratuity_exempt = min(v.gratuity_received, LIMITS['gratuity_new'])
    if gratuity_exempt > 0:
        exemptions['Gratuity [10(10)]'] = gratuity_exempt

    # Leave Encashment [10(10AA)] - Still allowed
    if v.is_government_employee:
        leave_exempt = v.leave_encashment_received
    else:
        leave_exempt = min(v.leave_encashment_received, LIMITS['leave_encashment'])
    if leave_exempt > 0:
        exemptions['Leave Encashment [10(10AA)]'] = leave_exempt

    return exemptions


def calculate_section_16_old_regime() -> Dict[str, float]:
    """Calculate Section 16 deductions for Old Tax Regime."""
    deductions = {}

    # Standard Deduction [16(ia)]
    deductions['Standard Deduction [16(ia)]'] = LIMITS['standard_deduction_old']

    # Professional Tax [16(iii)]
    if v.professional_tax_paid > 0:
        deductions['Professional Tax [16(iii)]'] = min(v.professional_tax_paid, 2500)

    # Entertainment Allowance [16(ii)] - Only for Govt employees
    if v.is_government_employee and v.entertainment_allowance > 0:
        # Min of: Actual, 1/5th of Basic, Rs 5,000
        ent_deduction = min(
            v.entertainment_allowance,
            v.basic_salary / 5,
            5000
        )
        deductions['Entertainment Allowance [16(ii)]'] = ent_deduction

    return deductions


def calculate_section_16_new_regime() -> Dict[str, float]:
    """Calculate Section 16 deductions for New Tax Regime."""
    deductions = {}

    # Standard Deduction [16(ia)] - Rs 75,000 in New Regime
    deductions['Standard Deduction [16(ia)]'] = LIMITS['standard_deduction_new']

    # Note: Professional Tax and Entertainment Allowance NOT allowed in New Regime

    return deductions


def calculate_income_from_house_property(regime: str) -> Tuple[float, Dict[str, float]]:
    """Calculate income/loss from house property."""
    details = {}

    # Self-Occupied Property
    self_occupied_loss = 0
    if v.home_loan_interest_self_occupied > 0:
        if regime == 'old':
            # Max Rs 2 Lakh deduction for self-occupied
            self_occupied_loss = min(
                v.home_loan_interest_self_occupied,
                LIMITS['home_loan_interest_self_occupied']
            )
            details['Self-Occupied Interest [24(b)]'] = -self_occupied_loss
        # New regime: No deduction for self-occupied

    # Let-Out Property
    let_out_income = 0
    if v.rental_income_annual > 0:
        gross_rent = v.rental_income_annual
        standard_deduction = gross_rent * 0.30  # 30% standard deduction
        interest_deduction = v.home_loan_interest_let_out  # No limit for let-out

        let_out_income = gross_rent - standard_deduction - interest_deduction

        details['Rental Income'] = gross_rent
        details['Standard Deduction (30%)'] = -standard_deduction
        if interest_deduction > 0:
            details['Let-Out Interest [24(b)]'] = -interest_deduction

    # Pre-construction interest (1/5th per year for 5 years)
    if v.construction_completed and v.pre_construction_interest > 0:
        pre_construction_yearly = v.pre_construction_interest / 5
        if regime == 'old':
            details['Pre-construction Interest'] = -pre_construction_yearly
            self_occupied_loss += pre_construction_yearly

    total_house_property = let_out_income - self_occupied_loss

    # Loss from house property can be set off only up to Rs 2 Lakh
    if total_house_property < -200000:
        total_house_property = -200000
        details['Loss restricted to Rs 2 Lakh'] = True

    return total_house_property, details


def calculate_chapter_via_old_regime() -> Dict[str, float]:
    """Calculate Chapter VI-A deductions for Old Tax Regime."""
    deductions = {}

    # Section 80C (Combined limit Rs 1,50,000)
    total_80c = (
        v.epf_contribution_employee +
        v.ppf_contribution +
        v.life_insurance_premium +
        v.elss_investment +
        v.nsc_investment +
        v.sukanya_samriddhi +
        v.tax_saver_fd +
        v.tuition_fees +
        v.home_loan_principal +
        v.scss_investment +
        v.other_80c +
        v.pension_fund_contribution +
        min(v.employee_nps_contribution, LIMITS['80c_limit'])  # 80CCD(1) within 80C
    )
    deduction_80c = min(total_80c, LIMITS['80c_limit'])
    if deduction_80c > 0:
        deductions['Section 80C'] = deduction_80c

    # Section 80CCD(1B) - Additional NPS
    deduction_80ccd_1b = min(v.additional_nps_contribution, LIMITS['80ccd_1b_limit'])
    if deduction_80ccd_1b > 0:
        deductions['Section 80CCD(1B) - Add. NPS'] = deduction_80ccd_1b

    # Section 80CCD(2) - Employer NPS (up to 14% of Basic+DA)
    basic_plus_da = v.basic_salary + v.dearness_allowance
    max_employer_nps = basic_plus_da * LIMITS['80ccd_2_percent']
    deduction_80ccd_2 = min(v.employer_nps_contribution, max_employer_nps)
    if deduction_80ccd_2 > 0:
        deductions['Section 80CCD(2) - Employer NPS'] = deduction_80ccd_2

    # Section 80D - Health Insurance
    # Self, spouse, children
    self_limit = LIMITS['80d_self_senior'] if v.age_category != 'below_60' else LIMITS['80d_self_normal']
    deduction_80d_self = min(v.health_insurance_self, self_limit)

    # Parents
    parents_limit = LIMITS['80d_parents_senior'] if v.parents_are_senior_citizen else LIMITS['80d_parents_normal']
    deduction_80d_parents = min(v.health_insurance_parents, parents_limit)

    # Preventive health checkup (within above limits)
    preventive = min(v.preventive_health_checkup, LIMITS['80d_preventive'])

    total_80d = deduction_80d_self + deduction_80d_parents
    # Preventive is included in the limits, not additional
    if total_80d > 0:
        deductions['Section 80D - Health Insurance'] = total_80d

    # Section 80DD - Disabled Dependent
    if v.disabled_dependent_expenses > 0:
        if v.is_severe_disability:
            deductions['Section 80DD - Disabled Dependent'] = LIMITS['80dd_severe']
        else:
            deductions['Section 80DD - Disabled Dependent'] = LIMITS['80dd_normal']

    # Section 80DDB - Medical Treatment
    if v.medical_treatment_expenses > 0:
        limit = LIMITS['80ddb_senior'] if v.age_category != 'below_60' else LIMITS['80ddb_normal']
        deductions['Section 80DDB - Medical Treatment'] = min(v.medical_treatment_expenses, limit)

    # Section 80E - Education Loan Interest (No limit)
    if v.education_loan_interest > 0:
        deductions['Section 80E - Education Loan'] = v.education_loan_interest

    # Section 80EE - Home Loan Interest
    if v.home_loan_interest_80ee > 0:
        deductions['Section 80EE - Home Loan'] = min(v.home_loan_interest_80ee, LIMITS['80ee_limit'])

    # Section 80EEA - Additional Home Loan Interest
    if v.home_loan_interest_80eea > 0:
        deductions['Section 80EEA - Add. Home Loan'] = min(v.home_loan_interest_80eea, LIMITS['80eea_limit'])

    # Section 80EEB - EV Loan Interest
    if v.ev_loan_interest > 0:
        deductions['Section 80EEB - EV Loan'] = min(v.ev_loan_interest, LIMITS['80eeb_limit'])

    # Section 80G - Donations
    if v.donations_100_percent > 0:
        deductions['Section 80G - Donations (100%)'] = v.donations_100_percent
    if v.donations_50_percent > 0:
        deductions['Section 80G - Donations (50%)'] = v.donations_50_percent * 0.5

    # Section 80GG - Rent Paid (if not receiving HRA)
    if v.rent_paid_no_hra > 0 and v.hra_received == 0:
        deductions['Section 80GG - Rent'] = min(v.rent_paid_no_hra, LIMITS['80gg_monthly'] * 12)

    # Section 80TTA - Savings Interest (Non-senior citizens)
    if v.age_category == 'below_60' and v.savings_account_interest > 0:
        deductions['Section 80TTA - Savings Interest'] = min(v.savings_account_interest, LIMITS['80tta_limit'])

    # Section 80TTB - Interest Income (Senior citizens only)
    if v.age_category != 'below_60' and v.senior_citizen_interest_income > 0:
        deductions['Section 80TTB - Interest Income'] = min(v.senior_citizen_interest_income, LIMITS['80ttb_limit'])

    # Section 80U - Self Disability
    if v.self_disability_claim:
        if v.self_severe_disability:
            deductions['Section 80U - Self Disability'] = LIMITS['80u_severe']
        else:
            deductions['Section 80U - Self Disability'] = LIMITS['80u_normal']

    return deductions


def calculate_chapter_via_new_regime() -> Dict[str, float]:
    """Calculate Chapter VI-A deductions for New Tax Regime."""
    deductions = {}

    # Only 80CCD(2) - Employer NPS is allowed in New Regime
    basic_plus_da = v.basic_salary + v.dearness_allowance
    max_employer_nps = basic_plus_da * LIMITS['80ccd_2_percent']
    deduction_80ccd_2 = min(v.employer_nps_contribution, max_employer_nps)
    if deduction_80ccd_2 > 0:
        deductions['Section 80CCD(2) - Employer NPS'] = deduction_80ccd_2

    return deductions


def calculate_tax_on_income(taxable_income: float, regime: str) -> float:
    """Calculate tax based on slabs."""
    if taxable_income <= 0:
        return 0

    if regime == 'new':
        slabs = NEW_REGIME_SLABS
    else:
        if v.age_category == 'super_senior':
            slabs = OLD_REGIME_SLABS_SUPER_SENIOR
        elif v.age_category == 'senior':
            slabs = OLD_REGIME_SLABS_SENIOR
        else:
            slabs = OLD_REGIME_SLABS_BELOW_60

    tax = 0
    previous_limit = 0

    for limit, rate in slabs:
        if taxable_income <= previous_limit:
            break

        taxable_in_slab = min(taxable_income, limit) - previous_limit
        tax += taxable_in_slab * rate
        previous_limit = limit

    return tax


def calculate_rebate_87a(taxable_income: float, tax: float, regime: str) -> float:
    """Calculate rebate under Section 87A."""
    if regime == 'new':
        if taxable_income <= LIMITS['rebate_87a_new_limit']:
            return min(tax, LIMITS['rebate_87a_new_amount'])
    else:
        if taxable_income <= LIMITS['rebate_87a_old_limit']:
            return min(tax, LIMITS['rebate_87a_old_amount'])
    return 0


def calculate_surcharge(taxable_income: float, tax: float, regime: str) -> float:
    """Calculate surcharge based on income level."""
    if taxable_income <= LIMITS['surcharge_50l']:
        return 0

    if regime == 'new':
        # New regime: Max surcharge 25%
        if taxable_income > LIMITS['surcharge_2cr']:
            rate = 0.25
        elif taxable_income > LIMITS['surcharge_1cr']:
            rate = 0.15
        elif taxable_income > LIMITS['surcharge_50l']:
            rate = 0.10
        else:
            rate = 0
    else:
        # Old regime: Max surcharge 37%
        if taxable_income > LIMITS['surcharge_5cr']:
            rate = 0.37
        elif taxable_income > LIMITS['surcharge_2cr']:
            rate = 0.25
        elif taxable_income > LIMITS['surcharge_1cr']:
            rate = 0.15
        elif taxable_income > LIMITS['surcharge_50l']:
            rate = 0.10
        else:
            rate = 0

    surcharge = tax * rate

    # Marginal relief calculation (simplified)
    # TODO: Implement full marginal relief logic

    return surcharge


def calculate_tax(regime: str) -> TaxBreakdown:
    """Calculate complete tax for a given regime."""
    breakdown = TaxBreakdown(regime=regime)

    # Step 1: Calculate Gross Salary
    breakdown.gross_salary = calculate_gross_salary()

    # Step 2: Calculate Exemptions
    if regime == 'old':
        breakdown.exemptions = calculate_exemptions_old_regime()
    else:
        breakdown.exemptions = calculate_exemptions_new_regime()
    breakdown.total_exemptions = sum(breakdown.exemptions.values())

    # Step 3: Income from Salary (after exemptions)
    breakdown.income_from_salary = breakdown.gross_salary - breakdown.total_exemptions

    # Step 4: Section 16 Deductions
    if regime == 'old':
        breakdown.section_16_deductions = calculate_section_16_old_regime()
    else:
        breakdown.section_16_deductions = calculate_section_16_new_regime()
    breakdown.total_section_16 = sum(breakdown.section_16_deductions.values())

    # Step 5: Net Salary Income
    breakdown.net_salary_income = max(0, breakdown.income_from_salary - breakdown.total_section_16)

    # Step 6: Income from House Property
    breakdown.income_from_house_property, _ = calculate_income_from_house_property(regime)

    # Step 7: Other Income
    breakdown.other_income = v.interest_income_other + v.other_income + v.savings_account_interest

    # Step 8: Gross Total Income
    breakdown.gross_total_income = (
        breakdown.net_salary_income +
        breakdown.income_from_house_property +
        breakdown.other_income
    )

    # Step 9: Chapter VI-A Deductions
    if regime == 'old':
        breakdown.chapter_via_deductions = calculate_chapter_via_old_regime()
    else:
        breakdown.chapter_via_deductions = calculate_chapter_via_new_regime()
    breakdown.total_chapter_via = sum(breakdown.chapter_via_deductions.values())

    # Step 10: Taxable Income
    breakdown.taxable_income = max(0, breakdown.gross_total_income - breakdown.total_chapter_via)

    # Step 11: Tax Calculation
    breakdown.tax_on_income = calculate_tax_on_income(breakdown.taxable_income, regime)

    # Step 12: Rebate under 87A
    breakdown.rebate_87a = calculate_rebate_87a(
        breakdown.taxable_income,
        breakdown.tax_on_income,
        regime
    )
    breakdown.tax_after_rebate = max(0, breakdown.tax_on_income - breakdown.rebate_87a)

    # Step 13: Surcharge
    breakdown.surcharge = calculate_surcharge(
        breakdown.taxable_income,
        breakdown.tax_after_rebate,
        regime
    )

    # Step 14: Health & Education Cess (4%)
    breakdown.cess = (breakdown.tax_after_rebate + breakdown.surcharge) * LIMITS['cess_rate']

    # Step 15: Total Tax
    breakdown.total_tax = breakdown.tax_after_rebate + breakdown.surcharge + breakdown.cess

    # Step 16: Effective Tax Rate
    if breakdown.gross_salary > 0:
        breakdown.effective_tax_rate = (breakdown.total_tax / breakdown.gross_salary) * 100

    return breakdown


def compare_regimes() -> Tuple[TaxBreakdown, TaxBreakdown]:
    """Calculate and compare tax under both regimes."""
    old_regime = calculate_tax('old')
    new_regime = calculate_tax('new')
    return old_regime, new_regime
