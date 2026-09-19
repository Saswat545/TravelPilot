---
name: data-visualization
description: 'Create clear, effective data visualizations using matplotlib and seaborn for exploratory analysis and stakeholder communication.'
---
# Data Visualization

Transform complex data into clear, compelling visual representations that reveal patterns, trends, and insights.

## When to Use

- Exploratory data analysis and pattern discovery
- Communicating insights to stakeholders
- Comparing distributions and relationships
- Presenting findings in reports and dashboards
- Identifying outliers and anomalies visually
- Creating publication-ready charts and graphs

## Visualization Types

| Type | Chart | Best For |
|------|-------|----------|
| **Distributions** | Histogram, KDE, Violin | Understanding data spread |
| **Relationships** | Scatter, Line, Heatmap | Correlation analysis |
| **Comparisons** | Bar, Box, Ridge | Category comparison |
| **Compositions** | Pie, Stacked Bar, Treemap | Part-to-whole |
| **Temporal** | Line, Area, Time series | Trends over time |
| **Multivariate** | Pair plot, Correlation heatmap | Multi-dimensional analysis |

## Design Principles

1. Choose appropriate chart type for data
2. Minimize ink-to-data ratio
3. Use color purposefully
4. Label clearly and completely
5. Maintain consistent scales
6. Consider accessibility

## Quick Python Setup

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
```
