import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Dict, List, Optional, Tuple, Union, Callable
from abc import ABC, abstractmethod
import warnings
import lifelines


class AssumptionChecker(ABC):
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
    
    @abstractmethod
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:

        pass

    @abstractmethod
    def get_alternative_tests(self) -> List[str]:
        pass

class NormalityChecker:
    
    def check_normality(self, data: pd.DataFrame, variables: List[str], 
                       alpha: float) -> Dict:
        results = {}
        for var in variables:
            clean_data = data[var].dropna()
            shapiro_stat, shapiro_p = stats.shapiro(clean_data)
            skew = stats.skew(clean_data)
            kurt = stats.kurtosis(clean_data)
            
            results[var] = {
                'shapiro_p_value': shapiro_p,
                'skewness': skew,
                'kurtosis': kurt,
                'is_normal': shapiro_p > alpha and abs(skew) < 2 and abs(kurt) < 7
            }
        return results

class HomoscedasticityChecker:
    
    def check_homoscedasticity(self, data: pd.DataFrame, variables: List[str],
                              group_column: str, alpha: float) -> Dict:
        results = {}
        for var in variables:
            groups = [group for _, group in data.groupby(group_column)[var]]
            levene_stat, p_value = stats.levene(*groups)
            
            results[var] = {
                'levene_p_value': p_value,
                'is_homoscedastic': p_value > alpha
            }
        return results

class IndependentTTestChecker(AssumptionChecker, NormalityChecker, HomoscedasticityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              group_column: Optional[str] = None, **kwargs) -> Dict:
        results = {
            'test_type': 'Independent t-test',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check normality
        norm_results = self.check_normality(data, variables, self.alpha)
        results['details']['normality'] = norm_results
        
        # Check homoscedasticity
        homo_results = self.check_homoscedasticity(data, variables, group_column, self.alpha)
        results['details']['homoscedasticity'] = homo_results
        
        # Check sample size
        group_sizes = data.groupby(group_column).size()
        min_group_size = group_sizes.min()
        
        results['details']['sample_size'] = {
            'min_group_size': min_group_size,
            'requirement_met': min_group_size >= 30
        }
        
        # Update assumptions_met and warnings
        self._update_results(results, norm_results, homo_results, min_group_size)
        
        return results
    
    def _update_results(self, results: Dict, norm_results: Dict, 
                       homo_results: Dict, min_group_size: int) -> None:
        for var, details in norm_results.items():
            if not details['is_normal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates normality assumption "
                    f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                )
        
        for var, details in homo_results.items():
            if not details['is_homoscedastic']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates homoscedasticity assumption "
                    f"(Levene's test p={details['levene_p_value']:.4f})"
                )
        
        if min_group_size < 30:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size in some groups "
                f"(minimum {min_group_size} < required 30)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Mann-Whitney U test', 'Welch\'s t-test']

class RepeatedMeasuresANOVAChecker(AssumptionChecker, NormalityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              subject_column: str, **kwargs) -> Dict:
        results = {
            'test_type': 'Repeated Measures ANOVA',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check normality
        norm_results = self.check_normality(data, variables, self.alpha)
        results['details']['normality'] = norm_results
        
        # Check sphericity using Mauchly's test
        try:
            wide_data = data.pivot(index=subject_column, 
                                 columns=kwargs.get('time_column'),
                                 values=variables[0])
            mauchly_result = self._check_sphericity(wide_data)
            results['details']['sphericity'] = mauchly_result
        except:
            results['details']['sphericity'] = {
                'error': 'Could not compute sphericity test'
            }
            results['warnings'].append(
                'Could not check sphericity assumption. Ensure data is properly formatted.'
            )
        
        # Update results
        self._update_results(results, norm_results)
        
        return results
    
    def _check_sphericity(self, wide_data: pd.DataFrame) -> Dict:
        # Implement Mauchly's test of sphericity
        # This is a simplified version - in practice you'd want to use
        # a proper implementation of Mauchly's test
        differences = wide_data.diff(axis=1).dropna(axis=1)
        covariance_matrix = differences.cov()
        
        return {
            'warning': 'Sphericity test implementation is simplified',
            'covariance_matrix': covariance_matrix.to_dict()
        }
    
    def _update_results(self, results: Dict, norm_results: Dict) -> None:
        for var, details in norm_results.items():
            if not details['is_normal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates normality assumption "
                    f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Friedman test', 'Mixed-effects model']

class LogisticRegressionChecker(AssumptionChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              dependent_var: str, **kwargs) -> Dict:
        results = {
            'test_type': 'Logistic Regression',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }  
        
        # Check multicollinearity
        predictors = [var for var in variables if var != dependent_var]
        X = data[predictors]
        vif_results = self._check_multicollinearity(X)
        results['details']['multicollinearity'] = vif_results
        
        # Check linearity of continuous variables with logit
        if len(predictors) > 0:
            linearity_results = self._check_linearity_with_logit(
                data, predictors, dependent_var
            )
            results['details']['linearity_with_logit'] = linearity_results
        
        # Check sample size
        sample_size_results = self._check_sample_size(
            data, dependent_var, len(predictors)
        )
        results['details']['sample_size'] = sample_size_results
        
        # Update results
        self._update_results(results, vif_results, sample_size_results)
        
        return results
    
    def _check_multicollinearity(self, X: pd.DataFrame) -> Dict:
        X = sm.add_constant(X)
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                          for i in range(X.shape[1])]
        return vif_data.set_index('Variable')['VIF'].to_dict()
    
    def _check_linearity_with_logit(self, data: pd.DataFrame, 
                                   predictors: List[str],
                                   dependent_var: str) -> Dict:
        results = {}
        for pred in predictors:
            if data[pred].dtype in ['int64', 'float64']:
                # Add implementation of Box-Tidwell test here
                results[pred] = {
                    'warning': 'Linearity with logit test not implemented'
                }
        return results
    
    def _check_sample_size(self, data: pd.DataFrame, dependent_var: str,
                          n_predictors: int) -> Dict:
        # Rule of thumb: minimum 10 events per predictor variable
        n_events = min(data[dependent_var].value_counts())
        events_per_predictor = n_events / n_predictors if n_predictors > 0 else float('inf')
        
        return {
            'events_per_predictor': events_per_predictor,
            'requirement_met': events_per_predictor >= 10
        }
    
    def _update_results(self, results: Dict, vif_results: Dict,
                       sample_size_results: Dict) -> None:
        # Check VIF values
        for var, vif in vif_results.items():
            if vif > 10:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"High multicollinearity detected for '{var}' (VIF={vif:.2f})"
                )
        
        # Check sample size
        if not sample_size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient events per predictor "
                f"({sample_size_results['events_per_predictor']:.1f} < required 10)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Penalized regression (Ridge, Lasso)', 'Decision trees']

class MonotonicityChecker:
    
    def check_monotonicity(self, data: pd.DataFrame, variables: List[str]) -> Dict:

        results = {}
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                spearman_corr, p_value = stats.spearmanr(
                    data[var1].dropna(), 
                    data[var2].dropna()
                )
                
                x = data[var1].dropna()
                y = data[var2].dropna()
                
                try:
                    coeffs = np.polyfit(x, y, 2)
                    quad_strength = abs(coeffs[0] / (coeffs[1] + 1e-10))
                    potentially_non_monotonic = quad_strength > 0.5
                except:
                    potentially_non_monotonic = False
                
                results[f"{var1}_vs_{var2}"] = {
                    'spearman_correlation': spearman_corr,
                    'spearman_p_value': p_value,
                    'potentially_non_monotonic': potentially_non_monotonic,
                    'is_monotonic': abs(spearman_corr) > 0.3 and not potentially_non_monotonic,
                    
                    'correlation_strength': abs(spearman_corr),
                    
                    'ties_first_var': {
                        'unique_values': len(np.unique(data[var1])),
                        'tied_values_pct': (len(data[var1]) - len(np.unique(data[var1]))) / len(data[var1]) * 100
                    },
                    'ties_second_var': {
                        'unique_values': len(np.unique(data[var2])),
                        'tied_values_pct': (len(data[var2]) - len(np.unique(data[var2]))) / len(data[var2]) * 100
                    }
                }
            
        return results

