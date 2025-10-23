# E-Commerce Sales Data Analysis - FDE Project

## Overview

This project implements a complete **Extract, Transform, Load (ETL)** pipeline for analyzing e-commerce sales data. The pipeline follows the FDE (Extract, Transform, Load) approach to process static sales data and generate comprehensive insights.

## Project Structure

```
E-Commerce Sales Data Analysis/
├── sales.csv                 # Raw sales data
├── clean.py                  # Data cleaning module
├── transform.py             # Data transformation module
├── load.py                  # Data loading module
├── analyze.py               # Data analysis module
├── fde_pipeline.py         # Main pipeline orchestrator
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

- **Data Cleaning**: Handle missing values, duplicates, and data inconsistencies
- **Data Transformation**: Create aggregations, derived features, and summary statistics
- **Data Loading**: Store data in multiple formats (CSV, JSON, SQLite, Data Warehouse)
- **Data Analysis**: Generate insights, visualizations, and comprehensive reports

## Outputs Generated

1. **Top Products Analysis**: Charts showing best-performing products by revenue and quantity
2. **Revenue Charts**: Comprehensive revenue analysis by category, region, and time
3. **Monthly Sales Trends**: Detailed monthly sales patterns and growth analysis
4. **Comprehensive Report**: JSON report with key insights and statistics

## Installation

1. **Clone or download** this project to your local machine
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

Run the complete FDE pipeline:

```bash
python fde_pipeline.py
```

This will execute all phases:
- **Extract**: Load raw data from `sales.csv`
- **Transform**: Clean and transform the data
- **Load**: Store in multiple formats
- **Analyze**: Generate insights and visualizations

### Individual Components

You can also run individual components:

```bash
# Data cleaning only
python clean.py

# Data transformation only
python transform.py

# Data loading only
python load.py

# Analysis only
python analyze.py
```

## Generated Files

After running the pipeline, you'll find these files:

### Data Files
- `cleaned_sales.csv` - Cleaned sales data
- `transformed_sales.csv` - Transformed sales data with new features
- `sales_analysis.db` - SQLite database with all data
- `sales_data.json` - JSON format for web applications
- `data_warehouse/` - Complete data warehouse structure

### Summary Files
- `product_summary.csv` - Product-level aggregations
- `category_summary.csv` - Category-level aggregations
- `monthly_sales.csv` - Monthly sales aggregations
- `region_summary.csv` - Region-level aggregations
- `customer_summary.csv` - Customer-level aggregations

### Analysis Outputs
- `top_products_analysis.png` - Top products visualization
- `revenue_analysis.png` - Revenue analysis charts
- `monthly_trends_analysis.png` - Monthly trends visualization
- `analysis_report.json` - Comprehensive analysis report
- `fde_pipeline.log` - Execution log

## Data Schema

### Input Data (sales.csv)
| Column | Type | Description |
|--------|------|-------------|
| order_id | String | Unique order identifier |
| product_name | String | Name of the product |
| category | String | Product category |
| quantity | Integer | Number of items ordered |
| unit_price | Float | Price per unit |
| total_amount | Float | Total amount for the order |
| customer_id | String | Unique customer identifier |
| order_date | Date | Date of the order |
| region | String | Geographic region |

### Transformed Data Features
- `month` - Month of the order
- `year` - Year of the order
- `day_of_week` - Day of the week
- `quarter` - Quarter of the year
- `is_weekend` - Boolean for weekend orders
- `revenue_segment` - Revenue category (Low, Medium, High, Very High)
- `quantity_segment` - Quantity category (Single, Small, Medium, Large)

## Analysis Insights

The pipeline generates several key insights:

1. **Top Products**: Best-performing products by revenue and quantity
2. **Revenue Trends**: Monthly revenue patterns and growth rates
3. **Category Analysis**: Revenue distribution across product categories
4. **Regional Analysis**: Sales performance by geographic region
5. **Customer Behavior**: Order patterns and customer segmentation

## Customization

### Adding New Data Sources
1. Update the `input_file` parameter in `fde_pipeline.py`
2. Modify the data schema in `clean.py` if needed
3. Adjust transformations in `transform.py` for new features

### Custom Analysis
1. Add new analysis functions in `analyze.py`
2. Update the `run_complete_analysis()` function
3. Modify visualizations as needed

### Database Schema
The SQLite database includes:
- `sales_data` - Main sales table with indexes
- `productsummary` - Product aggregations
- `categorysummary` - Category aggregations
- `monthlysales` - Monthly aggregations
- `regionsummary` - Region aggregations
- `customersummary` - Customer aggregations

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **File Not Found**: Ensure `sales.csv` exists in the project directory
3. **Permission Errors**: Check file write permissions in the directory
4. **Memory Issues**: For large datasets, consider processing in chunks

### Log Files
Check `fde_pipeline.log` for detailed execution information and error messages.

## Performance

- **Small datasets** (< 10K rows): ~30 seconds
- **Medium datasets** (10K-100K rows): ~2-5 minutes
- **Large datasets** (> 100K rows): Consider optimization

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check the log files for error details
2. Review the troubleshooting section
3. Create an issue with detailed error information

---

**Happy Analyzing!** 🚀📊



