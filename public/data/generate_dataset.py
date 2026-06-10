import json
import random
from datetime import datetime, timedelta

# Set random seed for deterministic generation
random.seed(42)

# Helper for dates
def date_str(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def date_only(dt):
    return dt.strftime("%Y-%m-%d")

# Start date for timeline (e.g. 2025-01-01 to 2025-05-31)
start_dt = datetime(2025, 1, 1, 9, 0, 0)

# Generate 20 Customers
customers = []
countries = ["US", "GB", "DE", "CA", "KY", "SG", "CH", "MX", "CN", "AE"]
segments = ["RETAIL", "HNW", "SMB", "CORPORATE"]
occupations = {
    "RETAIL": ["Software Engineer", "Teacher", "Nurse", "Consultant", "Unemployed", "Student"],
    "HNW": ["Venture Capitalist", "Real Estate Developer", "Private Equity Partner", "Art Dealer"],
    "SMB": ["E-commerce Retailer", "Consulting Agency", "Local Restaurant Owner", "Construction Subcontractor"],
    "CORPORATE": ["Import/Export Logistics", "Tech Start-up", "Holding Company", "Commercial Real Estate"]
}

first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", 
               "Ian", "Julia", "Kevin", "Laura", "Michael", "Nina", "Oscar", "Penelope", "Quincy", "Rachel"]
last_names = ["Smith", "Doe", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Moore", "Anderson", "Thomas",
              "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez"]

for i in range(1, 21):
    c_id = f"CUST_{i:03d}"
    c_type = "INDIVIDUAL" if i <= 15 else "CORPORATE"
    
    if c_type == "INDIVIDUAL":
        full_name = f"{first_names[i-1]} {last_names[i-1]}"
        dob = date_only(datetime(1960 + (i * 2) % 40, (i * 3) % 12 + 1, (i * 7) % 28 + 1))
        res_country = countries[i % len(countries)]
        nationality = res_country
        segment = "HNW" if i in [5, 10, 15] else "RETAIL"
        occupation = random.choice(occupations[segment])
    else:
        company_suffixes = ["LLC", "Ltd", "Holdings", "Group", "Enterprises"]
        company_names = ["Apex Import Export", "Nova Tech Ventures", "Vanguard Real Estate", "Global Logistics solutions", "Horizon Consulting"]
        full_name = f"{company_names[i - 16]} {company_suffixes[i % len(company_suffixes)]}"
        dob = None
        res_country = countries[i % len(countries)]
        nationality = "N/A"
        segment = "CORPORATE" if i in [19, 20] else "SMB"
        occupation = random.choice(occupations[segment])
        
    onboard_dt = start_dt - timedelta(days=random.randint(180, 730))
    
    # Flags
    pep_flag = False
    sanctions_flag = False
    adverse_media_flag = False
    
    # Let's set some flags for specific cases
    if i == 5: # HNW with adverse media (e.g. true positive PEP / adverse media alert)
        pep_flag = True
        adverse_media_flag = True
    elif i == 12: # Standard customer PEP false positive
        pep_flag = True
    elif i == 18: # Corp with sanctions flag
        sanctions_flag = True

    kyc_risk = "LOW"
    if pep_flag or sanctions_flag or segment == "HNW":
        kyc_risk = "HIGH"
    elif segment in ["SMB", "CORPORATE"] or adverse_media_flag:
        kyc_risk = "MEDIUM"
        
    customers.append({
        "customer_id": c_id,
        "customer_type": c_type,
        "full_name": full_name,
        "date_of_birth": dob,
        "residence_country": res_country,
        "nationality": nationality,
        "occupation_or_business_type": occupation,
        "segment": segment,
        "kyc_risk_rating": kyc_risk,
        "onboarded_date": date_only(onboard_dt),
        "pep_flag": pep_flag,
        "sanctions_flag": sanctions_flag,
        "adverse_media_flag": adverse_media_flag
    })

# Generate Accounts (25 to 35) -> Let's do exactly 30 accounts.
accounts = []
acc_types = ["CHECKING", "SAVINGS", "BUSINESS_CHECKING", "CORP_TREASURY"]
for i in range(1, 31):
    acc_id = f"ACC_{i:03d}"
    # Map to customers
    if i <= 20:
        c_id = f"CUST_{i:03d}"
    else:
        # Extra accounts for some customers
        c_id = f"CUST_{(i - 20) * 2:03d}"
        
    c = next(cust for cust in customers if cust["customer_id"] == c_id)
    
    if c["customer_type"] == "CORPORATE":
        acc_type = "CORP_TREASURY" if c["segment"] == "CORPORATE" else "BUSINESS_CHECKING"
    else:
        acc_type = "CHECKING" if i % 2 == 0 else "SAVINGS"
        
    curr = "USD" if c["residence_country"] in ["US", "KY"] else ("EUR" if c["residence_country"] in ["DE", "CH"] else "GBP")
    open_dt = datetime.strptime(c["onboarded_date"], "%Y-%m-%d") + timedelta(days=2)
    
    # Masked account number
    mask_num = f"******{1000 + i}"
    
    accounts.append({
        "account_id": acc_id,
        "customer_id": c_id,
        "account_number_masked": mask_num,
        "account_type": acc_type,
        "currency": curr,
        "opened_date": date_only(open_dt),
        "status": "ACTIVE",
        "branch_country": c["residence_country"]
    })

# Generate 30 Counterparties
counterparties = []
cp_names = [
    "Alpha Holdings", "Belize Trust Corp", "Zurich Private Bank", "Fast Pay International",
    "Global Trade Logistics", "High Risk Casino Group", "Mega Retail Wholesale", "Seychelles Nominee Ltd",
    "John Watson Consulting", "Mary Capital Partners", "Emirates Trading LLC", "Panama Shell Corp",
    "Munich Machining GmbH", "London Financial Clearing", "Tokyo Electronics", "Crypto Exchange Services",
    "Cayman Offshore Fund", "Dublin Import Co", "New York Legal Services", "Singapore Tech Dist",
    "Western Remittance Services", "East Asia Trading", "Global Wire Clearing", "Express Remitters LLC",
    "Standard Commerce Bank", "Pacifica Marine Trade", "Bermuda Asset Mgmt", "Delaware Shell Services",
    "Euro Express Trade", "Lombard Odier Swiss nominee"
]
for i in range(1, 31):
    cp_id = f"CP_{i:03d}"
    name = cp_names[i-1]
    # Assign some high risk countries and risk flags
    cp_country = ["KY", "BZ", "CH", "US", "AE", "PA", "SG", "GB", "DE"][i % 9]
    cp_type = "CORPORATE" if i <= 22 else "INDIVIDUAL"
    risk_flag = i in [2, 6, 8, 12, 17, 28] # Seychelles, Panama, Belize, Cayman, Delaware shell, etc.
    
    counterparties.append({
        "counterparty_id": cp_id,
        "name": name,
        "country": cp_country,
        "bank_name": f"{name.split()[0]} InterBank",
        "counterparty_type": cp_type,
        "risk_flag": risk_flag
    })

# Generate Transactions (around 450 transactions)
transactions = []
t_id_counter = 1