class PearsonCorrelationChecker(AssumptionChecker, NormalityChecker, MonotonicityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Pearson Correlation',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check normality
        norm_results = self.check_normality(data, variables, self.alpha)
        results['details']['normality'] = norm_results
        
        # Check monotonic relationship
        mono_results = self.check_monotonicity(data, variables)
        results['details']['monotonicity'] = mono_results
        
        # Check sample size
        size_results = self._check_sample_size(data)
        results['details']['sample_size'] = size_results
        
        # Check for outliers using z-score method
        outlier_results = self._check_outliers(data, variables)
        results['details']['outliers'] = outlier_results
        
        # Update results based on all checks
        self._update_results(results, norm_results, mono_results, 
                           size_results, outlier_results)
        
        return results
    
    def _check_sample_size(self, data: pd.DataFrame) -> Dict:
        # Rule of thumb: at least 25 pairs for moderate correlations
        n = len(data)
        return {
            'sample_size': n,
            'requirement_met': n >= 25
        }
    
    def _check_outliers(self, data: pd.DataFrame, 
                       variables: List[str]) -> Dict:
        results = {}
        for var in variables:
            clean_data = data[var].dropna()
            z_scores = np.abs(stats.zscore(clean_data))
            
            results[var] = {
                'n_outliers': (z_scores > 3).sum(),
                'has_significant_outliers': (z_scores > 3).sum() > len(clean_data) * 0.05
            }
        return results
    
    def _update_results(self, results: Dict, norm_results: Dict,
                       mono_results: Dict, size_results: Dict,
                       outlier_results: Dict) -> None:
        # Check normality
        for var, details in norm_results.items():
            if not details['is_normal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates normality assumption "
                    f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                )
        
        # Check monotonicity
        for pair, details in mono_results.items():
            if not details['is_monotonic']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable pair {pair} may not have a monotonic relationship "
                    f"(Spearman correlation={details['spearman_correlation']:.2f})"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size "
                f"(n={size_results['sample_size']} < required 25)"
            )
        
        # Check outliers
        for var, details in outlier_results.items():
            if details['has_significant_outliers']:
                results['warnings'].append(
                    f"Variable '{var}' has {details['n_outliers']} significant outliers "
                    "which may affect the correlation"
                )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Spearman rank correlation',
                'Kendall rank correlation',
                'Robust correlation methods']

class PairedDataChecker:
    
    def check_paired_structure(self, data: pd.DataFrame, variables: List[str]) -> Dict:
        """Check if data is properly paired."""
        if len(variables) != 2:
            return {
                'is_paired': False,
                'error': 'Exactly two variables required for paired data'
            }
            
        # Check equal number of observations
        valid_pairs = data[variables].dropna().shape[0]
        total_rows = len(data)
        
        return {
            'is_paired': valid_pairs == total_rows,
            'valid_pairs': valid_pairs,
            'total_observations': total_rows,
            'missing_pairs': total_rows - valid_pairs
        }
      
class PairedTTestChecker(AssumptionChecker, NormalityChecker, PairedDataChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Paired t-test',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check paired structure
        pair_results = self.check_paired_structure(data, variables)
        results['details']['paired_structure'] = pair_results
        
        # Check normality of differences
        if pair_results['is_paired']:
            # Calculate differences
            diff = data[variables[0]] - data[variables[1]]
            norm_results = self.check_normality(
                pd.DataFrame({'difference': diff}), 
                ['difference'], 
                self.alpha
            )
            results['details']['normality'] = norm_results
        
        # Check sample size
        size_results = self._check_sample_size(data, variables)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, pair_results, 
                           results['details'].get('normality', {}), 
                           size_results)
        
        return results
    
    def _check_sample_size(self, data: pd.DataFrame, 
                          variables: List[str]) -> Dict:
        # Rule of thumb: at least 30 pairs
        valid_pairs = data[variables].dropna().shape[0]
        return {
            'n_pairs': valid_pairs,
            'requirement_met': valid_pairs >= 30
        }
    
    def _update_results(self, results: Dict, pair_results: Dict,
                       norm_results: Dict, size_results: Dict) -> None:
        # Check paired structure
        if not pair_results['is_paired']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Data is not properly paired "
                f"({pair_results['missing_pairs']} missing pairs)"
            )
        
        # Check normality of differences
        if 'difference' in norm_results:
            details = norm_results['difference']
            if not details['is_normal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    "Differences between pairs are not normally distributed "
                    f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient number of pairs "
                f"(n={size_results['n_pairs']} < required 30)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Wilcoxon signed-rank test',
                'Sign test',
                'Randomization test']

class CategoricalDataChecker:
    
    def check_categorical_data(self, data: pd.DataFrame, variables: List[str]) -> Dict:
        """Check if variables are categorical and have sufficient categories."""
        results = {}
        
        for var in variables:
            n_categories = data[var].nunique()
            value_counts = data[var].value_counts()
            
            results[var] = {
                'n_categories': n_categories,
                'min_category_count': value_counts.min(),
                'is_categorical': data[var].dtype in ['object', 'category', 'bool'] or n_categories <= 10,
                'category_counts': value_counts.to_dict()
            }
            
        return results

class ChiSquareIndependenceChecker(AssumptionChecker, CategoricalDataChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Chi-square test of independence',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check categorical nature of variables
        cat_results = self.check_categorical_data(data, variables)
        results['details']['categorical_data'] = cat_results
        
        # Check expected frequencies
        freq_results = self._check_expected_frequencies(data, variables)
        results['details']['expected_frequencies'] = freq_results
        
        # Check independence of observations
        indep_results = self._check_independence(data, variables)
        results['details']['independence'] = indep_results
        
        # Update results
        self._update_results(results, cat_results, freq_results, indep_results)
        
        return results
    
    def _check_expected_frequencies(self, data: pd.DataFrame, 
                                  variables: List[str]) -> Dict:
        """Check if expected frequencies meet minimum requirements."""
        if len(variables) != 2:
            return {'error': 'Exactly two variables required'}
            
        # Create contingency table
        contingency = pd.crosstab(data[variables[0]], data[variables[1]])
        
        # Calculate expected frequencies
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        
        return {
            'min_expected': expected.min(),
            'cells_less_than_5': (expected < 5).sum(),
            'total_cells': expected.size,
            'requirements_met': expected.min() >= 5 and (expected < 5).sum() <= expected.size * 0.2
        }
    
    def _check_independence(self, data: pd.DataFrame, 
                          variables: List[str]) -> Dict:
        """Check independence of observations (basic checks)."""
        return {
            'warning': 'Independence of observations must be ensured by study design',
            'considerations': [
                'Each subject contributes to only one cell',
                'Samples are random and representative',
                'No paired or repeated measurements'
            ]
        }
    
    def _update_results(self, results: Dict, cat_results: Dict,
                       freq_results: Dict, indep_results: Dict) -> None:
        # Check categorical nature
        for var, details in cat_results.items():
            if not details['is_categorical']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' may not be categorical "
                    f"({details['n_categories']} unique values)"
                )
        
        # Check expected frequencies
        if 'error' not in freq_results:
            if freq_results['min_expected'] < 5:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Some expected frequencies are less than 5 "
                    f"({freq_results['cells_less_than_5']} cells affected)"
                )
            
            if not freq_results['requirements_met']:
                results['warnings'].append(
                    "More than 20% of expected frequencies are less than 5"
                )
        
        # Add independence reminder
        results['warnings'].append(
            "Note: Independence of observations must be verified through study design"
        )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Fisher\'s exact test',
                'G-test of independence',
                'Freeman-Halton test',
                'Log-linear analysis']

class MultivariateRelationshipChecker:
    
    def check_multivariate_relationships(self, X: pd.DataFrame, y: pd.Series) -> Dict:
        """Check relationships between multiple predictors and outcome."""
        results = {}
        
        # Check linearity for each predictor
        for column in X.columns:
            # Calculate Pearson correlation
            corr, p_value = stats.pearsonr(X[column].dropna(), y.dropna())
            
            # Check for non-linear patterns using polynomial fit
            try:
                x = X[column].values.reshape(-1, 1)
                y_vals = y.values
                
                # Fit linear and quadratic models
                linear_model = np.polyfit(x.ravel(), y_vals, 1)
                quad_model = np.polyfit(x.ravel(), y_vals, 2)
                
                # Compare fits using R-squared
                linear_r2 = np.corrcoef(y_vals, np.polyval(linear_model, x.ravel()))[0,1]**2
                quad_r2 = np.corrcoef(y_vals, np.polyval(quad_model, x.ravel()))[0,1]**2
                
                # If quadratic fit is substantially better, might indicate non-linearity
                potential_nonlinearity = (quad_r2 - linear_r2) > 0.1
                
            except:
                potential_nonlinearity = False
                linear_r2 = quad_r2 = None
            
            results[column] = {
                'correlation': corr,
                'p_value': p_value,
                'linear_r2': linear_r2,
                'quadratic_r2': quad_r2,
                'potential_nonlinearity': potential_nonlinearity,
                'passes_linearity': abs(corr) > 0.1 and not potential_nonlinearity
            }
            
        return results
    
