def lead_score(product):

    keywords = [
        "steel",
        "electronics",
        "solar",
        "medical",
        "furniture",
        "construction"
    ]

    for word in keywords:
        if word in product.lower():
            return "High"

    return "Medium"