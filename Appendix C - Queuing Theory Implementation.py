"""
APPENDIX C: QUEUEING THEORY IMPLEMENTATION FOR CAPACITY PLANNING

This implementation analyzes charging station performance using M/M/c queue models to:
- Estimate average waiting times (Wq)
- Calculate system utilization (ρ)
- Determine optimal charger counts
- Ensure service quality constraints (Wq ≤ W_max)

Dependencies: pandas (v2.1.0), numpy (v1.24.3)
"""

import numpy as np
import pandas as pd

def analyze_charging_station_queues(selected_locations, capacities, population_df):
    """
    ANALYZES QUEUE METRICS FOR OPTIMIZED CHARGING STATIONS
    
    Parameters:
    selected_locations : List of cities with charging stations
    capacities         : Dict of {city: charger_count}
    population_df      : DataFrame with demographic/EV data
    
    Returns:
    results_df : DataFrame of queue performance metrics
    """
    results = []
    
    for city in selected_locations:
        # Extract city-specific data
        city_data = population_df[population_df['City'] == city].iloc[0]
        potential_evs_2035 = city_data['Potential_EVs_2035']
        
        # Calculate arrival rate (λ)
        daily_charging_demand = potential_evs_2035 * 0.1  # 10% daily charging need
        hourly_arrival_rate = daily_charging_demand / 16   # Distributed over 16 operational hours
        
        # Service rate (μ = 2 vehicles/hour/charger = 30 min service time)
        service_rate = 2  
        num_chargers = capacities[city]  # Number of servers (c)
        
        # Compute M/M/c queue metrics
        metrics = mmc_queue_metrics(hourly_arrival_rate, service_rate, num_chargers)
        
        # Handle unstable queues (ρ ≥ 1)
        if not metrics:
            results.append({
                'City': city,
                'Arrival_Rate_λ': hourly_arrival_rate,
                'Chargers_c': num_chargers,
                'Utilization_ρ': 1.0,
                'Avg_Queue_Length_Lq': np.inf,
                'Avg_Waiting_Time_Wq': np.inf
            })
        else:
            results.append({
                'City': city,
                'Arrival_Rate_λ': hourly_arrival_rate,
                'Chargers_c': num_chargers,
                'Utilization_ρ': metrics['utilization'],
                'Avg_Queue_Length_Lq': metrics['avg_queue_length'],
                'Avg_Waiting_Time_Wq': metrics['avg_waiting_time']
            })
    
    return pd.DataFrame(results)

def mmc_queue_metrics(λ, μ, c):
    """
    SOLVES M/M/c QUEUE SYSTEM EQUATIONS
    
    Parameters:
    λ : Arrival rate (vehicles/hour)
    μ : Service rate per server (vehicles/hour)
    c : Number of servers
    
    Returns:
    metrics : Dict of queue performance indicators
    """
    # Check queue stability (ρ < 1 required)
    ρ = λ / (c * μ)
    if ρ >= 1:
        return None  # Unstable system
    
    # Calculate P₀ (probability of empty system)
    sum_term = sum([(c*ρ)**n / np.math.factorial(n) for n in range(c)])
    p0_denominator = sum_term + (c*ρ)**c / (np.math.factorial(c) * (1 - ρ))
    P₀ = 1 / p0_denominator
    
    # Calculate Lq (average queue length)
    Lq = (P₀ * (c*ρ)**c * ρ) / (np.math.factorial(c) * (1 - ρ)**2)
    
    # Calculate performance metrics
    L = Lq + λ / μ       # Average vehicles in system
    W = L / λ            # Average time in system (hours)
    Wq = Lq / λ          # Average waiting time (hours)
    
    return {
        'utilization': ρ,
        'avg_system_count': L,
        'avg_queue_length': Lq,
        'avg_system_time': W,
        'avg_waiting_time': Wq
    }