class MultipleRegressionChecker(AssumptionChecker, NormalityChecker, MultivariateRelationshipChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              dependent_var: str, **kwargs) -> Dict:
        results = {
            'test_type': 'Multiple Linear Regression',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Separate predictors and outcome
        X = data[variables].drop(dependent_var, axis=1, errors='ignore')
        y = data[dependent_var]
        
        # Check normality of residuals
        model = sm.OLS(y, sm.add_constant(X)).fit()
        residuals = model.resid
        norm_results = self.check_normality(
            pd.DataFrame({'residuals': residuals}),
            ['residuals'],
            self.alpha
        )
        results['details']['residuals_normality'] = norm_results
        
        # Check multivariate relationships
        relationship_results = self.check_multivariate_relationships(X, y)
        results['details']['predictor_relationships'] = relationship_results
        
        # Check homoscedasticity using Breusch-Pagan test
        homo_results = self._check_homoscedasticity(model)
        results['details']['homoscedasticity'] = homo_results
        
        # Check multicollinearity using VIF
        vif_results = self._check_multicollinearity(X)
        results['details']['multicollinearity'] = vif_results
        
        # Check independence using Durbin-Watson
        indep_results = self._check_independence(model)
        results['details']['independence'] = indep_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(X)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, norm_results, relationship_results,
                           homo_results, vif_results, indep_results, size_results)
        
        return results
    
    def _check_homoscedasticity(self, model) -> Dict:
        try:
            bp_test = sm.stats.diagnostic.het_breuschpagan(
                model.resid,
                model.model.exog
            )
            return {
                'bp_statistic': bp_test[0],
                'bp_p_value': bp_test[1],
                'is_homoscedastic': bp_test[1] > self.alpha
            }
        except:
            return {'error': 'Could not compute Breusch-Pagan test'}
    
    def _check_multicollinearity(self, X: pd.DataFrame) -> Dict:
        X_with_const = sm.add_constant(X)
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X_with_const.columns
        vif_data["VIF"] = [variance_inflation_factor(X_with_const.values, i)
                          for i in range(X_with_const.shape[1])]
        
        return {
            'vif_factors': vif_data.set_index('Variable')['VIF'].to_dict(),
            'has_multicollinearity': any(vif > 5 for vif in vif_data['VIF'])
        }
    
    def _check_independence(self, model) -> Dict:
        dw_stat = sm.stats.stattools.durbin_watson(model.resid)
        return {
            'durbin_watson': dw_stat,
            'is_independent': 1.5 < dw_stat < 2.5
        }
    
    def _check_sample_size(self, X: pd.DataFrame) -> Dict:
        n_predictors = X.shape[1]
        n_samples = X.shape[0]
        required_samples = n_predictors * 20
        
        return {
            'n_samples': n_samples,
            'n_predictors': n_predictors,
            'required_samples': required_samples,
            'requirement_met': n_samples >= required_samples
        }
    
    def _update_results(self, results: Dict, norm_results: Dict,
                       relationship_results: Dict, homo_results: Dict,
                       vif_results: Dict, indep_results: Dict,
                       size_results: Dict) -> None:
        # Check residuals normality
        if not norm_results['residuals']['is_normal']:
            results['assumptions_met'] = False
            results['warnings'].append(
                "Residuals are not normally distributed "
                f"(Shapiro-Wilk p={norm_results['residuals']['shapiro_p_value']:.4f})"
            )
        
        # Check predictor relationships
        for pred, details in relationship_results.items():
            if not details['passes_linearity']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Non-linear relationship detected for predictor '{pred}'"
                )
        
        # Check homoscedasticity
        if 'is_homoscedastic' in homo_results and not homo_results['is_homoscedastic']:
            results['assumptions_met'] = False
            results['warnings'].append(
                "Heteroscedasticity detected "
                f"(Breusch-Pagan p={homo_results['bp_p_value']:.4f})"
            )
        
        # Check multicollinearity
        if vif_results['has_multicollinearity']:
            results['assumptions_met'] = False
            high_vif = {k: v for k, v in vif_results['vif_factors'].items() if v > 5}
            results['warnings'].append(
                f"High multicollinearity detected for variables: {list(high_vif.keys())}"
            )
        
        # Check independence
        if not indep_results['is_independent']:
            results['assumptions_met'] = False
            results['warnings'].append(
                "Autocorrelation detected in residuals "
                f"(Durbin-Watson={indep_results['durbin_watson']:.2f})"
            )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size (n={size_results['n_samples']}, "
                f"required={size_results['required_samples']} for "
                f"{size_results['n_predictors']} predictors)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Ridge Regression',
                'Lasso Regression',
                'Robust Regression',
                'Quantile Regression',
                'Non-linear regression models']

class InteractionChecker:
    
    def check_interactions(self, data: pd.DataFrame, dependent_var: str,
                          factors: List[str]) -> Dict:
        results = {}
        
        # Check cell sizes for all factor combinations
        crosstab = pd.crosstab(*[data[f] for f in factors])
        cell_sizes = crosstab.values
        
        # Check balance
        is_balanced = len(set(cell_sizes.flatten())) == 1
        
        # Calculate mean for each combination
        means = data.groupby(factors)[dependent_var].mean().unstack()
        
        try:
            diffs = means.diff()
            max_diff_ratio = abs(diffs.max() / diffs.min())
            potential_interaction = max_diff_ratio > 1.5  # threshold for flagging
        except:
            potential_interaction = False
        
        results = {
            'cell_sizes': crosstab.to_dict(),
            'is_balanced': is_balanced,
            'min_cell_size': cell_sizes.min(),
            'max_cell_size': cell_sizes.max(),
            'potential_interaction': potential_interaction
        }
        
        return results
    
class TwoWayANOVAChecker(AssumptionChecker, NormalityChecker, HomoscedasticityChecker):
    """Checker for two-way ANOVA assumptions."""
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Two-way ANOVA',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Get factors from kwargs
        factors = kwargs.get('factors', [])
        if len(factors) != 2:
            results['assumptions_met'] = False
            results['warnings'].append("Two-way ANOVA requires exactly two factors")
            return results
        
        # First variable in variables list is the dependent variable
        dependent_var = variables[0]
            
        # Check normality within each group combination
        norm_results = {}
        for f1_val in data[factors[0]].unique():
            for f2_val in data[factors[1]].unique():
                group_data = data[
                    (data[factors[0]] == f1_val) & 
                    (data[factors[1]] == f2_val)
                ]
                if len(group_data) > 0:
                    group_name = f"{factors[0]}={f1_val}, {factors[1]}={f2_val}"
                    norm_results[group_name] = self.check_normality(
                        group_data, [dependent_var], self.alpha
                    )
        
        results['details']['normality'] = norm_results
        
        # Check homogeneity of variance
        data['_combined_groups'] = data[factors].apply(
            lambda x: '_'.join(x.astype(str)), axis=1
        )
        homo_results = self.check_homoscedasticity(
            data, [dependent_var], '_combined_groups', self.alpha
        )
        results['details']['homoscedasticity'] = homo_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(data, factors)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, norm_results, homo_results, size_results)
        
        return results
    
    def _check_sample_size(self, data: pd.DataFrame, factors: List[str]) -> Dict:
        cell_sizes = data.groupby(factors).size()
        
        return {
            'group_sizes': cell_sizes.to_dict(),
            'min_group_size': cell_sizes.min(),
            'requirement_met': cell_sizes.min() >= 30
        }
    
    def _update_results(self, results: Dict, norm_results: Dict,
                       homo_results: Dict, size_results: Dict) -> None:
        # Check normality in each group
        for group, norm_details in norm_results.items():
            for var, details in norm_details.items():
                if not details['is_normal']:
                    results['assumptions_met'] = False
                    results['warnings'].append(
                        f"Variable in group {group} violates normality "
                        f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                    )
        
        # Check homoscedasticity
        for var, details in homo_results.items():
            if not details['is_homoscedastic']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable violates homoscedasticity assumption "
                    f"(Levene's test p={details['levene_p_value']:.4f})"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size in some groups "
                f"(minimum {size_results['min_group_size']} < required 30)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return [
            'Non-parametric factorial analysis',
            'Robust two-way ANOVA',
            'Aligned Rank Transform ANOVA',
            'Separate non-parametric tests with correction',
            'Mixed-effects model'
        ]
                        
