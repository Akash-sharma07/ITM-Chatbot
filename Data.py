# Central data source used by the chatbot for university and admission answers.
itm_University_Data = {
    "profile": {
        "name": "ITM University Gwalior",
        "type": "Private University",
        "established": 1997,
        "trust": "Samata Lok Sansthan Trust",
        "accreditation": "NAAC Grade B",
        "campus_size": "165+ Acres",
    },
    "contact": {
        "main_address": "NH-44, Bypass Turari, Jhansi Road, Gwalior (M.P.) 475001",
        "sithouli_address": "NH-75, Sithouli, Jhansi Road, Gwalior 475001",
        "toll_free": "18002700031",
        "admission_helpline": "06264865609",
        "whatsapp_erp": "9074861054",
        "official_website": "https://www.itmuniversity.ac.in",
        "mis_portal": "https://mis.itmuniversity.ac.in",
    },
    # Dates are stored in ISO format so they remain easy to read and compare.
    "admission_calendar_2026": {
        "nest_registration_start": "2026-01-05",
        "nest_registration_end": "2026-04-06",
        "correction_window": ["2026-04-13", "2026-04-14"],
        "admit_card_release": "2026-05-15",
        "exam_date": "2026-06-06",
        "result_release": "2026-09-15",
    },
    # Course records are kept consistent for direct chatbot lookup and display.
    "courses": [
        {
            "name": "BTech",
            "fees": "1,01,000 - 1,75,000",
            "duration": "4 year",
        },
        {
            "name": "MBA",
            "fees": "1,20,000 - 2,00,000",
            "duration": "2 year",
        },
        {
            "name": "BCA",
            "fees": "70,000",
            "duration": "3 year",
        },
        {
            "name": "BBA",
            "fees": "1,00,000",
            "duration": "3 year",
        },
        {
            "name": "BSc_Nursing",
            "fees": "1,50,000",
            "duration": "3 year",
        },
        {
            "name": "BSc_Agriculture",
            "fees": "1,50,000",
            "duration": "3 year",
        },
        {
            "name": "BPharm",
            "fees": "1,00,000",
            "duration": "4 year",
        },
        {
            "name": "DPharm",
            "fees": "80,000",
            "duration": "2 year",
        },
        {
            "name": "BPT",
            "fees": "1,00,000",
            "duration": "4 year",
        },
        {
            "name": "LLB",
            "fees": "30,000 - 75,000",
            "duration": "4 year",
        },
        {
            "name": "BCom_Honours",
            "fees": "65000",
            "duration": "3 year",
        },
        {
            "name": "BSc_Hons_Agri",
            "fees": "120000",
            "duration": "4 year",
        },
        {
            "name": "MSc_Agri",
            "fees": "120000",
            "duration": "2 year",
        },
    ],
    "other_fees": {
        "application_nest": 1000,
        "caution_money_refundable": 5000,
        "hostel_min": 85000,
        "hostel_max": 200000,
    },
    "placement": {
        "highest_package": "45 LPA",
        "average_package": "6 LPA",
        "median_eng_package": "5.65 LPA",
        "placement_rate": "93%",
    },
    "facilities": {
        "hostel_ranges": "85,000 to 2,00,000 INR per annum",
        "additional_charges": {
            "AC_service": 20000,
            "Non_Veg_Mess": 8000,
            "Caution_Money": "10% of Tariff",
        },
    },
    "scholarship": {
        "early_bird": "Up to 25% for admissions before April 15",
        "merit_12th": "Up to 60% fee reduction for 95%+ marks",
        "sports_tier_1": "Free Education for International level athletes",
    },
    "admission_process": {
        "steps": [
            "Fill the application form",
            "Pay the application fee",
            "Appear for required entrance/test if applicable",
            "Submit documents",
            "Confirm admission",
        ],
        "required_documents": [
            "10th marksheet",
            "12th marksheet",
            "Aadhar card",
            "Passport size photos",
            "Transfer certificate",
        ],
    },
    "eligibility": {
        "BTech": "10+2 with PCM",
        "BCA": "10+2 from a recognized board",
        "MBA": "Graduation from a recognized university",
    },
}
