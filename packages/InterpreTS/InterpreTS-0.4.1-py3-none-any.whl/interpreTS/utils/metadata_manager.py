from ..utils.feature_loader import Features

def load_metadata():
    return {
        Features.LENGTH: {
            'level': 'easy',
            'description': 'Number of points in the window.'
        },
        Features.MEAN: {
            'level': 'easy',
            'description': 'Mean value within the window.'
        },
        Features.VARIANCE: {
            'level': 'moderate',
            'description': 'Variance of the signal within the window.'
        },
        Features.ENTROPY: {
            'level': 'advanced',
            'description': 'Degree of randomness or disorder in the window.'
        },
        Features.SPIKENESS: {
            'level': 'moderate',
            'description': 'Measure of sudden jumps or spikes in the signal.'
        },
        Features.SEASONALITY_STRENGTH: {
            'level': 'advanced',
            'description': 'Strength of seasonal patterns within the signal.'
        },
        Features.STABILITY: {
            'level': 'moderate',
            'description': 'Measure of consistency in the signal values.'
        },
        Features.PEAK: {
                'level': 'easy',
                'description': 'The maximum value in the window.'
        },
        Features.TROUGH: {
                'level': 'easy',
                'description': 'The minimum value in the window.'
        },
        Features.DISTANCE_TO_LAST_TREND_CHANGE: {
            'level': 'moderate',
            'description': 'Distance (in terms of indices) to the last detected trend change in the window.'
        },
        Features.ABSOLUTE_ENERGY: {
                'level': 'moderate',
                'description': 'Total energy of the signal in the window.'
            },
        Features.ABOVE_9TH_DECILE: {
            'level': 'moderate',
            'description': 'Fraction of values in the window above the 9th decile of the training data, representing the presence of extreme high values.'
        },
        Features.BELOW_1ST_DECILE: {
            'level': 'moderate',
            'description': 'Fraction of values in the window below the 1st decile of the training data, representing the presence of extreme low values.'
        },
        Features.BINARIZE_MEAN: {
            'level': 'moderate',
            'description': 'Binary value indicating whether the signal mean exceeds a threshold.'
        },
        Features.CROSSING_POINTS: {
            'level': 'easy',
            'description': 'Number of times the signal crosses its mean.'
        },
        Features.FLAT_SPOTS: {
            'level': 'easy',
            'description': 'Number of segments with constant values in the signal.'
        },
        Features.HETEROGENEITY: {
            'level': 'moderate',
            'description': 'Coefficient of variation, representing the ratio of standard deviation to mean, indicating the relative variability in the time series.'
        },
        Features.OUTLIERS_IQR: {
            'level': 'moderate',
            'description': 'Percentage of values in the window that are classified as outliers based on the Interquartile Range (IQR) method.'
        },
        Features.OUTLIERS_STD: {
            'level': 'moderate',
            'description': 'Percentage of values in the window that are more than 3 standard deviations away from the mean, indicating extreme deviations.'
        },
        Features.STD_1ST_DER: {
            'level': 'moderate',
            'description': 'Standard deviation of the first derivative of the signal.'
        },
        Features.DOMINANT: {
            'level': 'moderate',
            'description': 'The dominant value of the time series histogram, representing the most frequent range of values within the specified bins.'
        },
        Features.MEAN_CHANGE: {
            'level': 'moderate',
            'description': 'The rate of change in the rolling mean over time, capturing trends or shifts in the time series.'
        },
        Features.TREND_STRENGTH: {
            'level': 'moderate',
            'description': 'The R-squared value from a linear regression, representing the strength and consistency of the trend in the time series.'
        },
        Features.SIGNIFICANT_CHANGES: {
            'level': 'moderate',
            'description': 'Proportion of significant increases or decreases in the time series, based on deviations from the interquartile range (IQR) of differences between consecutive values.'
        },
        Features.MISSING_POINTS: {
            'level': 'easy',
            'description': 'Proportion or count of missing data points in the window.'
        },
        Features.VARIABILITY_IN_SUB_PERIODS: {
            'level': 'moderate',
            'description': 'Variance calculated within sub-periods of a time series, providing a measure of variability across fixed-size windows.'
        },
        Features.CHANGE_IN_VARIANCE: {
            'level': 'moderate',
            'description': 'Change in variance over time, calculated as the difference between rolling variances across consecutive windows.'
        },
        Features.LINEARITY:{
            'level': 'moderate',
            'description': 'Measure of how well the time series can be approximated by a linear trend, quantified using the R-squared value from linear regression.'
        }
    } 

def generate_feature_descriptions(self, extracted_features):
    """
    Generate textual descriptions for extracted features.

    Parameters
    ----------
    extracted_features : dict
        A dictionary where keys are feature names and values are their calculated values.

    Returns
    -------
    dict
        A dictionary where keys are feature names and values are textual descriptions.
    """
    descriptions = {}
    feature_metadata = self.load_metadata()
    for feature_name, feature_value in extracted_features.items():
        if feature_name in feature_metadata:
            metadata = self.feature_metadata[feature_name]
            description = metadata['description']
            descriptions[feature_name] = (
                f"Feature '{feature_name}': {description} Value: {feature_value}."
            )
        else:
            descriptions[feature_name] = (
                f"Unknown feature: '{feature_name}'. Value: {feature_value}."
            )
    return descriptions