class SurvivalDataChecker:
    
    def check_survival_data(self, data: pd.DataFrame, time_col: str,
                           event_col: str, group_col: Optional[str] = None) -> Dict:

        results = {}
        
        # Check time variable
        time_data = data[time_col]
        results['time'] = {
            'has_negative': (time_data < 0).any(),
            'missing_values': time_data.isnull().sum(),
            'is_numeric': np.issubdtype(time_data.dtype, np.number),
            'passes_requirements': (
                np.issubdtype(time_data.dtype, np.number) and
                not (time_data < 0).any() and
                time_data.isnull().sum() == 0
            )
        }
        
        event_data = data[event_col]
        unique_events = event_data.unique()
        results['event'] = {
            'unique_values': list(unique_events),
            'is_binary': len(unique_events) <= 2 and all(isinstance(x, (int, bool, np.integer)) 
                                                       for x in unique_events if pd.notna(x)),
            'missing_values': event_data.isnull().sum(),
            'passes_requirements': (
                len(unique_events) <= 2 and
                event_data.isnull().sum() == 0 and
                all(isinstance(x, (int, bool, np.integer)) for x in unique_events if pd.notna(x))
            )
        }
        
        if group_col:
            group_data = data[group_col]
            results['groups'] = {
                'n_groups': group_data.nunique(),
                'min_group_size': group_data.value_counts().min(),
                'group_sizes': group_data.value_counts().to_dict(),
                'missing_values': group_data.isnull().sum(),
                'passes_requirements': group_data.isnull().sum() == 0
            }
        
        return results
    
class KaplanMeierChecker(AssumptionChecker, SurvivalDataChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Kaplan-Meier survival analysis',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # First variable is time, second is event
        if len(variables) < 2:
            raise ValueError("KaplanMeierChecker requires time and event variables")
            
        time_col = variables[0]
        event_col = variables[1]
        group_col = kwargs.get('group_col', None)
        
        # Check basic survival data requirements
        survival_results = self.check_survival_data(data, time_col, event_col, group_col)
        results['details']['survival_data'] = survival_results
        
        # Check censoring patterns
        censor_results = self._check_censoring(data, time_col, event_col, group_col)
        results['details']['censoring'] = censor_results
        
        # Check independence of observations
        indep_results = self._check_independence()
        results['details']['independence'] = indep_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(data, event_col, group_col)  # Added event_col parameter
        results['details']['sample_size'] = size_results
        
        # Check for time-varying covariates (warning only)
        results['details']['time_varying'] = {
            'warning': 'Standard Kaplan-Meier cannot handle time-varying covariates'
        }
        
        # Update results
        self._update_results(results, survival_results, censor_results, 
                           indep_results, size_results)
        
        return results
    
    def _check_censoring(self, data: pd.DataFrame, time_col: str,
                        event_col: str, group_col: Optional[str]) -> Dict:
        """Check censoring patterns in the data."""
        results = {
            'overall_censoring_rate': (1 - data[event_col].mean()) * 100
        }
        
        if group_col:
            # Check censoring by group
            censoring_by_group = data.groupby(group_col)[event_col].agg(
                ['count', 'mean']
            )
            censoring_by_group['censoring_rate'] = (1 - censoring_by_group['mean']) * 100
            
            results.update({
                'censoring_by_group': censoring_by_group['censoring_rate'].to_dict(),
                'max_censoring_diff': censoring_by_group['censoring_rate'].max() - 
                                    censoring_by_group['censoring_rate'].min(),
                'has_informative_censoring': False  # This requires domain knowledge
            })
        
        return results
    
    def _check_independence(self) -> Dict:
        return {
            'warning': 'Independence must be ensured by study design',
            'considerations': [
                'No multiple observations from same subject',
                'No clustering/correlation between subjects',
                'Random sampling from population',
                'No competing risks that violate independence'
            ]
        }
    
    def _check_sample_size(self, data: pd.DataFrame, event_col: str,
                          group_col: Optional[str]) -> Dict:
        total_size = len(data)
        n_events = data[event_col].sum()
        
        results = {
            'total_sample_size': total_size,
            'total_events': n_events,
            'requirement_met': total_size >= 30 and n_events >= 15
        }
        
        if group_col:
            group_sizes = data.groupby(group_col).size()
            group_events = data.groupby(group_col)[event_col].sum()
            
            results.update({
                'min_group_size': group_sizes.min(),
                'min_group_events': group_events.min(),
                'group_requirement_met': (group_sizes.min() >= 20 and 
                                        group_events.min() >= 10)
            })
        
        return results
    
    def _update_results(self, results: Dict, survival_results: Dict,
                       censor_results: Dict, indep_results: Dict,
                       size_results: Dict) -> None:
        # Check time variable
        if not survival_results['time']['passes_requirements']:
            results['assumptions_met'] = False
            if survival_results['time']['has_negative']:
                results['warnings'].append("Negative survival times detected")
            if not survival_results['time']['is_numeric']:
                results['warnings'].append("Time variable must be numeric")
            if survival_results['time']['missing_values'] > 0:
                results['warnings'].append(
                    f"Missing values in time variable "
                    f"(n={survival_results['time']['missing_values']})"
                )
        
        # Check event indicator
        if not survival_results['event']['passes_requirements']:
            results['assumptions_met'] = False
            if not survival_results['event']['is_binary']:
                results['warnings'].append(
                    "Event indicator must be binary "
                    f"(found values: {survival_results['event']['unique_values']})"
                )
            if survival_results['event']['missing_values'] > 0:
                results['warnings'].append(
                    f"Missing values in event indicator "
                    f"(n={survival_results['event']['missing_values']})"
                )
        
        # Check censoring
        if censor_results['overall_censoring_rate'] > 70:
            results['warnings'].append(
                f"High censoring rate "
                f"({censor_results['overall_censoring_rate']:.1f}%)"
            )
        
        if 'max_censoring_diff' in censor_results:
            if censor_results['max_censoring_diff'] > 20:
                results['warnings'].append(
                    "Large difference in censoring rates between groups "
                    f"({censor_results['max_censoring_diff']:.1f}%)"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size or events "
                f"(n={size_results['total_sample_size']}, "
                f"events={size_results['total_events']})"
            )
        
        if 'group_requirement_met' in size_results:
            if not size_results['group_requirement_met']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Insufficient sample size in some groups "
                    f"(minimum n={size_results['min_group_size']}, "
                    f"minimum events={size_results['min_group_events']})"
                )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Cox Proportional Hazards model',
                'Parametric survival models',
                'Competing risks analysis',
                'Time-varying coefficient models']
        
class ProportionalHazardsChecker:
    
    def check_proportional_hazards(self, data: pd.DataFrame, time_col: str,
                                 event_col: str, predictors: List[str],
                                 alpha: float) -> Dict:
        results = {}
        
        try:
            # Fit Cox model
            cph = lifelines.CoxPHFitter()
            df = data[[time_col, event_col] + predictors].copy()
            cph.fit(df, duration_col=time_col, event_col=event_col)
            
            # Test proportional hazards using scaled Schoenfeld residuals
            ph_test = cph.check_assumptions(df, show_plots=False)
            
            for predictor in predictors:
                results[predictor] = {
                    'p_value': ph_test.loc[predictor, 'p'],
                    'passes_ph': ph_test.loc[predictor, 'p'] > alpha,
                    'correlation': ph_test.loc[predictor, 'correlation']
                }
                
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
class CoxPHChecker(AssumptionChecker, SurvivalDataChecker, ProportionalHazardsChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Cox Proportional Hazards Regression',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # First two variables are time and event, rest are predictors
        if len(variables) < 2:
            raise ValueError("CoxPHChecker requires time, event, and predictor variables")
            
        time_col = variables[0]
        event_col = variables[1]
        predictors = variables[2:] if len(variables) > 2 else []
        
        # Check basic survival data requirements
        survival_results = self.check_survival_data(data, time_col, event_col)
        results['details']['survival_data'] = survival_results
        
        # Check proportional hazards assumption
        ph_results = self.check_proportional_hazards(
            data, time_col, event_col, predictors, self.alpha
        )
        results['details']['proportional_hazards'] = ph_results
        
        # Check for multicollinearity among predictors
        if predictors:
            collin_results = self._check_multicollinearity(data[predictors])
            results['details']['multicollinearity'] = collin_results
        
        # Check for non-linear relationships
        linearity_results = self._check_linearity(
            data, time_col, event_col, predictors
        )
        results['details']['linearity'] = linearity_results
        
        # Check sample size and events per variable
        size_results = self._check_sample_size(data, event_col, len(predictors))
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, survival_results, ph_results,
                           collin_results if predictors else {},
                           linearity_results, size_results)
        
        return results

    def _check_multicollinearity(self, X: pd.DataFrame) -> Dict:
        """Check multicollinearity using VIF."""
        X = sm.add_constant(X)
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(X.shape[1])]
        
        return {
            'vif_factors': vif_data.set_index('Variable')['VIF'].to_dict(),
            'has_multicollinearity': any(vif > 5 for vif in vif_data['VIF'])
        }
    
    def _check_linearity(self, data: pd.DataFrame, time_col: str,
                        event_col: str, predictors: List[str]) -> Dict:
        results = {}
        
        if not predictors: 
            return results
            
        try:
            # Fit Cox model
            cph = lifelines.CoxPHFitter()
            df = data[[time_col, event_col] + predictors].copy()
            cph.fit(df, duration_col=time_col, event_col=event_col)
            
            # Get martingale residuals
            mart_residuals = cph.compute_residuals(df, 'martingale')
            
            # Check correlation with predictors
            for pred in predictors:
                if np.issubdtype(data[pred].dtype, np.number):
                    corr, p_value = stats.spearmanr(data[pred], mart_residuals)
                    results[pred] = {
                        'correlation': corr,
                        'p_value': p_value,
                        'is_linear': p_value > self.alpha
                    }
        except:
            results['error'] = "Could not compute martingale residuals"
        
        return results

    def _check_sample_size(self, data: pd.DataFrame, event_col: str,
                          n_predictors: int) -> Dict:
        """Check sample size and events per variable."""
        n_samples = len(data)
        n_events = data[event_col].sum()
        
        # Rule of thumb: at least 10 events per predictor
        required_events = max(n_predictors * 10, 1)  # Avoid division by zero
        
        return {
            'n_samples': n_samples,
            'n_events': n_events,
            'n_predictors': n_predictors,
            'events_per_predictor': n_events / required_events if required_events > 0 else float('inf'),
            'required_events': required_events,
            'requirement_met': n_events >= required_events
        }
    
    def _update_results(self, results: Dict, survival_results: Dict,
                       ph_results: Dict, collin_results: Dict,
                       linearity_results: Dict, size_results: Dict) -> None:
        pass
    
    def get_alternative_tests(self) -> List[str]:
        return ['Stratified Cox model',
                'Time-varying coefficient Cox model',
                'Parametric survival models',
                'Additive hazards models']

