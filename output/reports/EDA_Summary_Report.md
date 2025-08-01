# Churn Prediction and Customer Segmentation - EDA Summary Report

## Executive Summary

This exploratory data analysis examines customer churn patterns in a telecommunications dataset with **505,207 customers** and **12 features**. The analysis reveals significant insights about customer behavior, subscription patterns, and key factors driving churn.

## Dataset Overview

### Basic Statistics
- **Total Records**: 505,207 customers
- **Features**: 12 columns including customer demographics, usage patterns, and subscription details
- **Data Quality**: Each column contains exactly 1 missing value
- **No Duplicates**: Dataset is clean with no duplicate records

### Key Findings Summary
- **Churn Rate**: 55.5% (280,492 churned vs 224,714 retained)
- **Age Range**: 18-65 years with peak around age 50
- **Subscription Types**: Basic, Standard, Premium
- **Contract Types**: Monthly, Quarterly, Annual

---

## 1. Data Ingestion and Validation

### Dataset Structure
```
Shape: (505,207, 12)
Features: CustomerID, Age, Gender, Tenure, Usage Frequency, Support Calls, 
         Payment Delay, Subscription Type, Contract Length, Total Spend, 
         Last Interaction, Churn
```

### Data Quality Assessment
- **Missing Values**: 1 missing value per column (minimal impact)
- **Duplicates**: 0 duplicate records
- **Data Types**: Mixed (numerical and categorical)

---

## 2. Target Variable Analysis

### Churn Distribution
![Churn Distribution](output/charts/churn_distribution.png)

**Key Insights:**
- **Churn Rate**: 55.5% of customers have churned
- **Retention Rate**: 44.5% of customers are retained
- **Business Impact**: Higher churn than retention indicates need for robust retention strategy

---

## 3. Univariate Analysis

### Age Distribution
![Age Distribution](output/charts/age_distribution.png)

**Key Insights:**
- **Age Range**: Customers span 18-65 years
- **Peak Demographic**: Clear spike around age 50 (14,000+ customers)
- **Declining Engagement**: Rapid decline after age 50 (below 8,000 customers)
- **Young Market**: Limited engagement in under-25 age group

### Subscription Type Distribution
![Subscription Type Distribution](output/charts/subscription_type_distribution.png)

**Key Insights:**
- Distribution across Basic, Standard, and Premium tiers
- Indicates diverse customer base with varying service needs

### Contract Length Distribution
![Contract Length Distribution](output/charts/contract_length_distribution.png)

**Key Insights:**
- Three contract types: Monthly, Quarterly, Annual
- Contract length appears to be a key retention factor

### Usage Frequency Distribution
![Usage Frequency Distribution](output/charts/usage_frequency_distribution.png)

**Key Insights:**
- Shows variation in customer engagement levels
- Usage patterns may correlate with churn behavior

### Last Interaction Distribution
![Last Interaction Distribution](output/charts/last_interaction_distribution.png)

**Key Insights:**
- **High Early Engagement**: Strong interaction in first 0-14 days (~20,000 customers)
- **Declining Activity**: Progressive drop after day 15 (12,500-15,000 by day 30)
- **Engagement Window**: First two weeks critical for customer retention

---

## 4. Bivariate Analysis

### Subscription Type vs Total Spend by Churn
![Subscription Type vs Total Spend](output/charts/subscription_type_total_spend.png)

**Key Insights:**
- **Premium Value**: Premium customers show highest spending regardless of churn status
- **Churn Impact**: Churned customers consistently spend less across all subscription types
- **Revenue Risk**: Lower spending patterns among churned customers indicate revenue loss

### Churn vs Tenure
![Churn vs Tenure](output/charts/churn_tenure.png)

**Key Insights:**
- Tenure relationship with churn behavior
- Longer tenure may indicate higher loyalty

### Contract Length vs Churn
![Contract Length vs Churn](output/charts/contract_length_churn.png)

**Key Insights:**
- **Monthly Contracts**: High churn risk with disproportionate churn rates
- **Annual Contracts**: Strong retention with low churn rates
- **Quarterly Contracts**: Moderate retention between monthly and annual

### Subscription Type vs Churn
![Subscription Type vs Churn](output/charts/subscription_type_churn.png)

**Key Insights:**
- Different churn patterns across subscription tiers
- Premium vs Basic vs Standard retention comparison

---

## 5. Correlation Analysis

### Correlation Heatmap
![Correlation Heatmap](output/charts/heatmap.png)

### Key Correlations with Churn:

| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| **Support Calls** | +0.52 | Strong positive - More support calls = Higher churn risk |
| **Payment Delay** | +0.33 | Moderate positive - Payment delays indicate churn risk |
| **Total Spend** | -0.37 | Moderate negative - Higher spenders less likely to churn |
| **Contract Length** | -0.30 | Moderate negative - Longer contracts reduce churn |
| **CustomerID** | -0.65 | Data artifact - Should be excluded from modeling |

---

## 6. Business Insights and Recommendations

### Critical Risk Factors
1. **Support Calls (0.52 correlation)**: High support call volume indicates customer frustration
2. **Payment Delays (0.33 correlation)**: Financial strain or dissatisfaction signals
3. **Contract Type**: Monthly contracts show highest churn risk

### Retention Opportunities
1. **High-Value Customers**: Premium subscribers and high spenders show better retention
2. **Contract Strategy**: Annual contracts significantly reduce churn
3. **Early Engagement**: First 15 days critical for customer relationship

### Strategic Recommendations

#### Immediate Actions
- **Support Quality**: Improve customer service to reduce support call volume
- **Contract Incentives**: Promote annual contracts with attractive pricing
- **Early Engagement**: Implement robust onboarding program for first 15 days

#### Long-term Strategy
- **Premium Upselling**: Focus on converting customers to higher-value subscriptions
- **Payment Solutions**: Offer flexible payment options to reduce delays
- **Age-Targeted Marketing**: Develop strategies for under-25 and over-50 demographics

---

## 7. Technical Implementation Notes

### Data Preprocessing Applied
- Categorical variables encoded (Basic=1, Standard=2, Premium=3)
- Contract length encoded (Monthly=1, Quarterly=2, Annual=3)
- Gender encoded (Female=0, Male=1)

### Visualization Assets
All charts saved to `/output/charts/` directory:
- `churn_distribution.png`
- `age_distribution.png`
- `subscription_type_distribution.png`
- `contract_length_distribution.png`
- `usage_frequency_distribution.png`
- `last_interaction_distribution.png`
- `subscription_type_total_spend.png`
- `churn_tenure.png`
- `contract_length_churn.png`
- `subscription_type_churn.png`
- `heatmap.png`

---

## 8. Next Steps

### Model Development
1. **Feature Engineering**: Create additional features based on EDA insights
2. **Model Selection**: Test classification algorithms (Logistic Regression, Random Forest, etc.)
3. **Customer Segmentation**: Develop targeted retention strategies

### Business Intelligence
1. **Dashboard Creation**: Real-time churn monitoring
2. **A/B Testing**: Test retention strategies on high-risk segments
3. **ROI Analysis**: Quantify impact of retention initiatives

---

*Report Generated: July 30, 2025*  
*Data Source: telcom_behavior.csv (505,207 records)*  
*Analysis Tool: Jupyter Notebook with Python (pandas, matplotlib, seaborn)*
