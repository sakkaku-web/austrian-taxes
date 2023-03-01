tax_values = {
    2023: {
        'insurance-work': {
            475.86: 0.1512,
            1790: 0.1612,
            1953: 0.1712,
            2117: 0.1812,
            5550: 1005.66,
        },
        'insurance-other-work': {
            475.86: 0.1412,
            1790: 0.1512,
            1953: 0.1612,
            2117: 0.1712,
            5550: 1900.32,
        },
        'insurance-self': {
            'percentage': 26.83,
            'absolute': 10.97 * 12, # Unfallversicherung
            'min_income': 500.91 * 12,
            'max_income': 6825 * 12
        },
        'tax-work': {  # percent same as tax-self
            985.42: 197.08,
            1605.50: 357.63,
            2683.92: 652.86,
            5184.33: 1015.77,
            7771: 1171.19,
            83_344.33: 5238.97,
        },
        'tax-other': {
            620: 0.06,
            24_380: 0.27,
            25_000: 0.3575,
            33_333: 0.5,  # Unsure if 50% is correct, related to Jahressechstel
        },
        'tax-self': {
            11_000: 0.2,
            18_000: 0.3,
            31_000: 0.41,
            60_000: 0.48,
            90_000: 0.50,
            1_000_000: 0.55,
        },
        'flat': {
            'werbung': 132,
            'sonder': 60,
            'verkehr': 421,
            'free': 730,
            'partial': 1460
        }
    }
}
