# 🌟 **AlphaFlex Growth Portfolio (AFG)**  

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

[![ETF Type: Growth](https://img.shields.io/badge/ETF%20Type-Growth-yellow.svg)](https://github.com/AlphaFlexETF/Details)



[![5D Return: 4.23%](https://img.shields.io/badge/5D%20Return-4.23%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![1M Return: 5.34%](https://img.shields.io/badge/1M%20Return-5.34%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![3M Return: 110.84%](https://img.shields.io/badge/3M%20Return-110.84%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![6M Return: 138.21%](https://img.shields.io/badge/6M%20Return-138.21%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![1Y Return: 212%](https://img.shields.io/badge/1Y%20Return-212%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![2Y Return: 424.22%](https://img.shields.io/badge/2Y%20Return-424.22%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)
[![5Y Return: 301.01%](https://img.shields.io/badge/5Y%20Return-301.01%25-brightgreen.svg)](https://github.com/AlphaFlexETF/Performance)


---

> **Disclaimer**: This is a project aimed at exploring the concept of a portfolio that automatically adjusts itself every week in response to market movements, with the goal of reducing risk and increasing returns. The project leverages advanced quantitative models and strategies, but it is not intended as financial or investment advice. The performance of this portfolio is for educational and research purposes only, and any investments based on this project should be made with caution and after thorough research.

Please note that the portfolio you are querying is a model portfolio as of December 1, 2024, and does not reflect the updated and rebalanced portfolio as of today. This model excludes the proprietary strategy employed in selecting these stocks. For access to the real-time, updated portfolio, please contact us directly.

---

## 🛠️ **Installation & Usage**

Install AlphaFlex Growth Portfolio to have full access to AlphaFlex toolkit, including scripts for backtesting, optimization, and analysis.

```bash
pip install alpha-flex

from alpha_flex import get_portfolio, backtest_portfolio

# Get portfolio data
portfolio_df = get_portfolio() 
portfolio_df

#Get Portfolio Performance over different periods - 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
result = backtest_portfolio(investment_amount, period='1y')
result
```


## 🎯 **Table of Contents**
1. [Overview](#-overview)
2. [Core Features](#-core-features)
3. [Portfolio Construction Methodology](#-portfolio-construction-methodology)
4. [Performance Metrics](#-performance-metrics)
5. [Installation & Usage](#️-installation--usage)
6. [Repository Structure](#-repository-structure)
7. [Why Choose AlphaFlex?](#-why-choose-alphaflex)

---

## 🚀 **Overview**

The **AlphaFlex Growth ETF (AFG)** is a next-generation exchange-traded fund designed to capitalize on high-growth opportunities while minimizing risks. By leveraging a unique blend of **fundamental analysis**, **technical indicators**, and **quantitative optimization**, AFG empowers investors to achieve sustainable market-beating returns.

### Key Objectives:
- 📈 **Sustainable Growth**: Identify high-growth companies with robust earnings and sales metrics.
- 🛡️ **Risk Management**: Minimize volatility and drawdowns through disciplined portfolio construction.
- 🌍 **Diversification**: Achieve balanced exposure across sectors and industries for consistent performance.

---

## 🧠 **Core Features**

### 📊 **1. High Earnings Growth**
The High Earnings Growth approach emphasizes identifying companies with consistently robust earnings growth over multiple periods. This method seeks out businesses that demonstrate operational efficiency, strong demand for their products or services, and competitive advantages that enable them to scale profitably. Companies meeting these criteria are often market leaders with clear visibility into their future growth trajectories, making them ideal candidates for inclusion in the AlphaFlex portfolio.

---

### 📈 **2. High Sales Growth**
High Sales Growth focuses on companies that exhibit significant revenue expansion alongside financial prudence. This approach identifies firms with the ability to scale operations, capture market share, and maintain fiscal discipline, as evidenced by healthy balance sheets and high returns on equity. The methodology also accounts for management quality and their ability to sustain this growth while managing external risks effectively.

---

### 🤝 **3. Consistent Growth on a Bullish Trend**
The Consistent Growth on a Bullish Trend method leverages both fundamental and technical metrics to identify stocks with a proven track record of earnings expansion and positive market momentum. This dual-focus strategy emphasizes companies that not only deliver strong financial performance but also exhibit a robust upward price trajectory, signaling sustained investor confidence.

---

### 🛡️ **4. CANSLIM**
Inspired by William O’Neil’s investment framework, the CANSLIM method combines growth, momentum, and operational excellence. This approach identifies companies with a blend of earnings and sales growth, positive market sentiment, and strong technical performance. It also considers management quality and broader industry trends to ensure a comprehensive assessment of each stock's potential.

---

## 📐 Portfolio Construction Methodology

The **AlphaFlex Growth ETF (AFG)** is built upon a systematic, data-driven approach to construct a diversified portfolio of high-growth stocks. The portfolio construction methodology leverages various factors including market cap, revenue, volatility, and technical indicators to assign weights to each stock. Below is a detailed explanation of the steps involved in portfolio construction:

### 1. **Stock Selection and Screening**
   - **Country Filter**: The ETF exclusively includes stocks from the United States and Canada to ensure regulatory consistency and market familiarity.
   - **Stock Screening**: The stocks are selected based on various quantitative factors

### 2. **Weight Assignment**
   Once stocks are selected for inclusion in the ETF, different methodologies are used to assign a weight to each stock in the portfolio. These weightings are designed to balance between growth potential, risk, and diversification. The weight assignment methods include:

   - **Market Cap Weighting**: Stocks are weighted based on their market capitalization. Larger companies generally receive a larger weight, reflecting their established presence in the market. The market cap weight for each stock is calculated as:
     ```plaintext
     Market Cap Weight = Stock Market Cap / Total Market Cap of Portfolio
     ```

   - **Equal Weighting**: Each stock receives an equal weight in the portfolio, ensuring a broad diversification across all included stocks. The equal weight for each stock is calculated as:
     ```plaintext
     Equal Weight = 1 / Total Number of Stocks
     ```

   - **Fundamental Weighting (Revenue-based)**: Stocks are weighted according to their total revenue, prioritizing companies with higher revenue, which often correlates with stability and growth potential. The weight for each stock based on revenue is:
     ```plaintext
     Fundamental Weight = Stock Revenue / Total Revenue of Portfolio
     ```

   - **Volatility Weighting (Inverse of Volatility)**: To minimize risk, stocks with lower price volatility are given higher weights. This method emphasizes stability by allocating more to stocks with less price fluctuation. The volatility weight for each stock is:
     ```plaintext
     Volatility Weight = (1 / Volatility) / Σ (1 / Volatility of All Stocks)
     ```
     where **Volatility** is calculated as the standard deviation of the stock’s daily closing price over the past year.

   - **Log-Scaled Market Cap Weighting**: For scaling purposes and to avoid disproportionate influence from extremely large companies, the market cap is log-transformed before weighting. This method reduces the impact of exceptionally large companies without excluding them from the portfolio:
     ```plaintext
     Log Market Cap Weight = log(Market Cap + 1) / Σ log(Market Cap of All Stocks + 1)
     ```

### 3. **Final Weight Adjustment**
   After calculating individual weights using the above methods, the final weight for each stock is determined by adjusting and combining the different weightings to achieve a balanced portfolio. The adjusted weight for each stock is computed as a weighted average of the different weight categories:
   ```plaintext
   Adjusted Weight = 0.3 × Log Market Cap Weight + 0.15 × Equal Weight + 0.15 × Volatility Weight + 0.4 × Fundamental Weight
   ```
---


## 📊 **Performance Metrics**

| **Metric**                | **Target**                |
|---------------------------|---------------------------|
| **Annualized Return (CAGR)** | 40%–100%                 |
| **Beta**                  | 0.9–1.1                  |
| **Maximum Drawdown**      | -15% to -25%             |

AlphaFlex is designed to deliver **superior long-term returns** while maintaining a moderate risk profile, making it ideal for investors seeking consistent outperformance.

---

## 🌟 Why Choose AlphaFlex? ##
AlphaFlex offers an unparalleled investment opportunity by combining the best practices of quantitative finance with modern risk management.

**📈 Growth Potential**: High-growth companies with proven track records of performance.

**🛡️ Risk Mitigation**: Diversification, beta control, and strict screening rules ensure a balanced approach.

**🌍 Global Reach**: Exposure to a diversified portfolio of global equities.

**🧠 Transparency**: Open-source tools and robust documentation make AlphaFlex a model of investor trust.

AlphaFlex is more than an ETF—it's a comprehensive investment solution designed for outperformance in a dynamic market environment.