# We will generate base transactions for all accounts over 5 months.
# We also want to manually insert transaction sequences that trigger our 15-20 alerts.
# Let's define the alerts first so we can weave their transactions in!
# Typologies:
# 1. unusual cross-border transfer (True Positive, escalated)
# 2. high cash activity (False Positive, auto-cleared)
# 3. rapid movement/layering (True Positive, SAR)
# 4. structuring/smurfing (True Positive, SAR)
# 5. dormant account reactivation (False Positive, auto-cleared)
# 6. activity inconsistent with customer profile (False Positive, closed)
# 7. sanctions/adverse media related review (True Positive, escalated)
# 8. false positive noisy activity (False Positive, auto-cleared)

# Let's design 17 specific alerts. We will inject their transactions directly with specific attributes.
# Then fill the rest of the 450 transactions with normal, realistic baseline activity.

alert_templates = [
    # 1. Unusual cross-border transfer (CUST_005 - HNW)
    {
        "alert_id": "ALRT_001",
        "alert_type": "unusual cross-border transfer",
        "scenario_name": "Large Foreign Wire Outflow",
        "customer_id": "CUST_005",
        "account_id": "ACC_005",
        "severity": "HIGH",
        "status": "ESCALATED",
        "reason_summary": "Single wire transfer of $450,000 to high-risk offshore entity in Cayman Islands (CP_017).",
        "disposition": "ESCALATED_TO_L2",
        "type": "wire_out",
        "date": datetime(2025, 2, 15, 10, 30),
        "amount": 450000.0,
        "cp_id": "CP_017",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": True,
        "narrative": "INVESTMENT OVERSEAS PORTFOLIO TRANSFER"
    },
    # 2. High cash activity (CUST_002 - Retail - Teacher)
    {
        "alert_id": "ALRT_002",
        "alert_type": "high cash activity",
        "scenario_name": "Unusual Cash Deposits",
        "customer_id": "CUST_002",
        "account_id": "ACC_002",
        "severity": "MEDIUM",
        "status": "AUTO_CLEARED",
        "reason_summary": "Multiple cash deposits totaling $12,500 within 5 days. Resolved: verified sale of personal vehicle.",
        "disposition": "AUTO_CLEARED",
        "type": "cash_in_series",
        "dates": [datetime(2025, 3, 1, 9, 15), datetime(2025, 3, 3, 14, 20), datetime(2025, 3, 5, 11, 40)],
        "amounts": [4000.0, 4500.0, 4000.0],
        "cp_id": None,
        "currency": "GBP",
        "is_cash": True,
        "is_cross_border": False,
        "narratives": ["CASH DEPOSIT BRANCH", "CASH DEPOSIT BRANCH", "CASH DEPOSIT BRANCH"]
    },
    # 3. Rapid movement / layering (CUST_010 - HNW)
    {
        "alert_id": "ALRT_003",
        "alert_type": "rapid movement/layering",
        "scenario_name": "Rapid In-and-Out Funds Movement",
        "customer_id": "CUST_010",
        "account_id": "ACC_010",
        "severity": "CRITICAL",
        "status": "ESCALATED",
        "reason_summary": "Received $200,000 from Switzerland and immediately wired out $198,500 to Panama shell company within 2 hours.",
        "disposition": "SAR_CANDIDATE",
        "type": "layering_series",
        "txns": [
            {"date": datetime(2025, 4, 10, 10, 0), "amount": 200000.0, "dir": "INCOMING", "cp": "CP_003", "narrative": "LOAN PROCEEDS SH SHIELDING", "is_cb": True},
            {"date": datetime(2025, 4, 10, 11, 45), "amount": 198500.0, "dir": "OUTGOING", "cp": "CP_012", "narrative": "TRADE SERVICES REIMBURSEMENT", "is_cb": True}
        ],
        "currency": "USD"
    },
    # 4. Structuring/smurfing (CUST_007 - Retail)
    {
        "alert_id": "ALRT_004",
        "alert_type": "structuring/smurfing",
        "scenario_name": "Sub-threshold Cash Structured Deposits",
        "customer_id": "CUST_007",
        "account_id": "ACC_007",
        "severity": "HIGH",
        "status": "ESCALATED",
        "reason_summary": "Five cash deposits of exactly $9,800 or $9,900 within a 7-day window, avoiding the $10,000 CTR reporting threshold.",
        "disposition": "SAR_CANDIDATE",
        "type": "structuring_series",
        "dates": [datetime(2025, 1, 12, 10, 0), datetime(2025, 1, 13, 11, 30), datetime(2025, 1, 14, 14, 15), datetime(2025, 1, 16, 9, 45), datetime(2025, 1, 18, 15, 0)],
        "amounts": [9900.0, 9800.0, 9900.0, 9850.0, 9900.0],
        "currency": "EUR"
    },
    # 5. Dormant account reactivation (CUST_015 - HNW - no activity for a while)
    {
        "alert_id": "ALRT_005",
        "alert_type": "dormant account reactivation",
        "scenario_name": "Reactivation of Dormant Account",
        "customer_id": "CUST_015",
        "account_id": "ACC_015",
        "severity": "MEDIUM",
        "status": "AUTO_CLEARED",
        "reason_summary": "Account inactive for 180 days suddenly received a wire of $85,000. Verified: distribution from a mature estate trust.",
        "disposition": "AUTO_CLEARED",
        "type": "dormant_reactivation",
        "date": datetime(2025, 5, 2, 14, 10),
        "amount": 85000.0,
        "cp_id": "CP_027",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": True,
        "narrative": "ESTATE DISTRIBUTION TR"
    },
    # 6. Activity inconsistent with customer profile (CUST_003 - Retail - Nurse)
    {
        "alert_id": "ALRT_006",
        "alert_type": "activity inconsistent with customer profile",
        "scenario_name": "High Turnover vs Profile",
        "customer_id": "CUST_003",
        "account_id": "ACC_003",
        "severity": "MEDIUM",
        "status": "CLOSED",
        "reason_summary": "Monthly transactional turnover of $42,000 exceeds expected monthly turnover of $5,000. Verified: customer is selling an inherited property.",
        "disposition": "CLOSED_FALSE_POSITIVE",
        "type": "inconsistent_profile",
        "date": datetime(2025, 2, 22, 11, 20),
        "amount": 42000.0,
        "cp_id": "CP_019",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": False,
        "narrative": "ESCROW DEPOSIT HOME SALE PROCEEDS"
    },
    # 7. Sanctions/adverse media related review (CUST_018 - Corporate with Sanctions Flag)
    {
        "alert_id": "ALRT_007",
        "alert_type": "sanctions/adverse media related review",
        "scenario_name": "Sanctioned Entity Match",
        "customer_id": "CUST_018",
        "account_id": "ACC_018",
        "severity": "CRITICAL",
        "status": "ESCALATED",
        "reason_summary": "Screening match detected on customer beneficiary holding company, flagged as related to sanctioned entity list.",
        "disposition": "ESCALATED_TO_L2",
        "type": "sanctions_match",
        "date": datetime(2025, 4, 1, 9, 30),
        "amount": 15000.0,
        "cp_id": "CP_001",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": True,
        "narrative": "MONTHLY SERVICE FEES PAYMENT"
    },
    # 8. False positive noisy activity (CUST_001 - Retail - Software Engineer)
    {
        "alert_id": "ALRT_008",
        "alert_type": "false positive noisy activity",
        "scenario_name": "Frequent Card Transactions",
        "customer_id": "CUST_001",
        "account_id": "ACC_001",
        "severity": "LOW",
        "status": "AUTO_CLEARED",
        "reason_summary": "High volume of small-value online purchases matching typical e-commerce activity.",
        "disposition": "AUTO_CLEARED",
        "type": "noisy_activity",
        "dates": [datetime(2025, 3, i, 12, 0) for i in range(1, 11)],
        "amounts": [150.0 + i*12 for i in range(10)],
        "currency": "USD"
    },
    # 9. Unusual cross-border transfer (CUST_016 - SMB)
    {
        "alert_id": "ALRT_009",
        "alert_type": "unusual cross-border transfer",
        "scenario_name": "Suspicious Overseas Trade Wire",
        "customer_id": "CUST_016",
        "account_id": "ACC_016",
        "severity": "HIGH",
        "status": "AUTO_CLEARED",
        "reason_summary": "Wire of $120,000 sent to Belize entity. Verified: Import vendor documentation provided and verified valid invoice.",
        "disposition": "AUTO_CLEARED",
        "type": "wire_out",
        "date": datetime(2025, 3, 10, 16, 0),
        "amount": 120000.0,
        "cp_id": "CP_002",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": True,
        "narrative": "INVOICE AP-2098 SHIPMENT LOGISTICS"
    },
    # 10. High cash activity (CUST_006 - Retail)
    {
        "alert_id": "ALRT_010",
        "alert_type": "high cash activity",
        "scenario_name": "Significant ATM Withdrawals",
        "customer_id": "CUST_006",
        "account_id": "ACC_006",
        "severity": "LOW",
        "status": "AUTO_CLEARED",
        "reason_summary": "Multiple high-value ATM withdrawals over the weekend. Resolved: Checked against customer's prior vacation travel notice.",
        "disposition": "AUTO_CLEARED",
        "type": "cash_out_series",
        "dates": [datetime(2025, 5, 23, 18, 0), datetime(2025, 5, 24, 11, 0), datetime(2025, 5, 25, 14, 0)],
        "amounts": [2000.0, 2500.0, 2000.0],
        "currency": "EUR"
    },
    # 11. Activity inconsistent with profile (CUST_011 - Retail)
    {
        "alert_id": "ALRT_011",
        "alert_type": "activity inconsistent with customer profile",
        "scenario_name": "Unexplained Wire Receipt",
        "customer_id": "CUST_011",
        "account_id": "ACC_011",
        "severity": "MEDIUM",
        "status": "AUTO_CLEARED",
        "reason_summary": "Received wire of $35,000 which is 5x monthly salary. Resolved: Verified as tuition assistance from grandparents.",
        "disposition": "AUTO_CLEARED",
        "type": "wire_in",
        "date": datetime(2025, 1, 20, 11, 0),
        "amount": 35000.0,
        "cp_id": "CP_024",
        "currency": "GBP",
        "is_cash": False,
        "is_cross_border": False,
        "narrative": "FAMILY TRUST SEMESTER SUPPORT"
    },
    # 12. Structuring/smurfing (CUST_012 - Retail - PEP false positive)
    {
        "alert_id": "ALRT_012",
        "alert_type": "structuring/smurfing",
        "scenario_name": "Potential Deposit Structuring",
        "customer_id": "CUST_012",
        "account_id": "ACC_012",
        "severity": "HIGH",
        "status": "AUTO_CLEARED",
        "reason_summary": "Three cash deposits of $9,500 over 4 days. Resolved: cash intake from hobbyist collectibles fair stand.",
        "disposition": "AUTO_CLEARED",
        "type": "structuring_series",
        "dates": [datetime(2025, 2, 2, 9, 0), datetime(2025, 2, 4, 10, 30), datetime(2025, 2, 5, 15, 0)],
        "amounts": [9500.0, 9500.0, 9500.0],
        "currency": "EUR"
    },
    # 13. False positive noisy activity (CUST_019 - SMB)
    {
        "alert_id": "ALRT_013",
        "alert_type": "false positive noisy activity",
        "scenario_name": "Volume Spike in Merchant Clearing",
        "customer_id": "CUST_019",
        "account_id": "ACC_019",
        "severity": "LOW",
        "status": "AUTO_CLEARED",
        "reason_summary": "Merchant settlement volume spiked by 40% due to Black Friday/Seasonal promotion. Legitimate business activity.",
        "disposition": "AUTO_CLEARED",
        "type": "noisy_activity",
        "dates": [datetime(2025, 1, 2, 10, 0), datetime(2025, 1, 3, 10, 0), datetime(2025, 1, 4, 10, 0)],
        "amounts": [54000.0, 62000.0, 48000.0],
        "currency": "USD"
    },
    # 14. Dormant account reactivation (CUST_004 - Retail)
    {
        "alert_id": "ALRT_014",
        "alert_type": "dormant account reactivation",
        "scenario_name": "Dormant Account Reactivated by Cash Out",
        "customer_id": "CUST_004",
        "account_id": "ACC_004",
        "severity": "MEDIUM",
        "status": "AUTO_CLEARED",
        "reason_summary": "Account inactive for 210 days initiated a cash withdrawal of $10,000. Verified matching ID in branch.",
        "disposition": "AUTO_CLEARED",
        "type": "cash_out_dormant",
        "date": datetime(2025, 3, 18, 14, 0),
        "amount": 10000.0,
        "currency": "USD"
    },
    # 15. Sanctions/adverse media related review (CUST_005 - PEP adverse media)
    {
        "alert_id": "ALRT_015",
        "alert_type": "sanctions/adverse media related review",
        "scenario_name": "Adverse Media Adverse Entity Match",
        "customer_id": "CUST_005",
        "account_id": "ACC_005",
        "severity": "HIGH",
        "status": "ESCALATED",
        "reason_summary": "Outgoing wire match with media allegations concerning overseas corruption and asset concealment.",
        "disposition": "ESCALATED_TO_L2",
        "type": "wire_out",
        "date": datetime(2025, 2, 28, 11, 0),
        "amount": 95000.0,
        "cp_id": "CP_010",
        "currency": "USD",
        "is_cross_border": True,
        "is_cash": False,
        "narrative": "ADVISORY RETAINER PAYMENT"
    },
    # 16. Rapid movement/layering (CUST_020 - Corporate)
    {
        "alert_id": "ALRT_016",
        "alert_type": "rapid movement/layering",
        "scenario_name": "Round-Trip Funds Routing",
        "customer_id": "CUST_020",
        "account_id": "ACC_020",
        "severity": "HIGH",
        "status": "AUTO_CLEARED",
        "reason_summary": "Funds received from offshore entity and forwarded back to European supplier within 48 hours. Legitimate trade financing routing verified.",
        "disposition": "AUTO_CLEARED",
        "type": "layering_series",
        "txns": [
            {"date": datetime(2025, 4, 15, 9, 0), "amount": 150000.0, "dir": "INCOMING", "cp": "CP_011", "narrative": "TRADE INVOICE PREPAYMENT", "is_cb": True},
            {"date": datetime(2025, 4, 16, 15, 30), "amount": 149000.0, "dir": "OUTGOING", "cp": "CP_013", "narrative": "SUPPLIER SUB-ALLOCATION WIRE", "is_cb": True}
        ],
        "currency": "EUR"
    },
    # 17. Unusual cross-border transfer (CUST_017 - SMB)
    {
        "alert_id": "ALRT_017",
        "alert_type": "unusual cross-border transfer",
        "scenario_name": "High-Value Wire to High Risk Geo",
        "customer_id": "CUST_017",
        "account_id": "ACC_017",
        "severity": "HIGH",
        "status": "CLOSED",
        "reason_summary": "Wire of $75,000 sent to high-risk geography. Verified: Invoice and customs declaration validated for machinery purchases.",
        "disposition": "CLOSED_FALSE_POSITIVE",
        "type": "wire_out",
        "date": datetime(2025, 5, 12, 10, 15),
        "amount": 75000.0,
        "cp_id": "CP_008",
        "currency": "USD",
        "is_cash": False,
        "is_cross_border": True,
        "narrative": "EQUIPMENT PARTS BATCH 29"
    }
]

