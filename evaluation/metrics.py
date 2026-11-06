
def calculate_precision(expected, predicted):
    """
    Precision = Correctly predicted issues / Total predicted issues
    """
    true_positive = len(expected & predicted)
    false_positive = len(predicted - expected)

    if true_positive + false_positive == 0:
        return 0.0

    return true_positive / (true_positive + false_positive)


def calculate_recall(expected, predicted):
    """
    Recall = Correctly predicted issues / Total expected issues
    """
    true_positive = len(expected & predicted)
    false_negative = len(expected - predicted)

    if true_positive + false_negative == 0:
        return 0.0

    return true_positive / (true_positive + false_negative)


def calculate_f1(precision, recall):
    """
    F1-score = Harmonic mean of precision and recall
    """
    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


def calculate_metrics(expected, predicted):
    """
    Calculate precision, recall, and F1-score.
    """

    precision = calculate_precision(expected, predicted)
    recall = calculate_recall(expected, predicted)
    f1_score = calculate_f1(precision, recall)

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4)
    }
expected = {"sql_injection", "resource_leak"}
predicted = {"sql_injection", "bare_except"}

print(calculate_metrics(expected, predicted))