class PoissonRegressionChecker(AssumptionChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Poisson Regression',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        if len(variables) < 2:
            raise ValueError("PoissonRegressionChecker requires dependent variable and at least one predictor")
        
        # First variable is dependent variable, rest are predictors
        dependent_var = variables[0]
        predictors = variables[1:]
        offset_var = kwargs.get('offset_var', None)
        
        # Check response variable
        response_results = self._check_response_variable(data[dependent_var])
        results['details']['response'] = response_results
        
        # Check mean-variance relationship
        variance_results = self._check_equidispersion(
            data, dependent_var, predictors, offset_var
        )
        results['details']['equidispersion'] = variance_results
        
        # Check for excess zeros
        zero_results = self._check_excess_zeros(data[dependent_var])
        results['details']['zero_inflation'] = zero_results
        
        # Check multicollinearity
        collin_results = self._check_multicollinearity(data[predictors])
        results['details']['multicollinearity'] = collin_results
        
        # Check sample size
        size_results = self._check_sample_size(data, len(predictors))
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, response_results, variance_results,
                           zero_results, collin_results, size_results)
        
        return results
    
    def _check_response_variable(self, y: pd.Series) -> Dict:
        return {
            'is_integer': all(float(x).is_integer() for x in y.dropna()),
            'is_non_negative': all(x >= 0 for x in y.dropna()),
            'missing_values': y.isnull().sum(),
            'passes_requirements': (
                all(float(x).is_integer() for x in y.dropna()) and
                all(x >= 0 for x in y.dropna()) and
                y.isnull().sum() == 0
            )
        }
    
    def _check_equidispersion(self, data: pd.DataFrame, dependent_var: str,
                             predictors: List[str],
                             offset_var: Optional[str]) -> Dict:
        try:
            # Fit Poisson model
            X = sm.add_constant(data[predictors])
            y = data[dependent_var]
            
            if offset_var:
                model = sm.GLM(y, X, family=sm.families.Poisson(), 
                             offset=np.log(data[offset_var]))
            else:
                model = sm.GLM(y, X, family=sm.families.Poisson())
                
            results = model.fit()
            
            # Calculate pearson chi-square statistic
            pearson_chi2 = results.pearson_chi2 / results.df_resid
            
            return {
                'dispersion_ratio': pearson_chi2,
                'is_equidispersed': 0.5 <= pearson_chi2 <= 1.5
            }
            
        except:
            return {'error': 'Could not compute dispersion statistics'}
    
    def _check_excess_zeros(self, y: pd.Series) -> Dict:
        n_zeros = (y == 0).sum()
        prop_zeros = n_zeros / len(y)
        
        return {
            'zero_count': n_zeros,
            'zero_proportion': prop_zeros,
            'has_excess_zeros': prop_zeros > 0.5
        }
    
    def _check_multicollinearity(self, X: pd.DataFrame) -> Dict:
        X = sm.add_constant(X)
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(X.shape[1])]
        
        return {
            'vif_factors': vif_data.set_index('Variable')['VIF'].to_dict(),
            'has_multicollinearity': any(vif > 5 for vif in vif_data['VIF'])
        }
    
    def _check_sample_size(self, data: pd.DataFrame, 
                          n_predictors: int) -> Dict:
        n = len(data)
        # Rule of thumb: at least 10-20 observations per predictor
        required_n = n_predictors * 20
        
        return {
            'n_samples': n,
            'n_predictors': n_predictors,
            'required_samples': required_n,
            'requirement_met': n >= required_n
        }
    
    def _update_results(self, results: Dict, response_results: Dict,
                       variance_results: Dict, zero_results: Dict,
                       collin_results: Dict, size_results: Dict) -> None:
        # Check response variable
        if not response_results['passes_requirements']:
            results['assumptions_met'] = False
            if not response_results['is_integer']:
                results['warnings'].append("Response variable must be count data")
            if not response_results['is_non_negative']:
                results['warnings'].append("Response variable must be non-negative")
            if response_results['missing_values'] > 0:
                results['warnings'].append(
                    f"Response variable has {response_results['missing_values']} "
                    "missing values"
                )
        
        # Check equidispersion
        if 'error' not in variance_results:
            if not variance_results['is_equidispersed']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Over/underdispersion detected "
                    f"(dispersion ratio={variance_results['dispersion_ratio']:.2f})"
                )
        
        # Check zero inflation
        if zero_results['has_excess_zeros']:
            results['warnings'].append(
                f"Excess zeros detected "
                f"({zero_results['zero_proportion']*100:.1f}% zeros)"
            )
        
        # Check multicollinearity
        if collin_results['has_multicollinearity']:
            results['assumptions_met'] = False
            high_vif = {k: v for k, v in collin_results['vif_factors'].items() 
                       if v > 5}
            results['warnings'].append(
                f"High multicollinearity detected for variables: {list(high_vif.keys())}"
            )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size "
                f"(n={size_results['n_samples']} < "
                f"required {size_results['required_samples']})"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Negative Binomial Regression',
                'Zero-inflated Poisson Regression',
                'Zero-inflated Negative Binomial Regression',
                'Quasi-Poisson Regression']