# We need to map alert_id to its list of transaction_ids
alert_txn_map = {}

# Let's start generating transactions and weaving these alert events.
# We will generate base transactions (non-alert) first for all accounts, but carefully avoiding timestamps/amounts
# that would trigger false matches, and keeping it realistic.
# Let's populate the baseline transactions.
random.seed(42)

# Baseline transactions loop
# 20 customers, 30 accounts.
# Let's do about 12 baseline transactions per account = 360 baseline transactions.
baseline_txns = []

txn_id_counter = 1
for acc in accounts:
    c_id = acc["customer_id"]
    cust = next(c for c in customers if c["customer_id"] == c_id)
    acc_id = acc["account_id"]
    curr = acc["currency"]
    
    # Establish a start time for transactions for this account
    current_time = datetime(2025, 1, 3, 10, 0, 0) + timedelta(hours=random.randint(0, 48))
    
    # Check if this customer is a corporate or retail
    is_corp = (cust["customer_type"] == "CORPORATE")
    
    # Generate ~12-14 transactions spread out over 5 months
    for _ in range(random.randint(12, 16)):
        # advance time
        current_time += timedelta(days=random.randint(7, 12), hours=random.randint(-4, 6))
        if current_time > datetime(2025, 5, 28):
            break
            
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        
        # Decide direction
        direction = "INCOMING" if random.random() < 0.4 else "OUTGOING"
        
        # Decide amount based on segment
        if cust["segment"] == "HNW":
            amount = round(random.uniform(5000, 30000), 2)
        elif cust["segment"] == "CORPORATE":
            amount = round(random.uniform(10000, 75000), 2)
        elif cust["segment"] == "SMB":
            amount = round(random.uniform(2000, 15000), 2)
        else: # RETAIL
            amount = round(random.uniform(100, 3000), 2)
            
        # Is cash or wire/transfer?
        is_cash = False
        is_cross_border = False
        txn_type = "WIRE"
        channel = "ACH"
        narrative = "Standard transfer"
        cp_id = None
        
        if is_corp:
            # Corporate txns
            if random.random() < 0.7:
                txn_type = "WIRE"
                channel = "SWIFT" if random.random() < 0.5 else "FEDWIRE"
                cp_id = f"CP_{random.randint(1, 30):03d}"
                cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
                is_cross_border = (cp["country"] != acc["branch_country"])
                narrative = f"{'PAYMENT' if direction == 'OUTGOING' else 'RECEIPT'} CORP ID-{random.randint(1000,9999)}"
            else:
                txn_type = "ACH"
                channel = "ACH"
                narrative = f"MERCHANT SETTLEMENT REGULAR"
        else:
            # Retail txns
            r_val = random.random()
            if r_val < 0.3:
                txn_type = "CASH"
                is_cash = True
                channel = "BRANCH" if random.random() < 0.5 else "ATM"
                narrative = f"CASH {'DEPOSIT' if direction == 'INCOMING' else 'WITHDRAWAL'} IN BRANCH"
            elif r_val < 0.7:
                txn_type = "DEBIT"
                channel = "POS"
                narrative = f"DEBIT PURCHASE {random.choice(['AMAZON', 'GROCERY STORE', 'GAS STATION', 'UTILITIES'])}"
                direction = "OUTGOING"
            else:
                txn_type = "WIRE"
                channel = "ONLINE_BANKING"
                cp_id = f"CP_{random.randint(21, 30):03d}" # Individual or smaller CP
                cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
                is_cross_border = (cp["country"] != acc["branch_country"])
                narrative = f"TRANSFER TO {cp['name'].upper()}"

        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(current_time),
            "txn_type": txn_type,
            "direction": direction,
            "amount": amount,
            "currency": curr,
            "channel": channel,
            "country": cp["country"] if cp_id else acc["branch_country"],
            "narrative": narrative,
            "is_cash": is_cash,
            "is_cross_border": is_cross_border
        })

