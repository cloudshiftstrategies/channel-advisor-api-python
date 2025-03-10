def get_restricted_words_context() -> str:
    return """
1. Medical conditions and treatments (e.g., AIDS, Cancer, Diabetes, diseases, treatments, cures)
2. Marketing superlatives (e.g., "best", "perfect", "top", "guaranteed", "proven")
3. Time-sensitive offers (e.g., "limited time", "sale", "closeout", "supplies won't last")
4. Shipping claims (e.g., "free shipping", "ships faster", "UPS", "FedEx")
5. Price/value claims (e.g., "best price", "wholesale", "save money", "unbeatable")
6. Environmental claims (e.g., "biodegradable", "eco-friendly", "natural", "green")
7. Quality absolutes (e.g., "100%", "flawless", "professional quality")
8. Health/safety claims (e.g., "antibacterial", "sanitizes", "toxic-free")
9. Cultural appropriation terms (e.g., "indian", "native american", "tribes")
10. Generic marketing buzzwords (e.g., "authentic", "certified", "validated")
"""


# Keep original list for validation purposes
restricted_words_list = [
    "100% natural",
    "100% quality guaranteed",
    "Acquired Immune Deficiency Syndrome",
    "ADD",
    "added value",
    "ADHD",
    "AIDS",
    "All Natural",
    "ALS",
    "Alzheimers",
    "Antibacterial",
    "Anti-bacterial",
    "antifungal",
    "Anti-Fungal",
    "Anti-Microbial",
    "anxiety",
    "approved",
    "Arrive faster",
    "Attention Deficit Disorder Drug",
    "Authentic",
    "award winning",
    "bacteria",
    "best deal",
    "Best price",
    "Best seller",
    "Best selling",
    "big sale",
    "biodegradable",
    "biological contaminants",
    "bpa free",
    "brain",
    "brand new",
    "buy now",
    "buy with confidence",
    "Cancer",
    "Cancroid",
    "Cataract",
    "cataract",
    "certified",
    "Chlamydia",
    "closeout",
    "close-out",
    "CMV",
    "compostable",
    "concussion",
    "Coronavirus",
    "covid",
    "COVID-19",
    "Crabs",
    "Crystic Fibrosis",
    "cure",
    "Cytomegalovirus",
    "decomposable",
    "degradable",
    "Dementia",
    "Depression",
    "detoxification",
    "detoxify",
    "Diabetes",
    "Diabetic",
    "Diabetic Neuropathy",
    "Discounted price",
    "disease",
    "diseases",
    "don’t miss out",
    "dotoxifying",
    "eco friendly",
    "ecofriendly",
    "eco-friendly",
    "ensure",
    "environmentally friendly",
    "etc.",
    "Face Mask",
    "Face Shield",
    "fall sale",
    "fda",
    "FDA Approval",
    "FedEx",
    "filter",
    "flawless",
    "Flu",
    "free gift",
    "free shipping",
    "Free shipping Guaranteed",
    "fungal",
    "Fungicide",
    "Fungicides",
    "fungus",
    "gift idea",
    "Glaucoma",
    "Gororrhea",
    "Great as",
    "Great for",
    "green",
    "guarantee",
    "guaranteed",
    "Hassle free",
    "heal",
    "Hepatitis A",
    "Hepatitis B",
    "Hepatitis C",
    "Herpes",
    "Herpes Simplex Virus 1",
    "Herpes Simplex Virus 2",
    "highest rated",
    "HIV",
    "Hodgkins Lymphoma",
    "home compostable",
    "hot item",
    "HPV",
    "HSV1",
    "HSV2",
    "huge sale",
    "Human Immunodeficiency Virus",
    "Human Papiloma Virus",
    "imported from",
    "indian",
    "inflammation",
    "Influenza",
    "Kidney Disease",
    "Lasting quality",
    "LGV",
    "limited time offer",
    "Liver disease",
    "Lupus",
    "Lymphogranuloma Venereum",
    "Lymphoma",
    "Made in",
    "mail rebate",
    "make excellent",
    "makes awesome",
    "makes great",
    "makes perfect",
    "makes spectacular",
    "makes the best",
    "makes wonderful",
    "marine degradable",
    "massive sale",
    "Meningitis",
    "mildew",
    "moisture wicking",
    "mold",
    "money back guarantee",
    "Mono",
    "Mononucleosis",
    "mould",
    "mould resistant",
    "mould spores",
    "Multiple Sclerosis",
    "multiple sclerosis",
    "Muscular Dystrophy",
    "Mycoplasma Genitalium",
    "Nano Silver",
    "native american",
    "Native American Indian or tribes",
    "natural",
    "newest version",
    "NGU",
    "non toxic",
    "noncorrosive",
    "Nongonococcal Urethritis",
    "non-toxi",
    "non-toxic",
    "now together",
    "On sale",
    "ortholite",
    "over- stock",
    "overstock",
    "parasitic",
    "Parkinson",
    "Parkinsons",
    "parkinsons",
    "patented",
    "peal",
    "Pelvic Inflammatory Disease",
    "Perfect for",
    "Perfect gift",
    "pesticide",
    "pesticides",
    "PID",
    "platinum",
    "plus free",
    "Professional quality",
    "promise",
    "proven",
    "Public lice",
    "quality",
    "Ready to ship",
    "recommended by",
    "remedies",
    "remedy",
    "Retail box",
    "SAD",
    "sad",
    "sanitize",
    "sanitizes",
    "Satisfaction",
    "Save $",
    "Save cash",
    "Save money",
    "scabies",
    "Seasonal Affective Disorder",
    "seen on tv",
    "Ships faster",
    "shop with confidence",
    "Special offer",
    "Special promo",
    "spring sale",
    "Stroke",
    "stroke",
    "summer sale",
    "super sale",
    "supplies won’t last",
    "TBIs",
    "tbis",
    "tested",
    "tested",
    "The Clap",
    "the clap",
    "Top notch",
    "top quality",
    "top rated",
    "top selling",
    "toxic",
    "toxin",
    "toxins",
    "Traumatic Brain Injuries",
    "treat",
    "treatment",
    "tribes",
    "Trich",
    "trichomoniasis",
    "tricht",
    "Tumor",
    "unbeatable price",
    "UPS",
    "Used",
    "uv protectant",
    "validated",
    "viral",
    "virus",
    "viruses",
    "Washable",
    "weight loss",
    "wholesale price",
    "winter sale",
    "Within hours",
    "worlds best",
]
