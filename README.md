# Building Implied Volatility Curve for European Puts
This project constructs the implied volatility curve for 78 DTE European put options using strike/price data from Excel file. The Black-Scholes model is used to calculate the implied volatility for each strike price, and each option price as a function of volatility is plotted for a series of volatilities (0.01 to 0.30 sigma). This illustrates how option price changes for different volatilities. With each of these plots, linear interpolation is used to find the implied volatility for each market option price. For the last step, implied volatility is plotted against each strike price and the volatility smile is analyzed.

## Sigma Grid
A grid of sigmas/volatilities from 0.01 to 0.30 in increments of 0.01 was created. For each of these sigmas, the theoretical Black-Scholes option price was calculated using the equations:

<p align="center">
   <img src="https://github.com/user-attachments/assets/dca234b8-1863-4159-8326-15393b5e7906" alt="image">
</p>

Following the theoretical price calculation for each sigma, a plot of the theoretical price as a function of sigma was printed for each strike K.

## Analyzing Option Price vs Sigma Plots
The plots of price vs volatility revealed several trends (run Python code to see all 20 of them). First, clearly as the volatility of the underlying increases the price of the option increases. This is a well-known stylized fact of option prices, as well as a well-known result of the Black-Scholes pricing model. Second, the curve of each option shifts depending on how close the option is to being at the money. In other words, as the strike K approaches the underlying asset price x, the price curve has less of a “hockey stick” shape and becomes closer to a simple line. A noticeable difference at low sigmas (say 0.01 through 0.05) for options very in the money versus very out of the money is that the theoretical prices for OTM options is near 0 while those ITM can be very large (exceeding a value of 5, 10, and so on up to roughly 140). This makes sense since if the underlying is not likely to move very much (low volatility), then an option deep OTM is likely to remain there and expire worthless (0), while an option deep ITM is also likely to remain there and expire at some value significantly greater than 0. However, options with strikes ATM (near underlying price) have a nearly linear price vs. volatility relationship because there is a roughly 50/50 chance of expiring ITM or OTM. Even if the volatility is low, just a tiny move in the underlying asset price will move the option OTM or ITM and drastically impact its price.

## Linear Interpolation
Linear interpolation was used between the (price, sigma) points for each strike to derive the sigma given a price. In this case, the given price was the real market price. The output of this result is the implied volatility, which is shown as a function of the strike price below.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c69f4729-c7b4-4ed6-95fe-adc467cc9007" alt="image">
</p>

## Analysis of Volatility Curve/Smile
Clearly, the figure shows the implied volatility “smile.” As strike decreases or increases away from strikes near ATM, the implied volatility increases, leading to a “smile” shape. There were two strikes, 670 and 740, for which an implied volatility could not be calculated. This was because in my code I added a catch where if the market price is outside the range of all model prices calculated using sigmas 0.01 to 0.30, then linear interpolation can’t be done and NaN is output instead. For instance, for a strike of 670 the minimum theoretical price (where volatility is 0.01) is around 69. However, the market price is well below that at 59.59 so linear interpolation between points is not doable. Similarly, the minimum theoretical price for a strike of 740 is around 139 but the market price is 129.97, so linear interpolation again is not possible. Since both of the prices fall below their respective minimum theoretical prices, one could say the implied volatility is near 0 rather than NaN. One possible reason for these discrepancies is that options deep ITM are not traded very frequently, so the “last price” may have been recorded from a time at which the underlying price was substantially different from the current price of 594. Another reason may simply be that these options are not priced appropriately (underpriced) and a profitable opportunity is available.