# Now let's inject the alert transactions and map them.
alert_records = []
alert_txns_junctions = []

for al in alert_templates:
    c_id = al["customer_id"]
    acc_id = al["account_id"]
    curr = al["currency"]
    
    primary_txn_id = None
    linked_txn_ids = []
    
    if al["type"] == "wire_out":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        cp_id = al["cp_id"]
        cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(al["date"]),
            "txn_type": "WIRE",
            "direction": "OUTGOING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "SWIFT",
            "country": cp["country"],
            "narrative": al["narrative"],
            "is_cash": False,
            "is_cross_border": al.get("is_cross_border", True)
        })
        
    elif al["type"] == "wire_in":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        cp_id = al["cp_id"]
        cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(al["date"]),
            "txn_type": "WIRE",
            "direction": "INCOMING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "SWIFT",
            "country": cp["country"],
            "narrative": al["narrative"],
            "is_cash": False,
            "is_cross_border": al.get("is_cross_border", False)
        })

    elif al["type"] == "cash_in_series":
        # Generate several cash deposits
        dates = al["dates"]
        amounts = al["amounts"]
        narratives = al["narratives"]
        
        for idx, (dt, amt, narr) in enumerate(zip(dates, amounts, narratives)):
            txn_id = f"TXN_{txn_id_counter:04d}"
            txn_id_counter += 1
            linked_txn_ids.append(txn_id)
            if idx == len(dates) - 1:
                primary_txn_id = txn_id # Trigger txn is the last one
                
            baseline_txns.append({
                "transaction_id": txn_id,
                "customer_id": c_id,
                "account_id": acc_id,
                "counterparty_id": None,
                "timestamp": date_str(dt),
                "txn_type": "CASH",
                "direction": "INCOMING",
                "amount": amt,
                "currency": curr,
                "channel": "BRANCH",
                "country": "GB" if curr == "GBP" else "US",
                "narrative": narr,
                "is_cash": True,
                "is_cross_border": False
            })

    elif al["type"] == "cash_out_series":
        dates = al["dates"]
        amounts = al["amounts"]
        for idx, (dt, amt) in enumerate(zip(dates, amounts)):
            txn_id = f"TXN_{txn_id_counter:04d}"
            txn_id_counter += 1
            linked_txn_ids.append(txn_id)
            if idx == len(dates) - 1:
                primary_txn_id = txn_id
                
            baseline_txns.append({
                "transaction_id": txn_id,
                "customer_id": c_id,
                "account_id": acc_id,
                "counterparty_id": None,
                "timestamp": date_str(dt),
                "txn_type": "CASH",
                "direction": "OUTGOING",
                "amount": amt,
                "currency": curr,
                "channel": "ATM",
                "country": "DE" if curr == "EUR" else "US",
                "narrative": "ATM CASH WITHDRAWAL",
                "is_cash": True,
                "is_cross_border": False
            })
            
    elif al["type"] == "layering_series":
        # Rapid input and output
        txns_info = al["txns"]
        for idx, t_info in enumerate(txns_info):
            txn_id = f"TXN_{txn_id_counter:04d}"
            txn_id_counter += 1
            linked_txn_ids.append(txn_id)
            if idx == len(txns_info) - 1:
                primary_txn_id = txn_id # Outflow triggers
                
            cp = next(x for x in counterparties if x["counterparty_id"] == t_info["cp"])
            
            baseline_txns.append({
                "transaction_id": txn_id,
                "customer_id": c_id,
                "account_id": acc_id,
                "counterparty_id": t_info["cp"],
                "timestamp": date_str(t_info["date"]),
                "txn_type": "WIRE",
                "direction": t_info["dir"],
                "amount": t_info["amount"],
                "currency": curr,
                "channel": "SWIFT",
                "country": cp["country"],
                "narrative": t_info["narrative"],
                "is_cash": False,
                "is_cross_border": t_info["is_cb"]
            })
            
    elif al["type"] == "structuring_series":
        # Structured deposits
        dates = al["dates"]
        amounts = al["amounts"]
        for idx, (dt, amt) in enumerate(zip(dates, amounts)):
            txn_id = f"TXN_{txn_id_counter:04d}"
            txn_id_counter += 1
            linked_txn_ids.append(txn_id)
            if idx == len(dates) - 1:
                primary_txn_id = txn_id
                
            baseline_txns.append({
                "transaction_id": txn_id,
                "customer_id": c_id,
                "account_id": acc_id,
                "counterparty_id": None,
                "timestamp": date_str(dt),
                "txn_type": "CASH",
                "direction": "INCOMING",
                "amount": amt,
                "currency": curr,
                "channel": "ATM" if idx % 2 == 0 else "BRANCH",
                "country": "DE" if curr == "EUR" else "US",
                "narrative": "CASH DEPOSIT INTERNAL",
                "is_cash": True,
                "is_cross_border": False
            })

    elif al["type"] == "dormant_reactivation":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        cp_id = al["cp_id"]
        cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(al["date"]),
            "txn_type": "WIRE",
            "direction": "INCOMING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "SWIFT",
            "country": cp["country"],
            "narrative": al["narrative"],
            "is_cash": False,
            "is_cross_border": True
        })
        
    elif al["type"] == "inconsistent_profile":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        cp_id = al["cp_id"]
        cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(al["date"]),
            "txn_type": "WIRE",
            "direction": "INCOMING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "SWIFT",
            "country": cp["country"],
            "narrative": al["narrative"],
            "is_cash": False,
            "is_cross_border": False
        })
        
    elif al["type"] == "sanctions_match":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        cp_id = al["cp_id"]
        cp = next(x for x in counterparties if x["counterparty_id"] == cp_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": cp_id,
            "timestamp": date_str(al["date"]),
            "txn_type": "WIRE",
            "direction": "OUTGOING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "SWIFT",
            "country": cp["country"],
            "narrative": al["narrative"],
            "is_cash": False,
            "is_cross_border": True
        })
        
    elif al["type"] == "noisy_activity":
        dates = al["dates"]
        amounts = al["amounts"]
        for idx, (dt, amt) in enumerate(zip(dates, amounts)):
            txn_id = f"TXN_{txn_id_counter:04d}"
            txn_id_counter += 1
            linked_txn_ids.append(txn_id)
            if idx == len(dates) - 1:
                primary_txn_id = txn_id
                
            baseline_txns.append({
                "transaction_id": txn_id,
                "customer_id": c_id,
                "account_id": acc_id,
                "counterparty_id": None,
                "timestamp": date_str(dt),
                "txn_type": "DEBIT",
                "direction": "OUTGOING",
                "amount": amt,
                "currency": curr,
                "channel": "POS",
                "country": "US",
                "narrative": f"ONLINE TRANSACTION CLEARING VOL_{idx}",
                "is_cash": False,
                "is_cross_border": False
            })
            
    elif al["type"] == "cash_out_dormant":
        txn_id = f"TXN_{txn_id_counter:04d}"
        txn_id_counter += 1
        primary_txn_id = txn_id
        linked_txn_ids.append(txn_id)
        
        baseline_txns.append({
            "transaction_id": txn_id,
            "customer_id": c_id,
            "account_id": acc_id,
            "counterparty_id": None,
            "timestamp": date_str(al["date"]),
            "txn_type": "CASH",
            "direction": "OUTGOING",
            "amount": al["amount"],
            "currency": curr,
            "channel": "BRANCH",
            "country": "US",
            "narrative": "CASH WITHDRAWAL IN BRANCH - REACTIVATION",
            "is_cash": True,
            "is_cross_border": False
        })
        
    # Create the alert record
    alert_records.append({
        "alert_id": al["alert_id"],
        "alert_type": al["alert_type"],
        "scenario_name": al["scenario_name"],
        "customer_id": c_id,
        "account_id": acc_id,
        "primary_txn_id": primary_txn_id,
        "alert_created_at": date_str(al.get("date", al.get("dates", [datetime(2025, 3, 1)])[-1]) + timedelta(hours=2)),
        "severity": al["severity"],
        "status": al["status"],
        "reason_summary": al["reason_summary"]
    })
    
    # Create the alert transactions relationships
    for t_id in linked_txn_ids:
        rel_type = "TRIGGERING" if t_id == primary_txn_id else "SUPPORTING"
        alert_txns_junctions.append({
            "alert_id": al["alert_id"],
            "transaction_id": t_id,
            "relationship_type": rel_type
        })

