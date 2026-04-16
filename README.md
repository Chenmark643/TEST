# ☕ Coffee Market Analysis Dashboard

An interactive Streamlit application for exploring global coffee commodity market trends, production data, and international trade patterns.

## Overview

This project is an interactive data analysis tool that allows users to explore the global coffee market through multiple analytical perspectives: commodity price trends, country-level production analysis, international trade patterns, and key economic insights.

**Target Audience:** Business students, analysts, and anyone interested in agricultural commodity markets.

## Features

- **📊 Overview Dashboard** — Key metrics and summary visualizations
- **📈 Price Trends** — Interactive charts for Arabica and Robusta prices with filtering
- **🌍 Production Analysis** — Country and regional production comparisons with year selection
- **🚢 Trade & Export** — International trade flow analysis and export ratios
- **🔍 Country Explorer** — Deep dive into individual producing countries
- **💡 Key Insights** — Analytical findings with supporting visualizations

## Dataset

The analysis uses data constructed from reference values published by:

| Source | Data Used | Access Date |
|--------|-----------|-------------|
| International Coffee Organization (ICO) | Commodity price benchmarks | April 2026 |
| World Bank Open Data | GDP, GDP per capita indicators | April 2026 |
| FAOSTAT | Production volume references | April 2026 |
| USDA Foreign Agricultural Service | Trade and export data | April 2026 |

**Data Period:** 2015–2024  
**Countries Covered:** Top 10 coffee-producing nations

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/coffee-market-analysis.git
cd coffee-market-analysis

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### Run the analysis notebook

```bash
jupyter notebook notebook.ipynb
```

## Project Structure

```
coffee-market-analysis/
├── app.py                  # Streamlit interactive dashboard
├── analysis.py             # Standalone analysis script (generates charts)
├── notebook.ipynb          # Jupyter notebook with full analytical workflow
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── REFLECTION.md           # Reflection report (500-800 words)
└── DEMO_SCRIPT.md          # Narration script for 1-3 min demo video
```

## Key Insights

1. **Brazil's Dominance** — Brazil accounts for ~37% of global coffee production, holding a commanding market position with both Arabica and Robusta varieties.

2. **Price Volatility** — The 2021-2022 period showed significant price spikes due to supply chain disruptions and adverse weather, highlighting market vulnerability.

3. **Regional Trade Patterns** — South America maintains the strongest net export surplus, reflecting the production strength of Brazil and Colombia.

4. **Emerging Producers** — Ethiopia and Honduras show strong production growth rates, suggesting gradual diversification of global supply.

5. **Economic Dependency** — Lower-income producing countries show higher export-to-production ratios, indicating significant economic dependence on coffee trade.

## Methodology

The analytical workflow follows these steps:

1. **Problem Definition** — Define the analytical question and target user
2. **Data Acquisition** — Construct datasets from authoritative reference sources
3. **Data Cleaning** — Validate data quality and compute derived metrics
4. **Descriptive Analysis** — Calculate summary statistics, trends, and concentration measures
5. **Visualization** — Create interactive charts using Plotly
6. **Insight Generation** — Interpret patterns and communicate findings

## Technologies Used

- **Python 3** — Core programming language
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical computation
- **Plotly** — Interactive visualizations
- **Streamlit** — Web application framework
- **Matplotlib** — Static chart generation (notebook)

## ACC102 Mini Assignment

This project fulfills the requirements for Track 4 (Interactive Data Analysis Tool) of the ACC102 Mini Assignment, 2nd Semester 2024-25.

---

*Built with ☕ and Python*