class SpearmanCorrelationChecker(AssumptionChecker, MonotonicityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': "Spearman's Rank Correlation",
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check for monotonic relationship
        mono_results = self.check_monotonicity(data, variables)
        results['details']['monotonicity'] = mono_results
        
        # Check for independence of observations
        indep_results = self._check_independence()
        results['details']['independence'] = indep_results
        
        # Check for paired observations
        paired_results = self._check_paired_observations(data, variables)
        results['details']['paired_observations'] = paired_results
        
        # Check sample size
        size_results = self._check_sample_size(data, variables)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, mono_results, indep_results, 
                           paired_results, size_results)
        
        return results
    
    def _check_independence(self) -> Dict:
        return {
            'warning': 'Independence must be ensured by study design',
            'considerations': [
                'No repeated measures from same subjects',
                'Random sampling from population',
                'No natural ordering/time series structure',
                'No clustered/grouped observations'
            ]
        }
    
    def _check_paired_observations(self, data: pd.DataFrame, 
                                 variables: List[str]) -> Dict:
        """Check if observations are properly paired."""
        missing_patterns = data[variables].isnull()
        complete_pairs = (~missing_patterns).all(axis=1).sum()
        total_rows = len(data)
        
        return {
            'complete_pairs': complete_pairs,
            'missing_pairs': total_rows - complete_pairs,
            'is_properly_paired': complete_pairs == total_rows
        }
    
    def _check_sample_size(self, data: pd.DataFrame, 
                          variables: List[str]) -> Dict:
        """Check sample size requirements."""
        n = len(data)
        complete_cases = data[variables].dropna().shape[0]
        
        # For small samples (n < 25), better to use Kendall's tau
        # For very small samples (n < 10), correlation analysis might be unreliable
        return {
            'total_observations': n,
            'complete_cases': complete_cases,
            'small_sample_warning': complete_cases < 25,
            'very_small_sample': complete_cases < 10,
            'requirement_met': complete_cases >= 25
        }
    
    def _update_results(self, results: Dict, mono_results: Dict,
                       indep_results: Dict, paired_results: Dict,
                       size_results: Dict) -> None:
        # Check monotonicity and ties
        for pair, details in mono_results.items():
            if details['correlation_strength'] < 0.1:
                results['warnings'].append(
                    f"Very weak monotonic relationship detected for {pair} "
                    f"(strength={details['correlation_strength']:.3f})"
                )
            
            # Warning for excessive ties
            if details['ties_first_var']['tied_values_pct'] > 30 or \
               details['ties_second_var']['tied_values_pct'] > 30:
                results['warnings'].append(
                    f"High proportion of ties detected in {pair}, "
                    "consider using Kendall's tau-b"
                )
        
        # Check paired observations
        if not paired_results['is_properly_paired']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Missing pairs detected "
                f"({paired_results['missing_pairs']} missing pairs)"
            )
        
        # Check sample size
        if size_results['very_small_sample']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Sample size too small (n={size_results['complete_cases']} < 10)"
            )
        elif size_results['small_sample_warning']:
            results['warnings'].append(
                f"Small sample size (n={size_results['complete_cases']} < 25), "
                "consider using Kendall's tau"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ["Kendall's tau",
                "Kendall's tau-b (for ties)",
                "Pearson correlation (if relationship is linear)",
                "Distance correlation (for non-monotonic relationships)"]

class PairedDifferenceChecker:
    
    def check_paired_differences(self, data: pd.DataFrame, 
                               variables: List[str]) -> Dict:
        """Check properties of paired differences."""
        if len(variables) != 2:
            return {'error': 'Exactly two variables required for paired data'}
        
        # Calculate differences
        diff = data[variables[0]] - data[variables[1]]
        diff = diff.dropna()
        
        # Check for zeros
        zero_diffs = (diff == 0).sum()
        non_zero_diffs = len(diff) - zero_diffs
        
        # Check symmetry around zero
        if len(diff) > 0:
            pos_diffs = (diff > 0).sum()
            neg_diffs = (diff < 0).sum()
            
            # Simple symmetry check using proportion of positive vs negative differences
            prop_ratio = pos_diffs / neg_diffs if neg_diffs > 0 else float('inf')
            roughly_symmetric = 0.5 <= prop_ratio <= 2
            
            # More formal test of symmetry around zero
            try:
                _, symm_p_value = stats.wilcoxon(
                    diff, 
                    alternative='two-sided',
                    zero_method='wilcox'
                )
            except:
                symm_p_value = None
        else:
            pos_diffs = neg_diffs = 0
            roughly_symmetric = False
            symm_p_value = None
        
        return {
            'n_differences': len(diff),
            'n_zero_differences': zero_diffs,
            'n_non_zero_differences': non_zero_diffs,
            'n_positive_differences': pos_diffs,
            'n_negative_differences': neg_diffs,
            'roughly_symmetric': roughly_symmetric,
            'symmetry_p_value': symm_p_value,
            'median_difference': diff.median() if len(diff) > 0 else None,
            'passes_requirements': (
                len(diff) > 0 and
                non_zero_diffs >= 10  # Minimum recommended sample size
            )
        }

class WilcoxonSignedRankChecker(AssumptionChecker, PairedDifferenceChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Wilcoxon Signed-Rank Test',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check paired structure and differences
        diff_results = self.check_paired_differences(data, variables)
        results['details']['differences'] = diff_results
        
        # Check for independence of pairs
        indep_results = self._check_independence()
        results['details']['independence'] = indep_results
        
        # Check continuous scale of measurement
        scale_results = self._check_measurement_scale(data, variables)
        results['details']['measurement_scale'] = scale_results
        
        # Check sample size and ties
        size_results = self._check_sample_size(diff_results)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, diff_results, scale_results, size_results)
        
        return results
    
    def _check_independence(self) -> Dict:
        return {
            'warning': 'Independence must be ensured by study design',
            'considerations': [
                'Pairs are independent of each other',
                'No relationship between different pairs',
                'Random sampling from target population',
                'No multiple measurements from same subject (except the pair)'
            ]
        }
    
    def _check_measurement_scale(self, data: pd.DataFrame, 
                               variables: List[str]) -> Dict:
        """Check if variables are measured on at least ordinal scale."""
        results = {}
        
        for var in variables:
            unique_values = data[var].nunique()
            is_numeric = np.issubdtype(data[var].dtype, np.number)
            
            results[var] = {
                'n_unique_values': unique_values,
                'is_numeric': is_numeric,
                'appears_continuous': unique_values >= 10 and is_numeric,
                'appears_ordinal': unique_values >= 3
            }
            
        return results
    
    def _check_sample_size(self, diff_results: Dict) -> Dict:
        n_non_zero = diff_results['n_non_zero_differences']
        
        return {
            'total_pairs': diff_results['n_differences'],
            'non_zero_pairs': n_non_zero,
            'minimum_required': 10,  # Common minimum recommendation
            'requirement_met': n_non_zero >= 10,
            'exact_test_possible': n_non_zero <= 50  # Size limit for exact test
        }
    
    def _update_results(self, results: Dict, diff_results: Dict,
                       scale_results: Dict, size_results: Dict) -> None:
        if 'error' in diff_results:
            results['assumptions_met'] = False
            results['warnings'].append(diff_results['error'])
            return
            
        # Check differences
        if not diff_results['passes_requirements']:
            results['assumptions_met'] = False
            if diff_results['n_non_zero_differences'] < 10:
                results['warnings'].append(
                    f"Insufficient non-zero differences "
                    f"(n={diff_results['n_non_zero_differences']} < required 10)"
                )
        
        if diff_results['n_zero_differences'] > 0:
            results['warnings'].append(
                f"Found {diff_results['n_zero_differences']} zero differences "
                "which will be excluded from analysis"
            )
        
        if not diff_results['roughly_symmetric']:
            results['warnings'].append(
                "Differences may not be symmetrically distributed around zero"
            )
        
        # Check measurement scale
        for var, details in scale_results.items():
            if not details['appears_ordinal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' may not be measured on at least "
                    "an ordinal scale"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Sample size too small "
                f"({size_results['non_zero_pairs']} non-zero pairs < "
                f"required {size_results['minimum_required']})"
            )
        elif size_results['exact_test_possible']:
            results['warnings'].append(
                "Sample size allows for exact test computation"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Sign test (for asymmetric differences)',
                'Paired t-test (if differences are normal)',
                'Permutation test',
                'Bootstrap methods']

class MultivariateNormalityChecker:
    
    def check_multivariate_normality(self, data: pd.DataFrame, 
                                   dependent_vars: List[str],
                                   group_col: str = None,
                                   alpha: float = 0.05) -> Dict:
        """
        Check multivariate normality using Mardia's test and univariate tests
        """
        results = {}
        
        if group_col:
            # Check within each group
            for group in data[group_col].unique():
                group_data = data[data[group_col] == group][dependent_vars]
                results[f"group_{group}"] = self._check_mv_normality(
                    group_data, alpha
                )
        else:
            # Check overall
            results["overall"] = self._check_mv_normality(
                data[dependent_vars], alpha
            )
            
        return results
    
    def _check_mv_normality(self, data: pd.DataFrame, alpha: float) -> Dict:
        # Calculate Mardia's coefficients
        try:
            mardia_stats = self._calculate_mardia(data)
            
            # Univariate normality for each variable
            univariate_tests = {}
            for col in data.columns:
                _, p_value = stats.normaltest(data[col].dropna())
                univariate_tests[col] = {
                    'p_value': p_value,
                    'is_normal': p_value > alpha
                }
            
            return {
                'mardia_skewness': mardia_stats['skewness'],
                'mardia_kurtosis': mardia_stats['kurtosis'],
                'mardia_stats_normal': (
                    mardia_stats['skewness'] < 3 and 
                    abs(mardia_stats['kurtosis']) < 3
                ),
                'univariate_tests': univariate_tests,
                'all_univariate_normal': all(
                    test['is_normal'] for test in univariate_tests.values()
                )
            }
            
        except:
            return {'error': 'Could not compute multivariate normality tests'}
    
    def _calculate_mardia(self, data: pd.DataFrame) -> Dict:
        X = data.values
        n = X.shape[0]
        p = X.shape[1]
        
        # Center the data
        X_centered = X - X.mean(axis=0)
        
        # Compute covariance matrix
        S = np.cov(X_centered, rowvar=False)
        
        try:
            # Compute Mahalanobis distances
            S_inv = np.linalg.inv(S)
            d = np.zeros(n)
            for i in range(n):
                d[i] = X_centered[i].dot(S_inv).dot(X_centered[i])
            
            # Compute skewness
            b1p = np.mean(d**3)
            
            # Compute kurtosis
            b2p = np.mean(d**2)
            
            return {
                'skewness': b1p / (6 * p),
                'kurtosis': (b2p / (p * (p + 2))) - 1
            }
        except:
            return {
                'skewness': float('inf'),
                'kurtosis': float('inf')
            }

class MANOVAChecker(AssumptionChecker, MultivariateNormalityChecker):
    
    def check(self, data: pd.DataFrame, dependent_vars: List[str],
              group_col: str, **kwargs) -> Dict:
        results = {
            'test_type': 'MANOVA',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check multivariate normality
        mv_norm_results = self.check_multivariate_normality(
            data, dependent_vars, group_col, self.alpha
        )
        results['details']['multivariate_normality'] = mv_norm_results
        
        # Check homogeneity of covariance matrices (Box's M test)
        covar_results = self._check_covariance_homogeneity(
            data, dependent_vars, group_col
        )
        results['details']['covariance_homogeneity'] = covar_results
        
        # Check for multicollinearity
        collin_results = self._check_multicollinearity(data[dependent_vars])
        results['details']['multicollinearity'] = collin_results
        
        # Check linearity between pairs of DVs
        linear_results = self._check_linearity(data, dependent_vars, group_col)
        results['details']['linearity'] = linear_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(
            data, dependent_vars, group_col
        )
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, mv_norm_results, covar_results,
                           collin_results, linear_results, size_results)
        
        return results
    
    def _check_covariance_homogeneity(self, data: pd.DataFrame,
                                     dependent_vars: List[str],
                                     group_col: str) -> Dict:
        """Check homogeneity of covariance matrices using Box's M test."""
        try:
            # Calculate covariance matrices for each group
            cov_matrices = {}
            for group in data[group_col].unique():
                group_data = data[data[group_col] == group][dependent_vars]
                cov_matrices[group] = np.cov(group_data.values.T)
            
            # Compare covariance matrices
            n_groups = len(cov_matrices)
            pooled_cov = sum(cov_matrices.values()) / n_groups
            
            # Calculate Box's M statistic
            n = len(data)
            p = len(dependent_vars)
            ln_dets = [np.log(np.linalg.det(cov)) for cov in cov_matrices.values()]
            ln_det_pooled = np.log(np.linalg.det(pooled_cov))
            
            box_m = (n - n_groups) * ln_det_pooled - sum(
                (len(data[data[group_col] == group]) - 1) * ln_det
                for group, ln_det in zip(cov_matrices.keys(), ln_dets)
            )
            
            # Approximate chi-square distribution
            chi2_stat = box_m
            df = (p * (p + 1) * (n_groups - 1)) / 2
            p_value = 1 - stats.chi2.cdf(chi2_stat, df)
            
            return {
                'box_m_statistic': box_m,
                'p_value': p_value,
                'is_homogeneous': p_value > self.alpha,
                'covariance_ratios': self._calculate_covariance_ratios(cov_matrices)
            }
        except:
            return {'error': 'Could not compute Box\'s M test'}
    
    def _calculate_covariance_ratios(self, cov_matrices: Dict) -> Dict:
        ratios = {}
        matrix_keys = list(cov_matrices.keys())
        
        for i in range(cov_matrices[matrix_keys[0]].shape[0]):
            for j in range(cov_matrices[matrix_keys[0]].shape[1]):
                covs = [m[i,j] for m in cov_matrices.values()]
                max_cov = max(abs(x) for x in covs)
                min_cov = min(abs(x) for x in covs)
                ratios[f'var_{i}_{j}'] = max_cov / min_cov if min_cov != 0 else float('inf')
                
        return ratios
    
    def _check_multicollinearity(self, X: pd.DataFrame) -> Dict:
        corr_matrix = X.corr()
        eigenvals = np.linalg.eigvals(corr_matrix)
        condition_number = max(eigenvals) / min(eigenvals)
        
        # Check for high correlations
        high_corrs = []
        for i in range(len(X.columns)):
            for j in range(i+1, len(X.columns)):
                if abs(corr_matrix.iloc[i,j]) > 0.9:
                    high_corrs.append({
                        'variables': (X.columns[i], X.columns[j]),
                        'correlation': corr_matrix.iloc[i,j]
                    })
        
        return {
            'condition_number': condition_number,
            'has_multicollinearity': condition_number > 30 or len(high_corrs) > 0,
            'high_correlations': high_corrs
        }
    
    def _check_linearity(self, data: pd.DataFrame, dependent_vars: List[str],
                        group_col: str) -> Dict:
        results = {}
        
        for group in data[group_col].unique():
            group_data = data[data[group_col] == group]
            group_results = {}
            
            for i, var1 in enumerate(dependent_vars):
                for var2 in dependent_vars[i+1:]:
                    # Fit polynomial regression
                    x = group_data[var1].values.reshape(-1, 1)
                    y = group_data[var2].values
                    
                    try:
                        # Compare linear and quadratic fits
                        linear_fit = np.polyfit(x.ravel(), y, 1)
                        quad_fit = np.polyfit(x.ravel(), y, 2)
                        
                        # Calculate R-squared for both models
                        linear_r2 = 1 - np.sum((y - np.polyval(linear_fit, x.ravel()))**2) / \
                                   np.sum((y - np.mean(y))**2)
                        quad_r2 = 1 - np.sum((y - np.polyval(quad_fit, x.ravel()))**2) / \
                                 np.sum((y - np.mean(y))**2)
                        
                        group_results[f"{var1}_vs_{var2}"] = {
                            'linear_r2': linear_r2,
                            'quadratic_r2': quad_r2,
                            'r2_difference': quad_r2 - linear_r2,
                            'is_linear': (quad_r2 - linear_r2) < 0.1
                        }
                    except:
                        group_results[f"{var1}_vs_{var2}"] = {
                            'error': 'Could not assess linearity'
                        }
            
            results[f"group_{group}"] = group_results
            
        return results
    
    def _check_sample_size(self, data: pd.DataFrame, dependent_vars: List[str],
                          group_col: str) -> Dict:
        """Check sample size requirements."""
        n_groups = data[group_col].nunique()
        n_dvs = len(dependent_vars)
        group_sizes = data.groupby(group_col).size()
        
        return {
            'n_groups': n_groups,
            'n_dependent_vars': n_dvs,
            'group_sizes': group_sizes.to_dict(),
            'min_group_size': group_sizes.min(),
            'meets_min_size': group_sizes.min() >= max(20, n_dvs + 1),
            'more_dvs_than_groups': n_dvs > n_groups
        }
    
    def _update_results(self, results: Dict, mv_norm_results: Dict,
                       covar_results: Dict, collin_results: Dict,
                       linear_results: Dict, size_results: Dict) -> None:
        # Check multivariate normality
        for group, details in mv_norm_results.items():
            if 'error' not in details:
                if not details['mardia_stats_normal']:
                    results['assumptions_met'] = False
                    results['warnings'].append(
                        f"Multivariate normality violated in {group}"
                    )
        
        # Check covariance homogeneity
        if 'error' not in covar_results:
            if not covar_results['is_homogeneous']:
                results['warnings'].append(
                    "Homogeneity of covariance matrices violated "
                    f"(Box's M p={covar_results['p_value']:.4f})"
                )
                
                # Check if violation is severe
                max_ratio = max(covar_results['covariance_ratios'].values())
                if max_ratio > 10:
                    results['assumptions_met'] = False
                    results['warnings'].append(
                        "Severe violation of covariance homogeneity "
                        f"(max ratio={max_ratio:.1f})"
                    )
        
        # Check multicollinearity
        if collin_results['has_multicollinearity']:
            results['assumptions_met'] = False
            if collin_results['condition_number'] > 30:
                results['warnings'].append(
                    "High multicollinearity detected "
                    f"(condition number={collin_results['condition_number']:.1f})"
                )
            for corr in collin_results['high_correlations']:
                results['warnings'].append(
                    f"High correlation ({corr['correlation']:.2f}) between "
                    f"{corr['variables'][0]} and {corr['variables'][1]}"
                )
        
        # Check linearity
        for group, group_results in linear_results.items():
            for pair, details in group_results.items():
                if 'error' not in details and not details['is_linear']:
                    results['assumptions_met'] = False
                    results['warnings'].append(
                        f"Non-linear relationship detected for {pair} in {group}"
                    )
        
        # Check sample size
        if not size_results['meets_min_size']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size in some groups "
                f"(minimum {size_results['min_group_size']} < "
                f"required {max(20, size_results['n_dependent_vars'] + 1)})"
            )
        
        if not size_results['more_dvs_than_groups']:
            results['warnings'].append(
                "Number of dependent variables should ideally be greater "
                "than number of groups"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Separate univariate ANOVAs with Bonferroni correction',
                'Robust MANOVA',
                'Permutation MANOVA',
                'Non-parametric multivariate tests (e.g., NPMANOVA)',
                'Linear Discriminant Analysis']
                                                                                                            
