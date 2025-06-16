"""
APPENDIX A: LINEAR PROGRAMMING IMPLEMENTATION FOR CHARGING STATION OPTIMIZATION

This implementation minimizes total infrastructure costs while satisfying:
- Budget constraints
- Charging demand requirements
- Geographical coverage thresholds
- Grid capacity limitations

Dependencies: PuLP (v2.7.0), pandas (v2.1.0)
"""
import pulp as pl

def optimize_charging_network(population_df, traffic_df, energy_df, 
                             budget=50_000_000,  # USD
                             max_distance=15):   # km
    """
    SOLVES EV CHARGING NETWORK OPTIMIZATION PROBLEM
    
    Parameters:
    population_df : DataFrame with ['City','Population','Potential_EVs_2035']
    traffic_df    : DataFrame with ['Source','Target','Daily_Traffic']
    energy_df     : DataFrame with ['City','Grid_Capacity_MW']
    
    Returns:
    results : Dict containing optimal locations/capacities
    prob    : PuLP problem object
    """
    # Initialize minimization problem
    prob = pl.LpProblem("EV_Charging_Network_Optimization", pl.LpMinimize)
    
    # --- PARAMETERS ---
    cities = list(population_df['City'])
    
    # Installation costs = Fixed + Population-dependent component
    installation_costs = {
        city: 500_000 + pop * 0.5 
        for city, pop in zip(population_df['City'], population_df['Population'])
    }
    
    # --- CONSTRAINTS ---
    # (Full implementation as previously provided)
    # ... [remainder of original code] ...
    
    return results, prob