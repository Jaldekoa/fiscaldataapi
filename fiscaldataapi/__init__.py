from urllib.parse import urlencode
import pandas as pd
import requests

__base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
__all_types = {
    "NUMBER": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY0": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY1": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY2": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY3": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY4": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY5": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY6": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY7": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY8": lambda x: pd.to_numeric(x, errors="coerce"),
    "CURRENCY9": lambda x: pd.to_numeric(x, errors="coerce"),
    "MONTH": lambda x: pd.to_numeric(x, errors="coerce"),
    "PERCENTAGE": lambda x: pd.to_numeric(x, errors="coerce"),
    "YEAR": lambda x: pd.to_numeric(x, errors="coerce"),
    "DATE": lambda x: pd.to_datetime(x, errors="coerce", format="%Y-%m-%d"),
    "DAY": lambda x: pd.to_numeric(x, errors="coerce"),
    "INTEGER": lambda x: pd.to_numeric(x, errors="coerce"),
    "QUARTER": lambda x: pd.to_numeric(x, errors="coerce"),
    "STRING": str
}

__valid_params = {
    "fields": "fields",
    "filter": "filter",
    "sort": "sort",
    "page_size": "page[size]",
    "page_number": "page[number]"
}

__endpoints = {
    '120 Day Delinquent Debt Referral Compliance Report': '/v2/debt/tror/data_act_compliance',
    'Redemption Tables': '/v2/accounting/od/redemption_tables',
    'Advances to State Unemployment Funds (Social Security Act Title XII)': '/v2/accounting/od/title_xii',
    'Average Interest Rates on U.S. Treasury Securities': '/v2/accounting/od/avg_interest_rates',
    'Operating Cash Balance': '/v1/accounting/dts/operating_cash_balance',
    'Deposits and Withdrawals of Operating Cash': '/v1/accounting/dts/deposits_withdrawals_operating_cash',
    'Public Debt Transactions': '/v1/accounting/dts/public_debt_transactions',
    'Adjustment of Public Debt Transactions to Cash Basis': '/v1/accounting/dts/adjustment_public_debt_transactions_cash_basis',
    'Debt Subject to Limit': '/v1/accounting/dts/debt_subject_to_limit',
    'Inter-Agency Tax Transfers': '/v1/accounting/dts/inter_agency_tax_transfers',
    'Income Tax Refunds Issued': '/v1/accounting/dts/income_tax_refunds_issued',
    'Federal Tax Deposits': '/v1/accounting/dts/federal_tax_deposits',
    'Short-Term Cash Investments': '/v1/accounting/dts/short_term_cash_investments',
    'Debt to the Penny': '/v2/accounting/od/debt_to_penny',
    'Sales': '/v1/accounting/od/securities_sales',
    'Sales by Term': '/v1/accounting/od/securities_sales_term',
    'Transfers of Marketable Securities': '/v1/accounting/od/securities_transfers',
    'Conversions of Paper Savings Bonds': '/v1/accounting/od/securities_conversions',
    'Redemptions': '/v1/accounting/od/securities_redemptions',
    'Outstanding': '/v1/accounting/od/securities_outstanding',
    'Certificates of Indebtedness': '/v1/accounting/od/securities_c_of_i',
    'Accounts': '/v1/accounting/od/securities_accounts',
    'Federal Borrowings Program: Interest on Uninvested Funds': '/v2/accounting/od/interest_uninvested',
    'Summary General Ledger Borrowing Balances': '/v1/accounting/od/fbp_gl_borrowing_balances',
    'Summary General Ledger Repayable Advance Balances': '/v1/accounting/od/fbp_gl_repay_advance_balances',
    'Federal Credit Similar Maturity Rates': '/v1/accounting/od/federal_maturity_rates',
    'Federal Investments Program: Interest Cost by Fund': '/v2/accounting/od/interest_cost_fund',
    'Principal Outstanding': '/v1/accounting/od/fip_principal_outstanding_table1',
    'Total Outstanding Inflation Compensation': '/v1/accounting/od/fip_principal_outstanding_table2',
    'CARS Reporting': '/v1/accounting/od/fip_statement_of_account_table1',
    'Account Position Summary': '/v1/accounting/od/fip_statement_of_account_table2',
    'Transaction Detail': '/v1/accounting/od/fip_statement_of_account_table3',
    'Statements of Net Cost': '/v2/accounting/od/statement_net_cost',
    'Statements of Operations and Changes in Net Position': '/v1/accounting/od/net_position',
    'Reconciliations of Net Operating Cost and Budget Deficit': '/v1/accounting/od/reconciliations',
    'Statements of Changes in Cash Balance from Budget and Other Activities': '/v1/accounting/od/cash_balance',
    'Balance Sheets': '/v2/accounting/od/balance_sheets',
    'Statements of Long-Term Fiscal Projections': '/v1/accounting/od/long_term_projections',
    'Statements of Social Insurance': '/v1/accounting/od/social_insurance',
    'Statements of Changes in Social Insurance Amounts': '/v1/accounting/od/insurance_amounts',
    'FRN Daily Indexes': '/v1/accounting/od/frn_daily_indexes',
    'Gift Contributions to Reduce the Public Debt': '/v2/accounting/od/gift_contributions',
    'Historical Debt Outstanding': '/v2/accounting/od/debt_outstanding',
    'Historical Qualified Tax Credit Bond Interest Rates': '/v2/accounting/od/qualified_tax',
    'Interest Expense on the Public Debt Outstanding': '/v2/accounting/od/interest_expense',
    'Judgment Fund: Annual Report to Congress': '/v2/payments/jfics/jfics_congress_report',
    'Monthly State and Local Government Series (SLGS) Securities Program': '/v2/accounting/od/slgs_statistics',
    'Summary of Receipts, Outlays, and the Deficit/Surplus of the U.S. Government': '/v1/accounting/mts/mts_table_1',
    'Summary of Budget and Off-Budget Results and Financing of the U.S. Government': '/v1/accounting/mts/mts_table_2',
    'Summary of Receipts and Outlays of the U.S. Government': '/v1/accounting/mts/mts_table_3',
    'Receipts of the U.S. Government': '/v1/accounting/mts/mts_table_4',
    'Outlays of the U.S. Government': '/v1/accounting/mts/mts_table_5',
    'Means of Financing the Deficit or Disposition of Surplus by the U.S. Government': '/v1/accounting/mts/mts_table_6',
    'Analysis of Change in Excess of Liabilities of the U.S. Government': '/v1/accounting/mts/mts_table_6a',
    'Securities Issued by Federal Agencies Under Special Financing Authorities': '/v1/accounting/mts/mts_table_6b',
    'Federal Agency Borrowing Financed Through the Issue of Treasury Securities': '/v1/accounting/mts/mts_table_6c',
    'Investments of Federal Government Accounts in Federal Securities': '/v1/accounting/mts/mts_table_6d',
    'Guaranteed and Direct Loan Financing, Net Activity': '/v1/accounting/mts/mts_table_6e',
    'Receipts and Outlays of the U.S. Government by Month': '/v1/accounting/mts/mts_table_7',
    'Trust Fund Impact on Budget Results and Investment Holdings': '/v1/accounting/mts/mts_table_8',
    'Summary of Receipts by Source, and Outlays by Function of the U.S. Government': '/v1/accounting/mts/mts_table_9',
    'Receipts by Department': '/v1/accounting/od/receipts_by_department',
    'Record-Setting Auction': '/v2/accounting/od/record_setting_auction',
    'Savings Bonds Securities': '/v1/accounting/od/slgs_savings_bonds',
    'Savings Bonds Value Files': '/v2/accounting/od/sb_value',
    'Schedules of Federal Debt by Month': '/v1/accounting/od/schedules_fed_debt',
    'Schedules of Federal Debt, Fiscal Year-to-Date': '/v1/accounting/od/schedules_fed_debt_fytd',
    'Daily Activity': '/v1/accounting/od/schedules_fed_debt_daily_activity',
    'Daily Summary': '/v1/accounting/od/schedules_fed_debt_daily_summary',
    'Demand Deposit Rate': '/v1/accounting/od/slgs_demand_deposit_rates',
    'Time Deposit Rate': '/v1/accounting/od/slgs_time_deposit_rates',
    'State and Local Government Series Securities (Non-Marketable)': '/v1/accounting/od/slgs_securities',
    'Reference CPI Numbers and Daily Index Ratios Summary Table': '/v1/accounting/od/tips_cpi_data_summary',
    'Reference CPI Numbers and Daily Index Ratios Details Table': '/v1/accounting/od/tips_cpi_data_detail',
    'PDO-1 - Offerings of Regular Weekly Treasury Bills': '/v1/accounting/tb/pdo1_offerings_regular_weekly_treasury_bills',
    'PDO-2 - Offerings of Marketable Securities Other than Regular Weekly Treasury Bills': '/v1/accounting/tb/pdo2_offerings_marketable_securities_other_regular_weekly_treasury_bills',
    'OFS-1 - Distribution of Federal Securities by Class of Investors and Type of Issues': '/v1/accounting/tb/ofs1_distribution_federal_securities_class_investors_type_issues',
    'OFS-2 - Estimated Ownership of U.S. Treasury Securities': '/v1/accounting/tb/ofs2_estimated_ownership_treasury_securities',
    'USCC-1 - Amounts Outstanding and in Circulation': '/v1/accounting/tb/uscc1_amounts_outstanding_circulation',
    'USCC-2 - Amounts Outstanding and in Circulation': '/v1/accounting/tb/uscc2_amounts_outstanding_circulation',
    'FCP-1 - Weekly Report of Major Market Participants': '/v1/accounting/tb/fcp1_weekly_report_major_market_participants',
    'FCP-2 - Monthly Report of Major Market Participants': '/v1/accounting/tb/fcp2_monthly_report_major_market_participants',
    'FCP-3 - Quarterly Report of Large Market Participants': '/v1/accounting/tb/fcp3_quarterly_report_large_market_participants',
    'ESF-1 - Balances': '/v1/accounting/tb/esf1_balances',
    'ESF-2 - Statement of Net Cost': '/v1/accounting/tb/esf2_statement_net_cost',
    'FFO-5 - Internal Revenue Receipts by State': '/v1/accounting/tb/ffo5_internal_revenue_by_state',
    'FFO-6 - Customs and Border Protection Collection of Duties, Taxes, and Fees by Districts and Ports': '/v1/accounting/tb/ffo6_customs_border_protection_collections',
    'Airport and Airway Trust Fund Results of Operations': '/v1/accounting/od/airport_airway_trust_fund_results',
    'Airport and Airway Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/airport_airway_trust_fund_expected',
    'Uranium Enrichment Decontamination and Decommissioning Fund Results of Operations': '/v1/accounting/od/uranium_enrichment_decontamination_decommissioning_fund_results',
    'Uranium Enrichment Decontamination and Decommissioning Fund Expected Cond. and Results of Operations': '/v1/accounting/od/uranium_enrichment_decontamination_decommissioning_fund_expected',
    'Black Lung Disability Trust Fund Results of Operations': '/v1/accounting/od/black_lung_disability_trust_fund_results',
    'Black Lung Disability Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/black_lung_disability_trust_fund_expected',
    'Harbor Maintenance Trust Fund Results of Operation': '/v1/accounting/od/harbor_maintenance_trust_fund_results',
    'Harbor Maintenance Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/harbor_maintenance_trust_fund_expected',
    'Hazardous Substance Superfund Results of Operations': '/v1/accounting/od/hazardous_substance_superfund_results',
    'Hazardous Substance Superfund Expected Condition and Results of Operations': '/v1/accounting/od/hazardous_substance_superfund_expected',
    'Highway Trust Fund Results of Operations': '/v1/accounting/od/highway_trust_fund_results',
    'Highway Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/highway_trust_fund_expected',
    'Highway Trust Fund': '/v1/accounting/od/highway_trust_fund',
    'Inland Waterways Trust Fund Results of Operations': '/v1/accounting/od/inland_waterways_trust_fund_results',
    'Inland Waterways Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/inland_waterways_trust_fund_expected',
    'Leaking Underground Storage Tank Trust Fund Results of Operations': '/v1/accounting/od/leaking_underground_storage_tank_trust_fund_results',
    'Leaking Underground Storage Tank Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/leaking_underground_storage_tank_trust_fund_expected',
    'Nuclear Waste Fund Results of Operations': '/v1/accounting/od/nuclear_waste_fund_results',
    'Reforestation Trust Fund Results of Operations': '/v1/accounting/od/reforestation_trust_fund_results',
    'Reforestation Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/reforestation_trust_fund_expected',
    'Sport Fish Restoration and Boating Trust Fund Sport Fish Restoration Results of Operations': '/v1/accounting/od/sport_fish_restoration_boating_trust_fund_results',
    'Sport Fish Restoration and Boating Trust Fund Sport Fish Expected Cond. and Results of Operations': '/v1/accounting/od/sport_fish_restoration_boating_trust_fund_expected',
    'Oil Spill Liability Trust Fund Results of Operations': '/v1/accounting/od/oil_spill_liability_trust_fund_results',
    'Oil Spill Liability Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/oil_spill_liability_trust_fund_expected',
    'Vaccine Injury Compensation Trust Fund Results of Operations': '/v1/accounting/od/vaccine_injury_compensation_trust_fund_results',
    'Vaccine Injury Compensation Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/vaccine_injury_compensation_trust_fund_expected',
    'Wool Research, Development, and Promotion Trust Fund Results of Operations': '/v1/accounting/od/wool_research_development_promotion_trust_fund_results',
    'Wool Research, Development, and Promotion Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/wool_research_development_promotion_trust_fund_expected',
    'Agriculture Disaster Relief Trust Fund Results of Operations': '/v1/accounting/od/agriculture_disaster_relief_trust_fund_results',
    'Agriculture Disaster Relief Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/agriculture_disaster_relief_trust_fund_expected',
    'Patient Centered Outcomes Research Trust Fund Results of Operations': '/v1/accounting/od/patient_centered_outcomes_research_trust_fund_results',
    'Patient Centered Outcomes Research Trust Fund Expected Condition and Results of Operations': '/v1/accounting/od/patient_centered_outcomes_research_trust_fund_expected',
    'United States Victims of State Sponsored Terrorism Fund Results of Operations': '/v1/accounting/od/us_victims_state_sponsored_terrorism_fund_results',
    'United States Victims of State Sponsored Terrorism Fund Expected Condition and Results of Operations': '/v1/accounting/od/us_victims_state_sponsored_terrorism_fund_expected',
    'Range of Maturities': '/v1/accounting/od/tcir_annual_table_1',
    'Small Reclamation Project Act': '/v1/accounting/od/tcir_annual_table_2',
    'U.S. Army Corps of Engineers': '/v1/accounting/od/tcir_annual_table_3',
    'Bureau of Reclamation': '/v1/accounting/od/tcir_annual_table_4',
    'Mid-Dakota Rural Water System Act': '/v1/accounting/od/tcir_annual_table_5',
    'Merchant Marine Act': '/v1/accounting/od/tcir_annual_table_6',
    'Other Specific Legislation - Calendar Year': '/v1/accounting/od/tcir_annual_table_7',
    'Other Specific Legislation - Fiscal Year': '/v1/accounting/od/tcir_annual_table_8',
    'Power Marketing Administration': '/v1/accounting/od/tcir_annual_table_9',
    'Month Year Specific Maturities': '/v1/accounting/od/tcir_monthly_table_1',
    'Month Year Range of Maturities': '/v1/accounting/od/tcir_monthly_table_2',
    'Month Year Other Treasury Borrowing Authorities': '/v1/accounting/od/tcir_monthly_table_3',
    'Month Year Guam Development Fund Act': '/v1/accounting/od/tcir_monthly_table_4',
    'Month Year Department of Defense Arms Export Control Act': '/v1/accounting/od/tcir_monthly_table_5',
    'Month Year Other Specific Legislation': '/v1/accounting/od/tcir_monthly_table_6',
    'Interest Rates for the Reclamation Reform Act of 1982': '/v1/accounting/od/tcir_quarterly_table_1',
    'Interest Rates for Specific Legislation 1': '/v1/accounting/od/tcir_quarterly_table_2a',
    'Interest Rates for Specific Legislation 2': '/v1/accounting/od/tcir_quarterly_table_2b',
    'Interest Rates for National Consumer Cooperative Bank': '/v1/accounting/od/tcir_quarterly_table_3',
    'Semi-Annual Interest Rate Certification': '/v1/accounting/od/tcir_semi_annual',
    'Contract Disputes Receivables': '/v1/accounting/od/tma_contract_disputes',
    'No FEAR Act Receivables': '/v1/accounting/od/tma_no_fear',
    'Unclaimed Money': '/v1/accounting/od/tma_unclaimed_money',
    'Federal Collections': '/v1/debt/top/top_federal',
    'State Programs': '/v1/debt/top/top_state',
    'Treasury Report on Receivables Full Data': '/v2/debt/tror',
    'Collected and Outstanding Receivables': '/v2/debt/tror/collected_outstanding_recv',
    'Delinquent Debt': '/v2/debt/tror/delinquent_debt',
    'Collections on Delinquent Debt': '/v2/debt/tror/collections_delinquent_debt',
    'Written Off Delinquent Debt': '/v2/debt/tror/written_off_delinquent_debt',
    'Treasury Reporting Rates of Exchange': '/v1/accounting/od/rates_of_exchange',
    'Treasury Securities Auctions Data': '/v1/accounting/od/auctions_query',
    'Treasury Securities Upcoming Auctions': '/v1/accounting/od/upcoming_auctions',
    'U.S. Government Revenue Collections': '/v2/revenue/rcm',
    'Summary of Treasury Securities Outstanding': '/v1/debt/mspd/mspd_table_1',
    'Statutory Debt Limit': '/v1/debt/mspd/mspd_table_2',
    'Detail of Treasury Securities Outstanding': '/v1/debt/mspd/mspd_table_3',
    'Detail of Marketable Treasury Securities Outstanding': '/v1/debt/mspd/mspd_table_3_market',
    'Detail of Non-Marketable Treasury Securities Outstanding': '/v1/debt/mspd/mspd_table_3_nonmarket',
    'Historical Data': '/v1/debt/mspd/mspd_table_4',
    'Holdings of Treasury Securities in Stripped Form': '/v1/debt/mspd/mspd_table_5',
    'Paper Savings Bonds Issues, Redemptions, and Maturities by Series': '/v1/accounting/od/savings_bonds_report',
    'Matured Unredeemed Debt': '/v1/accounting/od/savings_bonds_mud',
    'Piece Information by Series': '/v1/accounting/od/savings_bonds_pcs',
    'U.S. Treasury-Owned Gold': '/v2/accounting/od/gold_reserve',
    'Unemployment Trust Fund: Quarterly Yields': '/v2/accounting/od/utf_qtr_yields',
}