class OneWayANOVAChecker(AssumptionChecker, NormalityChecker, HomoscedasticityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              group_column: str, **kwargs) -> Dict:
        results = {
            'test_type': 'One-way ANOVA',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check normality within each group
        group_normality = {}
        for group in data[group_column].unique():
            group_data = data[data[group_column] == group]
            norm_results = self.check_normality(group_data, variables, self.alpha)
            group_normality[group] = norm_results
        
        results['details']['normality'] = group_normality
        
        # Check homogeneity of variance
        homo_results = self.check_homoscedasticity(data, variables, group_column, self.alpha)
        results['details']['homoscedasticity'] = homo_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(data, group_column)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, group_normality, homo_results, size_results)
        
        return results
    
    def _check_sample_size(self, data: pd.DataFrame, group_column: str) -> Dict:
        group_sizes = data.groupby(group_column).size()
        min_group_size = group_sizes.min()
        
        return {
            'group_sizes': group_sizes.to_dict(),
            'min_group_size': min_group_size,
            'requirement_met': min_group_size >= 30
        }
    
    def _update_results(self, results: Dict, group_normality: Dict,
                       homo_results: Dict, size_results: Dict) -> None:
        # Check normality in each group
        for group, norm_results in group_normality.items():
            for var, details in norm_results.items():
                if not details['is_normal']:
                    results['assumptions_met'] = False
                    results['warnings'].append(
                        f"Variable '{var}' in group '{group}' violates normality "
                        f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                    )
        
        # Check homoscedasticity
        for var, details in homo_results.items():
            if not details['is_homoscedastic']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates homoscedasticity assumption "
                    f"(Levene's test p={details['levene_p_value']:.4f})"
                )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size in some groups "
                f"(minimum {size_results['min_group_size']} < required 30)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Kruskal-Wallis H-test', 
                'Welch\'s ANOVA',
                'Brown-Forsythe test']

