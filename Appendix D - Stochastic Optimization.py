"""
APPENDIX D: STOCHASTIC OPTIMIZATION FOR EV ADOPTION UNCERTAINTY

This implementation generates probabilistic scenarios for EV adoption uncertainty using:
- Base adoption rates (low/medium/high scenarios)
- Region-specific multipliers (truncated normal distribution)
- Demographic weighting by city population

The methodology enables:
1. Risk-averse infrastructure planning
2. Sensitivity analysis of adoption variability
3. Robust optimization under uncertainty

Dependencies: numpy (v1.24.3), pandas (v2.1.0)
"""

import numpy as np

def generate_ev_adoption_scenarios(population_df, num_scenarios=100, seed=42):
    """
    GENERATES PROBABILISTIC EV ADOPTION SCENARIOS
    
    Parameters:
    population_df : DataFrame with columns:
        - 'City'
        - 'EV_Adoption_Rate_2035' (base scenario rate)
        - 'Population'
    num_scenarios : Number of scenarios to generate (default=100)
    seed          : Random seed for reproducibility (default=42)
    
    Returns:
    scenarios : List of dictionaries with scenario data
    """
    # Initialize random generator with fixed seed
    rng = np.random.default_rng(seed)
    
    # Extract base data
    base_rates = population_df['EV_Adoption_Rate_2035'].values
    cities = population_df['City'].values
    populations = population_df['Population'].values
    
    scenarios = []
    
    for i in range(num_scenarios):
        # Generate regional multipliers (μ=1.0, σ=0.2)
        multipliers = rng.normal(loc=1.0, scale=0.2, size=len(cities))
        
        # Apply constraints: 0.5 ≤ multiplier ≤ 1.5
        multipliers = np.clip(multipliers, 0.5, 1.5)
        
        # Calculate scenario-specific adoption rates
        scenario_rates = base_rates * multipliers
        
        # Apply upper bound (80% max adoption)
        scenario_rates = np.minimum(scenario_rates, 0.8)
        
        # Calculate EV counts
        scenario_evs = (populations * scenario_rates).astype(int)
        
        scenarios.append({
            'scenario_id': i,
            'cities': cities,
            'adoption_rates': scenario_rates,
            'ev_counts': scenario_evs,
            'total_evs': scenario_evs.sum()
        })
    
    return scenarios