def __connect_fiscaldata(datatable: str, **kwargs):
    web_params = {v: kwargs[k] for k, v in __valid_params.items() if k in kwargs and kwargs[k]}
    url = f"{__base_url}{__endpoints[datatable]}?{urlencode(web_params)}"
    res = requests.get(url).json()
    return res


def get_fiscaldata(datatable: str, **kwargs) -> pd.DataFrame:
    """
    Get FiscalData from Treasury series data.

    Args:
        datatable (str): Table name of the endpoint

    Keyword Args:
        fields (str): The fields parameter allows you to select which field(s) should be included. If
        desired fields are not specified, all fields will be returned. When a file name passed to the fields parameter is
        not available for the endpoint accessed, an error will occur.

        filter (str): Filters are used to view a subset of the data based on specific criteria. For example, you may
        want to find data that falls within a certain date range, or only show records which contain a value larger than
        a certain threshold.  Use a colon at the end of a filter parameter to pass a value or list of values. For lists
        passed as filter criteria, use a comma-separated list within parentheses. Filter for specific dates using the
        format YYYY-MM-DD. When no filters are provided, the default response will return all fields and all data.

        sort (str): The sort parameter allows a user to sort a field in ascending (least to greatest) or descending
        (greatest to least) order. The sort parameter accepts a comma-separated list of field names. When no sort
        parameter is specified, the default is to sort by the first column listed.

        page_size (int or str): The page size will set the number of rows that are returned on a request. When no
        page size parameter is specified, the default response is 100.

        page_number (int or str): The page number will set the index for the pagination, starting at 1. When no page
        number is specified, the default response is 1.

    Returns:
        pd.DataFrame: Dataframe containing the FiscalData endpoint table data.
    """

    res = __connect_fiscaldata(datatable, **kwargs)
    data, labels, dtypes = res["data"], res["meta"]["labels"], res["meta"]["dataTypes"]
    df = pd.DataFrame.from_records(data)

    for col in df.columns:
        df[col] = df[col].apply(__all_types[dtypes[col]])

    df.columns = [el for el in labels.values()]
    return df


def info_fiscaldata(database: str):
    """
    Get information of a FiscalData table.

    Args:
        datatable (str): Table name of the endpoint

    Returns:
        tuple(dict, int, int): Dictionary with the format of the table columns, the number of pages of table data (each page has up to 100 rows) and number of total rows of table data.
    """
    url = f"{__base_url}{__endpoints[database]}"
    res = requests.get(url, timeout=10).json()
    return res["meta"]["dataFormats"], res["meta"]["total-pages"], res["meta"]["total-count"]