class FactorialANOVAChecker(AssumptionChecker, NormalityChecker, HomoscedasticityChecker):
    
    def check(self, data: pd.DataFrame, variables: List[str], 
              group_columns: List[str], **kwargs) -> Dict:
        results = {
            'test_type': 'Factorial ANOVA',
            'assumptions_met': True,
            'warnings': [],
            'details': {}
        }
        
        # Check normality for dependent variable
        dependent_var = variables[0]  # First variable is dependent
        norm_results = self.check_normality(data, [dependent_var], self.alpha)
        results['details']['normality'] = norm_results
        
        # Check homogeneity of variance across all group combinations
        # Create interaction term for all group columns
        data['_combined_groups'] = data[group_columns].apply(lambda x: '_'.join(x.astype(str)), axis=1)
        homo_results = self.check_homoscedasticity(data, [dependent_var], '_combined_groups', self.alpha)
        results['details']['homoscedasticity'] = homo_results
        
        # Check balanced design
        balance_results = self._check_balanced_design(data, group_columns)
        results['details']['balanced_design'] = balance_results
        
        # Check sample size requirements
        size_results = self._check_sample_size(data, group_columns)
        results['details']['sample_size'] = size_results
        
        # Update results
        self._update_results(results, norm_results, homo_results, 
                           balance_results, size_results)
        
        return results
    
    def _check_balanced_design(self, data: pd.DataFrame, 
                             group_columns: List[str]) -> Dict:
        # Get cell sizes for all combinations
        cell_sizes = data.groupby(group_columns).size()
        
        return {
            'cell_sizes': cell_sizes.to_dict(),
            'is_balanced': len(set(cell_sizes)) == 1,
            'min_cell_size': cell_sizes.min(),
            'max_cell_size': cell_sizes.max()
        }
    
    def _check_sample_size(self, data: pd.DataFrame,
                          group_columns: List[str]) -> Dict:
        # Rule of thumb: at least 30 observations per cell
        cell_sizes = data.groupby(group_columns).size()
        min_cell_size = cell_sizes.min()
        
        return {
            'min_cell_size': min_cell_size,
            'requirement_met': min_cell_size >= 30
        }
    
    def _update_results(self, results: Dict, norm_results: Dict,
                       homo_results: Dict, balance_results: Dict,
                       size_results: Dict) -> None:
        # Check normality
        for var, details in norm_results.items():
            if not details['is_normal']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates normality assumption "
                    f"(Shapiro-Wilk p={details['shapiro_p_value']:.4f})"
                )
        
        # Check homoscedasticity
        for var, details in homo_results.items():
            if not details['is_homoscedastic']:
                results['assumptions_met'] = False
                results['warnings'].append(
                    f"Variable '{var}' violates homoscedasticity assumption "
                    f"(Levene's test p={details['levene_p_value']:.4f})"
                )
        
        # Check balanced design
        if not balance_results['is_balanced']:
            results['warnings'].append(
                f"Unbalanced design detected (cell sizes range from "
                f"{balance_results['min_cell_size']} to {balance_results['max_cell_size']})"
            )
        
        # Check sample size
        if not size_results['requirement_met']:
            results['assumptions_met'] = False
            results['warnings'].append(
                f"Insufficient sample size in some cells "
                f"(minimum {size_results['min_cell_size']} < required 30)"
            )
    
    def get_alternative_tests(self) -> List[str]:
        return ['Non-parametric factorial analysis', 
                'Mixed-effects model',
                'Robust ANOVA']

class StatisticalTestAssumptions:
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
        self.checkers = {
            't_test_ind': IndependentTTestChecker(alpha),
            'repeated_anova': RepeatedMeasuresANOVAChecker(alpha),
            'logistic': LogisticRegressionChecker(alpha),
            'factorial_anova': FactorialANOVAChecker(alpha),
            'one_way_anova': OneWayANOVAChecker(alpha),
            'pearson_correlation': PearsonCorrelationChecker(alpha),
            'paired_ttest': PairedTTestChecker(alpha),
            'chi_square_independence': ChiSquareIndependenceChecker(alpha),
            'multiple_regression': MultipleRegressionChecker(alpha),
            'two_way_anova': TwoWayANOVAChecker(alpha),
            'kaplan_meier': KaplanMeierChecker(alpha),
            'cox_ph': CoxPHChecker(alpha),         
            'poisson': PoissonRegressionChecker(alpha),
            'spearman': SpearmanCorrelationChecker(alpha),
            'wilcoxon_signed_rank': WilcoxonSignedRankChecker(alpha),
            'manova': MANOVAChecker(alpha)
        }
    
    def check_assumptions(self, data: pd.DataFrame, test_type: str,
                         variables: List[str], **kwargs) -> Dict:

        if test_type not in self.checkers:
            raise ValueError(f"Unsupported test type. Choose from: {list(self.checkers.keys())}")
        
        checker = self.checkers[test_type]
        results = checker.check(data, variables, **kwargs)
        
        return results
    
    def get_recommendation(self, results: Dict) -> str:
        test_type = results['test_type']
        
        if results['assumptions_met']:
            return f"✓ All assumptions are met. You can proceed with the {test_type}."
        
        recommendation = f"⚠ Some assumptions for {test_type} are violated:\n\n"
        for warning in results['warnings']:
            recommendation += f"- {warning}\n"
        
        # Add alternative test suggestions
        test_type_to_checker = {
            'Pearson Correlation': 'pearson_correlation',
            'Independent t-test': 't_test_ind',
            'Repeated Measures ANOVA': 'repeated_anova',
            'One-way ANOVA': 'one_way_anova',
            'Factorial ANOVA': 'factorial_anova',
            'Logistic Regression': 'logistic',
            'MANOVA': 'manova',
            'Two-way ANOVA': 'two_way_anova',
            'Kaplan-Meier': 'kaplan_meier',
            'Cox PH': 'cox_ph',
            'Poisson Regression': 'poisson',
            'Spearman Correlation': 'spearman',
            'Wilcoxon Signed-Rank': 'wilcoxon_signed_rank',
            'Chi-Square Independence': 'chi_square_independence',
            'Multiple Regression': 'multiple_regression',
            'Paired t-test': 'paired_ttest'
        }
        
        checker_type = test_type_to_checker.get(test_type)
        if checker_type and checker_type in self.checkers:
            checker = self.checkers[checker_type]
            alternatives = checker.get_alternative_tests()
            if alternatives:
                recommendation += "\nConsider these alternatives:\n"
                for alt in alternatives:
                    recommendation += f"- {alt}\n"
        
        return recommendation
    
    def register_checker(self, test_type: str, checker: AssumptionChecker) -> None:

        if not isinstance(checker, AssumptionChecker):
            raise ValueError("Checker must inherit from AssumptionChecker")
        
        self.checkers[test_type] = checker
