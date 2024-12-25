# __init__.py content:
from .assumption_sheriff import (
    # Main classes
    StatisticalTestAssumptions,
    AssumptionChecker,
    
    # Mixins
    NormalityChecker,
    HomoscedasticityChecker,
    MonotonicityChecker,
    PairedDataChecker,
    CategoricalDataChecker,
    MultivariateRelationshipChecker,
    SurvivalDataChecker,
    ProportionalHazardsChecker,
    MultivariateNormalityChecker,
    InteractionChecker,
    PairedDifferenceChecker,
    
    # Test-specific checkers
    IndependentTTestChecker,
    RepeatedMeasuresANOVAChecker,
    LogisticRegressionChecker,
    PearsonCorrelationChecker,
    PairedTTestChecker,
    ChiSquareIndependenceChecker,
    MultipleRegressionChecker,
    TwoWayANOVAChecker,
    KaplanMeierChecker,
    CoxPHChecker,
    PoissonRegressionChecker,
    SpearmanCorrelationChecker,
    WilcoxonSignedRankChecker,
    MANOVAChecker,
    OneWayANOVAChecker,
    FactorialANOVAChecker
)


# What to expose when someone does 'from assumptionguard import *'
__all__ = [
    'StatisticalTestAssumptions',
    'AssumptionChecker',
    'NormalityChecker',
    'HomoscedasticityChecker',
    'MonotonicityChecker',
    'PairedDataChecker',
    'CategoricalDataChecker',
    'MultivariateRelationshipChecker',
    'SurvivalDataChecker',
    'ProportionalHazardsChecker',
    'MultivariateNormalityChecker',
    'InteractionChecker',
    'PairedDifferenceChecker',
    'IndependentTTestChecker',
    'RepeatedMeasuresANOVAChecker',
    'LogisticRegressionChecker',
    'PearsonCorrelationChecker',
    'PairedTTestChecker',
    'ChiSquareIndependenceChecker',
    'MultipleRegressionChecker',
    'TwoWayANOVAChecker',
    'KaplanMeierChecker',
    'CoxPHChecker',
    'PoissonRegressionChecker',
    'SpearmanCorrelationChecker',
    'WilcoxonSignedRankChecker',
    'MANOVAChecker',
    'OneWayANOVAChecker',
    'FactorialANOVAChecker'
]