# Sort transactions by timestamp to make them realistic
baseline_txns.sort(key=lambda x: x["timestamp"])

# Re-map transaction_ids so they are ordered chronologically and correctly referenced
# This guarantees deterministic order and references.
id_mapping = {}
sorted_txns = []
for idx, old_txn in enumerate(baseline_txns):
    new_id = f"TXN_{idx+1:04d}"
    id_mapping[old_txn["transaction_id"]] = new_id
    new_txn = old_txn.copy()
    new_txn["transaction_id"] = new_id
    sorted_txns.append(new_txn)

# Update transactions in other arrays
for al_rec in alert_records:
    al_rec["primary_txn_id"] = id_mapping[al_rec["primary_txn_id"]]

for junction in alert_txns_junctions:
    junction["transaction_id"] = id_mapping[junction["transaction_id"]]

# Let's map cases.
# We want linked cases for surfaced alerts.
# Disposition summary requirement:
# - mix of true positives and false positives
# - majority auto-cleared, minority escalated, 1 to 2 SAR-style cases
# Wait! Let's examine alert templates and their intended statuses.
# ALRT_001: L2 Escalated (ESCALATED_TO_L2)
# ALRT_002: Auto-cleared (AUTO_CLEARED)
# ALRT_003: Escalated -> SAR Candidate (SAR_CANDIDATE)
# ALRT_004: Escalated -> SAR Candidate (SAR_CANDIDATE)
# ALRT_005: Auto-cleared (AUTO_CLEARED)
# ALRT_006: Closed False Positive (CLOSED_FALSE_POSITIVE)
# ALRT_007: Escalated (ESCALATED_TO_L2)
# ALRT_008: Auto-cleared (AUTO_CLEARED)
# ALRT_009: Auto-cleared (AUTO_CLEARED)
# ALRT_010: Auto-cleared (AUTO_CLEARED)
# ALRT_011: Auto-cleared (AUTO_CLEARED)
# ALRT_012: Auto-cleared (AUTO_CLEARED)
# ALRT_013: Auto-cleared (AUTO_CLEARED)
# ALRT_014: Auto-cleared (AUTO_CLEARED)
# ALRT_015: L2 Escalated (ESCALATED_TO_L2)
# ALRT_016: Auto-cleared (AUTO_CLEARED)
# ALRT_017: Closed False Positive (CLOSED_FALSE_POSITIVE)

