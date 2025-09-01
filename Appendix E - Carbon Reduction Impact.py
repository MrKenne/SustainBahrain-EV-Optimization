"""
APPENDIX E: CARBON REDUCTION IMPACT MODEL

This implementation quantifies CO₂ emission reductions from EV adoption by calculating:
- Annual vehicle kilometers displaced
- Fuel-to-electricity emission differentials
- Contribution to national carbon reduction targets

Methodology:
1. Computes avoided emissions from internal combustion engines
2. Accounts for grid emission intensity
3. Projects cumulative impact over infrastructure lifetime

Dependencies: None (pure Python)
"""

def calculate_carbon_impact(selected_locations, capacities, population_df, 
                           annual_km=15000,  # Average annual driving distance (km)
                           years=10):         # Analysis period
    """
    QUANTIFIES CO₂ REDUCTION FROM EV CHARGING NETWORK
    
    Parameters:
    selected_locations : List of implemented cities
    capacities         : Dict of {city: charging_points}
    population_df      : DataFrame with EV projections
    annual_km          : Avg km driven per EV annually (default 15,000)
    years              : Analysis timeframe (default 10 years)
    
    Returns:
    results : Dict of carbon impact metrics
    """
    # Emission factors (kg CO₂/km) [Sources: Wu et al. 2012, Teixeira & Sodre 2018]
    ICE_EMISSION_FACTOR = 0.18   # Internal combustion engine vehicles
    GRID_EMISSION_FACTOR = 0.12  # Bahrain grid intensity 
    EMISSION_REDUCTION_PER_KM = ICE_EMISSION_FACTOR - GRID_EMISSION_FACTOR
    
    # Calculate supported EVs based on charging capacity
    total_charging_points = sum(capacities.values())
    supported_evs = total_charging_points * 20  # 20 EVs per charger
    
    # Constrain by projected EV adoption
    total_projected_evs = population_df['Potential_EVs_2035'].sum()
    actual_evs = min(supported_evs, total_projected_evs)
    
    # Annual emissions reduction (tons CO₂)
    annual_vkm_reduction = actual_evs * annual_km
    annual_co2_reduction_tons = (annual_vkm_reduction 
                                 * EMISSION_REDUCTION_PER_KM 
                                 / 1000)  # Convert kg to tons
    
    # Cumulative reduction with adoption growth
    cumulative_reduction = 0
    for year in range(1, years + 1):
        adoption_rate = min(1.0, year / years)  # Linear growth to full adoption
        cumulative_reduction += annual_co2_reduction_tons * adoption_rate
    
    # Contextualize against national emissions
    BAHRAIN_TOTAL_CO2_2022 = 34.411e6  # Metric tons (IEA 2023)
    TRANSPORT_SHARE = 0.20              # 20% of national emissions
    
    transport_emissions = BAHRAIN_TOTAL_CO2_2022 * TRANSPORT_SHARE
    transport_impact_pct = (annual_co2_reduction_tons / transport_emissions) * 100
    
    # Compare to 2035 target (30% reduction from 2022 levels)
    TARGET_REDUCTION = BAHRAIN_TOTAL_CO2_2022 * 0.30
    target_contribution_pct = (annual_co2_reduction_tons / TARGET_REDUCTION) * 100
    
    return {
        'supported_evs': supported_evs,
        'actual_evs': actual_evs,
        'annual_co2_reduction_tons': annual_co2_reduction_tons,
        'cumulative_reduction_tons': cumulative_reduction,
        'pct_of_transport_emissions': transport_impact_pct,
        'pct_of_2035_target': target_contribution_pct
    }