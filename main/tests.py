from classifier import Classifier
from fuzzy_distance import calc_fuzzy_dist
import config

def testClassifierInit():
    pass

def testFuzzyDistance():
    clf = Classifier()
    fuzzy_calc_filter = clf.filters[2]
    assert calc_fuzzy_dist("ITALY", "ITLAY"), 2

def testClassifier():
    clf = Classifier()
    sample_inputs = [
        "France",
        "Colombia",
        "USA",
        "U.S.A.",
        "United States",
        "Bnited States",
        "   Argentina",
        "Caneda",
        "Uk",
        "Fraace",
        "Austraia",
        "Germay",
        "Chia",
        "Itlay",
        "Brasil",
        "Spai",
        "Japa",
        "Australa",
        "Mexco",
        "Inda",
        "Argentia",
        "Russa",
        "Thailad",
        "Egy",
        "Cuba",
        "Nigeri",
        "Switzeland",
        "Canama",
        "Panada",
        "Intentional Failure",
    ]

    print(f"")
    print(f"Testing simple inputs on the newly implemented Classifier.applyFilterStack() method...")
    print(f"")

    total_confidence = 0
    num_well_placed = 0
    for sample in sample_inputs:
        probable_country, confidence = clf.applyFilterStack(sample)
        total_confidence += confidence
        if confidence >= config.WELL_PLACED_CONFIDENCE_THRESHOLD: num_well_placed += 1
        print(f"{sample.strip()} mapped to {probable_country} with {confidence}% confidence.")

    print(f"")
    print(f"OVERALL CONFIDENCE: {total_confidence/len(sample_inputs):.2f}")
    print(f"Percentage of Input mapped with at least {config.WELL_PLACED_CONFIDENCE_THRESHOLD}% Confidence: {num_well_placed/len(sample_inputs)*100:.2f}")

    print(f"")
    print(f"Done.")


testClassifier()