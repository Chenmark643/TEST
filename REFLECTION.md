# Reflection Report: Coffee Market Analysis Dashboard

## Analytical Problem and Intended User

The analytical problem addressed in this project is: *How have global coffee commodity prices evolved, and what patterns exist in the production and trade of coffee among major producing countries?* The intended user is business students and professionals who need a quick, interactive way to understand commodity market dynamics. Rather than reading static reports, users can explore the data themselves through filtering, country selection, and year-based comparisons, making the tool suitable for both learning and preliminary market research.

## Dataset Description and Selection Rationale

The project uses three interconnected datasets covering coffee commodity prices, country-level production, and regional trade flows for the period 2015–2024. Reference data were drawn from the International Coffee Organization (ICO), World Bank Open Data, FAOSTAT, and USDA Foreign Agricultural Service, all accessed in April 2026. Coffee was selected as the subject because it is one of the most traded agricultural commodities globally, offering rich opportunities to explore price volatility, geographic concentration, and the relationship between commodity exports and national economic indicators. The top 10 producing countries were included, representing over 90% of global output, ensuring coverage of the most significant market participants.

## Python Methods Used

The analytical workflow was implemented entirely in Python. Pandas was used for data loading, cleaning, transformation, and aggregation — including computing annual averages, year-over-year price changes, and market share percentages. NumPy was used for generating realistic time-series data with seasonal components and controlled noise. Plotly provided interactive visualizations including line charts for price trends, bar charts for production comparisons, pie charts for market share, scatter plots for cross-variable relationships, and area charts for country-level production trends. Streamlit was used to package the analysis into an interactive web application with sidebar navigation, user-driven filtering, and responsive layout. The Herfindahl-Hirschman Index (HHI) was calculated as a simple measure of market concentration, adding a quantitative dimension to the qualitative observations.

## Main Insights and Outputs

Five key insights emerged from the analysis. First, Brazil's dominance in coffee production is overwhelming, accounting for approximately 37% of global output — more than double the second-largest producer, Vietnam. Second, coffee prices exhibited significant volatility, particularly during the 2021–2022 period when supply chain disruptions and adverse weather in Brazil drove Arabica prices to a multi-year peak. Third, South America consistently leads in net coffee exports, reinforcing its central role in global supply. Fourth, emerging producers such as Ethiopia and Honduras show strong growth trajectories, suggesting gradual diversification of supply sources. Fifth, there is a clear inverse relationship between a country's GDP per capita and its dependence on coffee exports, with lower-income nations like Honduras and Uganda exporting a higher proportion of their production.

## Limitations, Reliability, and Possible Improvements

The primary limitation is that the datasets, while based on real-world reference values, were constructed rather than directly downloaded from live APIs. This means specific monthly price figures are approximations, not exact historical records. For a production-grade analysis, connecting directly to APIs such as the World Bank API or Yahoo Finance would improve accuracy. Additionally, the analysis is descriptive and does not include predictive modelling or causal inference — for example, identifying the specific weather events or policy changes that drove price spikes. Future improvements could include integrating real-time data feeds, adding a forecasting module using time-series methods such as ARIMA or Prophet, and incorporating sentiment analysis from coffee industry news. The Streamlit app could also benefit from user authentication and the ability to save custom views or export charts.

## Personal Contribution and Learning

My contribution included designing the analytical framework, constructing the datasets from authoritative reference sources, implementing the full Python workflow from data cleaning through interactive visualization, building the Streamlit application, and synthesising the analytical findings. Through this project, I gained practical experience in product thinking — designing not just an analysis, but a user-facing tool that communicates value. I also deepened my understanding of commodity market structures and the economic factors that shape agricultural trade. The iterative process of building, testing, and refining the dashboard taught me the importance of user-centred design in data products.

## AI Use Disclosure

- **Tool:** ChatGPT (GPT-4), accessed April 2026  
  **Used for:** Assistance with Streamlit layout structure, Plotly chart configuration, and code debugging suggestions.

- **Tool:** GitHub Copilot, accessed April 2026  
  **Used for:** Code autocompletion during development of data processing functions.

All analytical decisions, dataset construction, insight interpretation, and final product design were my own work. AI tools were used as coding assistants rather than analytical substitutes.
