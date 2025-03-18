import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.interpolate import interp1d

# Given parameters
tau = 0.2137 # Time until expiration in years
x = 594 # Underlying price
r = 0.045 # Interest rate

# Grid on sigma from 0.01 to 0.30 in increments of 0.01
sigma_grid = np.arange(0.01, 0.31, 0.01)

# Download Excel data
excel_data = pd.read_excel(r'C:\Users\willk\OneDrive\Desktop\Implied_Volatility_Curve_Data.xlsx')
strike_prices = excel_data['Strike Price']
market_prices = excel_data['Last Price']

# Initialize implied vol calcs
implied_vols = []

# Loop through each strike price and last/market put price
for K, market_price in zip(strike_prices, market_prices):
    
    # Initialize put prices computed via Black-Scholes
    put_prices_theor = []

    # Calculate theoretical put prices for each sigma
    for sigma in sigma_grid:
        d_plus = 1/(sigma * np.sqrt(tau)) * (np.log(x / K) + (r + sigma**2 / 2) * tau)
        d_minus = 1/(sigma * np.sqrt(tau)) * (np.log(x / K) + (r - sigma**2 / 2) * tau)
        put_price_theor = K * np.exp(-r * tau) * norm.cdf(-d_minus) - x * norm.cdf(-d_plus)
        put_prices_theor.append(put_price_theor)
    put_prices_theor = np.array(put_prices_theor)

    # Using points (sigma, p) plot a graph of theoretical option price as a function of volatility
    plt.figure(figsize=(8,6))
    plt.plot(sigma_grid, put_prices_theor, marker='o', linestyle='-')
    plt.xlabel("Volatility (σ)")
    plt.ylabel("Theoretical Put Price (p)")
    plt.title(f"Theoretical Put Price vs. Volatility for Strike K = {K}")
    plt.grid(True)
    plt.show()

    # In the event that the real price in market is outside range of all theoretical prices calculated, implied volatility is NaN
    if market_price < put_prices_theor.min() or market_price > put_prices_theor.max():
        implied_volatility = np.nan
    else:
        # If market price is within range of theoretical prices, use linear interpolation between the points (sigma, put_price) to solve for implied volatility
        linear_interpolation = interp1d(put_prices_theor, sigma_grid)
        implied_volatility = float(linear_interpolation(market_price))

    implied_vols.append(implied_volatility)

# Table of implied volatilities
implied_vols_table = pd.DataFrame({
    'Strike Price': strike_prices,
    'Market Price': market_prices,
    'Implied Volatility': implied_vols
})
print(implied_vols_table)

# Plot of strike prices versus implied volatility to show volatility smile
plt.figure(figsize=(8,6))
plt.plot(strike_prices, implied_vols, marker='o', linestyle='-')
plt.xlabel("Strike Price (K)")
plt.ylabel("Implied Volatility (σ)")
plt.title("Implied Volatility as a Function of Strike Price for European Put Options")
plt.grid(True)
plt.show()