# Let's create cases for each alert!
# Wait, typically in AML systems, multiple alerts for the same customer can be aggregated into a single case,
# or we can have a case per escalated/closed alert. Let's make cases for the non-auto-cleared alerts:
# Let's make 6 Cases.
# Case 1: CUST_005 (HNW) - includes ALRT_001 and ALRT_015. Disposition: ESCALATED_TO_L2. (Investigation of large wires and PEP context).
# Case 2: CUST_010 (HNW) - includes ALRT_003. Disposition: SAR_CANDIDATE. (Rapid movement / layering).
# Case 3: CUST_007 (Retail) - includes ALRT_004. Disposition: SAR_CANDIDATE. (Structuring).
# Case 4: CUST_003 (Retail) - includes ALRT_006. Disposition: CLOSED_FALSE_POSITIVE.
# Case 5: CUST_018 (Corp) - includes ALRT_007. Disposition: ESCALATED_TO_L2. (Sanctions match review).
# Case 6: CUST_017 (SMB) - includes ALRT_017. Disposition: CLOSED_FALSE_POSITIVE.

# Wait, what about AUTO_CLEARED alerts? Do they have cases?
# "linked cases for surfaced alerts. majority auto-cleared, minority escalated, 1 to 2 SAR-style cases"
# Usually, auto-cleared alerts might not generate a Case or they might have an auto-generated case that was auto-closed.
# To be extremely clean, we can create cases for all alerts or create cases for a subset.
# Let's create a Case for all alerts or let's create a Case for all escalated/closed ones and auto-cleared ones could just remain as alerts (which is typical - alerts are auto-dismissed without a case, or we can make cases for them as well).
# Wait, "linked cases for surfaced alerts ... majority auto-cleared, minority escalated, 1 to 2 SAR-style cases"
# Let's read carefully: "majority auto-cleared, minority escalated, 1 to 2 SAR-style cases" as a requirement for "linked cases".
# So the CASES themselves should have:
# - majority auto-cleared
# - minority escalated
# - 1 to 2 SAR-style cases
# Ah! The cases themselves have those dispositions!
# Let's make cases for all alerts (or group them), where the case dispositions are:
# - Case 1: CUST_005, primary ALRT_001 (also links ALRT_015) -> Disposition: ESCALATED_TO_L2
# - Case 2: CUST_010, primary ALRT_003 -> Disposition: SAR_CANDIDATE
# - Case 3: CUST_007, primary ALRT_004 -> Disposition: SAR_CANDIDATE
# - Case 4: CUST_003, primary ALRT_006 -> Disposition: CLOSED_FALSE_POSITIVE
# - Case 5: CUST_018, primary ALRT_007 -> Disposition: ESCALATED_TO_L2
# - Case 6: CUST_017, primary ALRT_017 -> Disposition: CLOSED_FALSE_POSITIVE
# - Case 7: CUST_002, primary ALRT_002 -> Disposition: AUTO_CLEARED
# - Case 8: CUST_015, primary ALRT_005 -> Disposition: AUTO_CLEARED
# - Case 9: CUST_001, primary ALRT_008 -> Disposition: AUTO_CLEARED
# - Case 10: CUST_016, primary ALRT_009 -> Disposition: AUTO_CLEARED
# - Case 11: CUST_006, primary ALRT_010 -> Disposition: AUTO_CLEARED
# - Case 12: CUST_011, primary ALRT_011 -> Disposition: AUTO_CLEARED
# - Case 13: CUST_012, primary ALRT_012 -> Disposition: AUTO_CLEARED
# - Case 14: CUST_019, primary ALRT_013 -> Disposition: AUTO_CLEARED
# - Case 15: CUST_004, primary ALRT_014 -> Disposition: AUTO_CLEARED
# - Case 16: CUST_020, primary ALRT_016 -> Disposition: AUTO_CLEARED

# This is perfect! 16 cases total:
# - 10 AUTO_CLEARED (majority)
# - 2 CLOSED_FALSE_POSITIVE
# - 2 ESCALATED_TO_L2
# - 2 SAR_CANDIDATE
# This fits the requirement perfectly! "majority auto-cleared, minority escalated, 1 to 2 SAR-style cases".

cases = []
case_alerts = []
case_events = []
case_notes = []

# Map case_id -> alert links
# Case 1 (CUST_005): ALRT_001, ALRT_015
cases.append({
    "case_id": "CASE_001",
    "primary_alert_id": "ALRT_001",
    "customer_id": "CUST_005",
    "case_status": "OPEN",
    "disposition": "ESCALATED_TO_L2",
    "opened_at": "2025-02-15T12:30:00Z",
    "closed_at": None
})
case_alerts.append({"case_id": "CASE_001", "alert_id": "ALRT_001"})
case_alerts.append({"case_id": "CASE_001", "alert_id": "ALRT_015"})

# Case 2 (CUST_010): ALRT_003
cases.append({
    "case_id": "CASE_002",
    "primary_alert_id": "ALRT_003",
    "customer_id": "CUST_010",
    "case_status": "CLOSED",
    "disposition": "SAR_CANDIDATE",
    "opened_at": "2025-04-10T13:45:00Z",
    "closed_at": "2025-04-12T16:00:00Z"
})
case_alerts.append({"case_id": "CASE_002", "alert_id": "ALRT_003"})

# Case 3 (CUST_007): ALRT_004
cases.append({
    "case_id": "CASE_003",
    "primary_alert_id": "ALRT_004",
    "customer_id": "CUST_007",
    "case_status": "CLOSED",
    "disposition": "SAR_CANDIDATE",
    "opened_at": "2025-01-18T17:00:00Z",
    "closed_at": "2025-01-20T10:30:00Z"
})
case_alerts.append({"case_id": "CASE_003", "alert_id": "ALRT_004"})

# Case 4 (CUST_003): ALRT_006
cases.append({
    "case_id": "CASE_004",
    "primary_alert_id": "ALRT_006",
    "customer_id": "CUST_003",
    "case_status": "CLOSED",
    "disposition": "CLOSED_FALSE_POSITIVE",
    "opened_at": "2025-02-22T13:20:00Z",
    "closed_at": "2025-02-23T09:15:00Z"
})
case_alerts.append({"case_id": "CASE_004", "alert_id": "ALRT_006"})

# Case 5 (CUST_018): ALRT_007
cases.append({
    "case_id": "CASE_005",
    "primary_alert_id": "ALRT_007",
    "customer_id": "CUST_018",
    "case_status": "OPEN",
    "disposition": "ESCALATED_TO_L2",
    "opened_at": "2025-04-01T11:30:00Z",
    "closed_at": None
})
case_alerts.append({"case_id": "CASE_005", "alert_id": "ALRT_007"})

# Case 6 (CUST_017): ALRT_017
cases.append({
    "case_id": "CASE_006",
    "primary_alert_id": "ALRT_017",
    "customer_id": "CUST_017",
    "case_status": "CLOSED",
    "disposition": "CLOSED_FALSE_POSITIVE",
    "opened_at": "2025-05-12T12:15:00Z",
    "closed_at": "2025-05-13T14:00:00Z"
})
case_alerts.append({"case_id": "CASE_006", "alert_id": "ALRT_017"})

