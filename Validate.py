def measure(validation, tree):
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    accuracy = 0.0
    precision = 0.0
    recall = 0.0
    specificity = 0.0

    for i in validation:
        var = tree.classify(i)

        if var == i[0] and var == 1:
            tp = tp + 1
        if var == i[0] and var == 0:
            tn = tn + 1
        if var != i[0] and var == 1:
            fp = fp + 1
        if var != i[0] and var == 0:
            fn = fn + 1

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)

    print "Accuracy: ", accuracy
    print "Precision:", precision
    print "Recall:   ", recall
    print "Specificity:", specificity
