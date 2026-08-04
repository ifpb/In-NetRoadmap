import numpy as np
from scipy.stats import norm
from sklearn.naive_bayes import GaussianNB

def extract_model(
    model: GaussianNB, 
    features: list[str], 
    feature_max_vals: dict[str, int] = None
) -> dict:
    """
    Extracts statistical parameters from a Gaussian Naive Bayes model, 
    calculates probabilities for all possible feature values, quantizes them to 0-100, 
    and groups them into ranges for P4 table generation.
    """
    if feature_max_vals is None:
        # Default to 16-bit max value (65535) if no limits are provided
        feature_max_vals = {f: 65535 for f in features}

    classes = model.classes_
    means = model.theta_
    variances = model.var_

    res = {
        "classes": classes.tolist(),
        "features": features,
        "rules": {}
    }

    # Helper function to compress flat arrays into P4-friendly ranges
    def compress_to_ranges(quantized_array):
        ranges = []
        start_idx = 0
        current_val = quantized_array[0]
        
        for i in range(1, len(quantized_array)):
            if quantized_array[i] != current_val:
                ranges.append({"start": start_idx, "end": i - 1, "value": int(current_val)})
                start_idx = i
                current_val = quantized_array[i]
                
        # Append the final range
        ranges.append({"start": start_idx, "end": len(quantized_array) - 1, "value": int(current_val)})
        return ranges

    # Iterate over each feature to generate probability ranges
    for idx_feature, feature in enumerate(features):
        res["rules"][feature] = {}
        max_val = feature_max_vals.get(feature, 65535)
        
        # Generate an array of all possible discrete values for this feature
        x_values = np.arange(0, max_val + 1)
        feature_pdfs = {}
        max_pdf_across_classes = 0.0

        # Calculate the PDF (Probability Density Function) for each class
        for idx_class, cls in enumerate(classes):
            mu = means[idx_class, idx_feature]
            # Add a tiny epsilon to std to prevent division by zero in zero-variance features
            std = np.sqrt(variances[idx_class, idx_feature]) + 1e-9 
            
            pdf_values = norm.pdf(x_values, mu, std)
            feature_pdfs[cls] = pdf_values
            
            if np.max(pdf_values) > max_pdf_across_classes:
                max_pdf_across_classes = np.max(pdf_values)

        # Quantize the PDF values to a 0-100 scale and compress into ranges
        for cls in classes:
            if max_pdf_across_classes > 0:
                # Normalize relative to the highest probability found for this feature 
                # to keep the mathematical proportion between classes intact
                quantized = np.round((feature_pdfs[cls] / max_pdf_across_classes) * 100).astype(int)
            else:
                quantized = np.zeros_like(x_values, dtype=int)
            
            # Compress the 65k+ array into grouped ranges
            res["rules"][feature][cls] = compress_to_ranges(quantized)

    return res