# Remaining are Auto-Cleared Cases (Case 7 to 16)
auto_cases_mapping = [
    ("ALRT_002", "CUST_002", "2025-03-05T13:40:00Z", "2025-03-05T13:45:00Z"),
    ("ALRT_005", "CUST_015", "2025-05-02T16:10:00Z", "2025-05-02T16:15:00Z"),
    ("ALRT_008", "CUST_001", "2025-03-10T14:00:00Z", "2025-03-10T14:05:00Z"),
    ("ALRT_009", "CUST_016", "2025-03-10T18:00:00Z", "2025-03-10T18:05:00Z"),
    ("ALRT_010", "CUST_006", "2025-05-25T16:00:00Z", "2025-05-25T16:05:00Z"),
    ("ALRT_011", "CUST_011", "2025-01-20T13:00:00Z", "2025-01-20T13:05:00Z"),
    ("ALRT_012", "CUST_012", "2025-02-05T17:00:00Z", "2025-02-05T17:05:00Z"),
    ("ALRT_013", "CUST_019", "2025-01-04T12:00:00Z", "2025-01-04T12:05:00Z"),
    ("ALRT_014", "CUST_004", "2025-03-18T16:00:00Z", "2025-03-18T16:05:00Z"),
    ("ALRT_016", "CUST_020", "2025-04-16T17:30:00Z", "2025-04-16T17:35:00Z")
]

for idx, (al_id, c_id, open_t, close_t) in enumerate(auto_cases_mapping):
    case_id = f"CASE_{idx+7:03d}"
    cases.append({
        "case_id": case_id,
        "primary_alert_id": al_id,
        "customer_id": c_id,
        "case_status": "CLOSED",
        "disposition": "AUTO_CLEARED",
        "opened_at": open_t,
        "closed_at": close_t
    })
    case_alerts.append({"case_id": case_id, "alert_id": al_id})

# Generate Case Events & Notes
# For non-auto-cleared cases:
# Case 1 (CUST_005) - HNW Escalated
case_events.append({
    "event_id": "EVT_001",
    "case_id": "CASE_001",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-02-15T12:30:00Z",
    "details": "Case created automatically from scenario alert: Large Foreign Wire Outflow."
})
case_events.append({
    "event_id": "EVT_002",
    "case_id": "CASE_001",
    "event_type": "ALERT_ASSOCIATION",
    "actor": "SYSTEM",
    "timestamp": "2025-02-28T13:00:00Z",
    "details": "Additional alert ALRT_015 (Adverse Media Adverse Entity Match) associated with case."
})
case_events.append({
    "event_id": "EVT_003",
    "case_id": "CASE_001",
    "event_type": "INVESTIGATION_START",
    "actor": "analyst_sarah",
    "timestamp": "2025-02-28T14:15:00Z",
    "details": "Analyst Sarah started reviewing transactions and customer PEP status."
})
case_events.append({
    "event_id": "EVT_004",
    "case_id": "CASE_001",
    "event_type": "CASE_ESCALATION",
    "actor": "analyst_sarah",
    "timestamp": "2025-03-01T10:45:00Z",
    "details": "Case escalated to Level 2 due to complex cross-border flows to Swiss & Cayman entities with PEP flags."
})

case_notes.append({
    "note_id": "NTE_001",
    "case_id": "CASE_001",
    "author": "analyst_sarah",
    "timestamp": "2025-02-28T14:30:00Z",
    "note_text": "Reviewed wire of $450,000 sent to Cayman Islands (CP_017). Customer is a High Net Worth individual with PEP flag. We also have a subsequent alert for adverse media alleging corruption in overseas investments. Customer has not provided investment registry documents. Escalating to L2 for enhanced due diligence."
})

# Case 2 (CUST_010) - Layering / SAR
case_events.append({
    "event_id": "EVT_005",
    "case_id": "CASE_002",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-04-10T13:45:00Z",
    "details": "Case created from scenario alert: Rapid In-and-Out Funds Movement."
})
case_events.append({
    "event_id": "EVT_006",
    "case_id": "CASE_002",
    "event_type": "INVESTIGATION_START",
    "actor": "analyst_mark",
    "timestamp": "2025-04-11T09:30:00Z",
    "details": "Analyst Mark initiated review of rapid layering behavior."
})
case_events.append({
    "event_id": "EVT_007",
    "case_id": "CASE_002",
    "event_type": "CASE_CLOSURE",
    "actor": "manager_helen",
    "timestamp": "2025-04-12T16:00:00Z",
    "details": "Case closed with disposition SAR_CANDIDATE."
})

case_notes.append({
    "note_id": "NTE_002",
    "case_id": "CASE_002",
    "author": "analyst_mark",
    "timestamp": "2025-04-11T11:00:00Z",
    "note_text": "Customer received $200,000 from Zurich Bank (CP_003) and immediately wired out $198,500 to a Panama shell company (CP_012) within a 2-hour window. This is highly indicative of layering/laundering proceeds of foreign origin. Suggesting immediate SAR filing."
})
case_notes.append({
    "note_id": "NTE_003",
    "case_id": "CASE_002",
    "author": "manager_helen",
    "timestamp": "2025-04-12T15:45:00Z",
    "note_text": "Agreed with analyst assessment. Transaction lacks commercial logic and shows classic integration patterns. Approved for SAR filing."
})

# Case 3 (CUST_007) - Structuring / SAR
case_events.append({
    "event_id": "EVT_008",
    "case_id": "CASE_003",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-01-18T17:00:00Z",
    "details": "Case created for potential structuring activity."
})
case_events.append({
    "event_id": "EVT_009",
    "case_id": "CASE_003",
    "event_type": "CASE_CLOSURE",
    "actor": "manager_helen",
    "timestamp": "2025-01-20T10:30:00Z",
    "details": "Case closed and SAR approved."
})

case_notes.append({
    "note_id": "NTE_004",
    "case_id": "CASE_003",
    "author": "analyst_sarah",
    "timestamp": "2025-01-19T10:00:00Z",
    "note_text": "Customer made five cash deposits just under the $10,000 reporting threshold within a week (totaling $49,350). The pattern is consistent with avoiding CTR filings. Account owner is a teacher whose profile only lists a monthly salary of $3,500. This cash volume is unexplained. Recommending SAR."
})

# Case 4 (CUST_003) - False Positive Home Sale
case_events.append({
    "event_id": "EVT_010",
    "case_id": "CASE_004",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-02-22T13:20:00Z",
    "details": "Case created from alert: High Turnover vs Profile."
})
case_events.append({
    "event_id": "EVT_011",
    "case_id": "CASE_004",
    "event_type": "CASE_CLOSURE",
    "actor": "analyst_mark",
    "timestamp": "2025-02-23T09:15:00Z",
    "details": "Case closed as CLOSED_FALSE_POSITIVE."
})

case_notes.append({
    "note_id": "NTE_005",
    "case_id": "CASE_004",
    "author": "analyst_mark",
    "timestamp": "2025-02-23T08:45:00Z",
    "note_text": "Reviewed incoming wire of $42,000. Customer provided legitimate settlement agreement showing property sale. Source of funds verified as legitimate. False positive."
})

# Case 5 (CUST_018) - Sanctions review
case_events.append({
    "event_id": "EVT_012",
    "case_id": "CASE_005",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-04-01T11:30:00Z",
    "details": "Case created from alert: Sanctioned Entity Match."
})

case_notes.append({
    "note_id": "NTE_006",
    "case_id": "CASE_005",
    "author": "analyst_sarah",
    "timestamp": "2025-04-01T14:00:00Z",
    "note_text": "Matched shareholder structure against updated EU sanctions registry. Verified 52% ownership by blocked entity. Account restricted. Escalating to L2 Sanctions compliance desk."
})

# Case 6 (CUST_017) - False Positive Trade
case_events.append({
    "event_id": "EVT_013",
    "case_id": "CASE_006",
    "event_type": "CASE_CREATION",
    "actor": "SYSTEM",
    "timestamp": "2025-05-12T12:15:00Z",
    "details": "Case created from alert: High-Value Wire to High Risk Geo."
})
case_events.append({
    "event_id": "EVT_014",
    "case_id": "CASE_006",
    "event_type": "CASE_CLOSURE",
    "actor": "analyst_mark",
    "timestamp": "2025-05-13T14:00:00Z",
    "details": "Case closed as CLOSED_FALSE_POSITIVE."
})

case_notes.append({
    "note_id": "NTE_007",
    "case_id": "CASE_006",
    "author": "analyst_mark",
    "timestamp": "2025-05-13T11:00:00Z",
    "note_text": "Wire of $75,000 sent to CP_008 (Bermuda bank). Customer is an import/export SMB. Confirmed matching commercial invoices for cargo parts import. Checked bill of lading. Valid business transactions."
})

# Add events and notes for auto-cleared cases to make them look complete and fully populated.
for idx, (al_id, c_id, open_t, close_t) in enumerate(auto_cases_mapping):
    case_id = f"CASE_{idx+7:03d}"
    
    # Event
    case_events.append({
        "event_id": f"EVT_{100+idx}",
        "case_id": case_id,
        "event_type": "CASE_CREATION",
        "actor": "SYSTEM",
        "timestamp": open_t,
        "details": f"System initiated alert {al_id}."
    })
    case_events.append({
        "event_id": f"EVT_{150+idx}",
        "case_id": case_id,
        "event_type": "AUTO_RESOLUTION",
        "actor": "SYSTEM_BOT",
        "timestamp": close_t,
        "details": "Alert cleared by rule engine auto-clear logic."
    })
    
    # Note
    case_notes.append({
        "note_id": f"NTE_{100+idx}",
        "case_id": case_id,
        "author": "SYSTEM_BOT",
        "timestamp": close_t,
        "note_text": "Auto-clear rule applied. Transaction behavior matches historical baseline / acceptable customer activity parameters."
    })

# Screening hits
screening_hits = []
# Screening hits should link to PEP/Sanctions flags
# CUST_005 has pep_flag = True, adverse_media_flag = True
screening_hits.append({
    "hit_id": "HIT_001",
    "customer_id": "CUST_005",
    "hit_type": "PEP",
    "source": "Dow Jones Watchlist",
    "matched_name": "John Smith (Senior Advisor, Ministry of Oil)",
    "match_score": 0.95,
    "status": "CONFIRMED"
})
screening_hits.append({
    "hit_id": "HIT_002",
    "customer_id": "CUST_005",
    "hit_type": "ADVERSE_MEDIA",
    "source": "World Compliance News",
    "matched_name": "John Smith",
    "match_score": 0.88,
    "status": "CONFIRMED"
})
# CUST_012 has pep_flag = True
screening_hits.append({
    "hit_id": "HIT_003",
    "customer_id": "CUST_012",
    "hit_type": "PEP",
    "source": "WorldCompliance",
    "matched_name": "Julia White (Attaché to Ministry of Culture)",
    "match_score": 0.92,
    "status": "FALSE_POSITIVE"
})
# CUST_018 has sanctions_flag = True
screening_hits.append({
    "hit_id": "HIT_004",
    "customer_id": "CUST_018",
    "hit_type": "SANCTION",
    "source": "OFAC SDN List",
    "matched_name": "Apex Import Export Holdings Ltd",
    "match_score": 1.00,
    "status": "CONFIRMED"
})

# Customer Risk Profiles
risk_profiles = []
# customer_id, expected_monthly_turnover, expected_cash_activity, expected_geographies, expected_products, customer_risk_score, risk_band, risk_rationale
for cust in customers:
    c_id = cust["customer_id"]
    is_corp = (cust["customer_type"] == "CORPORATE")
    
    if cust["segment"] == "HNW":
        expected_turnover = 100000.0
        expected_cash = 5000.0
        expected_geos = ["US", "CH", "KY", "GB"]
        expected_prods = ["WIRE", "INVESTMENTS"]
        score = 85 if cust["pep_flag"] else 60
        band = "HIGH"
        rationale = "High wealth client with international wire activity." if not cust["pep_flag"] else "PEP Status combined with high net worth wealth origin."
    elif cust["segment"] == "CORPORATE":
        expected_turnover = 500000.0
        expected_cash = 0.0
        expected_geos = ["US", "DE", "GB", "CN"]
        expected_prods = ["WIRE", "CORP_TREASURY"]
        score = 95 if cust["sanctions_flag"] else 55
        band = "HIGH" if cust["sanctions_flag"] else "MEDIUM"
        rationale = "Sanctioned Entity match on ultimate beneficial owner." if cust["sanctions_flag"] else "Standard large commercial operating account."
    elif cust["segment"] == "SMB":
        expected_turnover = 80000.0
        expected_cash = 10000.0
        expected_geos = [cust["residence_country"]]
        expected_prods = ["WIRE", "ACH", "CASH"]
        score = 45
        band = "MEDIUM"
        rationale = "Local business operation with moderate cash receipts."
    else: # RETAIL
        expected_turnover = 5000.0
        expected_cash = 2000.0
        expected_geos = [cust["residence_country"]]
        expected_prods = ["ACH", "DEBIT", "ATM"]
        score = 75 if cust["pep_flag"] else 25
        band = "HIGH" if cust["pep_flag"] else "LOW"
        rationale = "PEP match on secondary registry list." if cust["pep_flag"] else "Low risk retail banking client."

    risk_profiles.append({
        "customer_id": c_id,
        "expected_monthly_turnover": expected_turnover,
        "expected_cash_activity": expected_cash,
        "expected_geographies": expected_geos,
        "expected_products": expected_prods,
        "customer_risk_score": score,
        "risk_band": band,
        "risk_rationale": rationale
    })

# Format and write outputs
print(f"Total Transactions Generated: {len(sorted_txns)}")
print(f"Total Alerts Generated: {len(alert_records)}")
print(f"Total Cases Generated: {len(cases)}")
print(f"Total Customers: {len(customers)}")
print(f"Total Accounts: {len(accounts)}")
print(f"Total Counterparties: {len(counterparties)}")

with open("customers.json", "w") as f:
    json.dump(customers, f, indent=2)
with open("accounts.json", "w") as f:
    json.dump(accounts, f, indent=2)
with open("counterparties.json", "w") as f:
    json.dump(counterparties, f, indent=2)
with open("transactions.json", "w") as f:
    json.dump(sorted_txns, f, indent=2)
with open("alerts.json", "w") as f:
    json.dump(alert_records, f, indent=2)
with open("alert_transactions.json", "w") as f:
    json.dump(alert_txns_junctions, f, indent=2)
with open("cases.json", "w") as f:
    json.dump(cases, f, indent=2)
with open("case_alerts.json", "w") as f:
    json.dump(case_alerts, f, indent=2)
with open("case_events.json", "w") as f:
    json.dump(case_events, f, indent=2)
with open("case_notes.json", "w") as f:
    json.dump(case_notes, f, indent=2)
with open("screening_hits.json", "w") as f:
    json.dump(screening_hits, f, indent=2)
with open("customer_risk_profiles.json", "w") as f:
    json.dump(risk_profiles, f, indent=2)
