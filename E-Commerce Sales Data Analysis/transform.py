import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def transform_sales_data(input_file='cleaned_sales.csv', output_file='transformed_sales.csv'):
    """
    Transform the cleaned sales data by creating aggregations and derived features.
    
    Args:
        input_file (str): Path to cleaned CSV file
        output_file (str): Path to output transformed CSV file
    
    Returns:
        pd.DataFrame: Transformed dataframe
    """
    logger.info(f"Starting data transformation process for {input_file}")
    
    try:
        # Load cleaned data
        df = pd.read_csv(input_file)
        df['order_date'] = pd.to_datetime(df['order_date'])
        logger.info(f"Loaded {len(df)} rows for transformation")
        
        # Create product-level aggregations
        logger.info("Creating product-level aggregations...")
        product_summary = df.groupby('product_name').agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'order_id': 'count',
            'unit_price': 'mean'
        }).round(2)
        
        product_summary.columns = ['total_quantity_sold', 'total_revenue', 'order_count', 'avg_unit_price']
        product_summary['avg_order_value'] = (product_summary['total_revenue'] / product_summary['order_count']).round(2)
        product_summary = product_summary.reset_index()
        
        # Create category-level aggregations
        logger.info("Creating category-level aggregations...")
        category_summary = df.groupby('category').agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'order_id': 'count',
            'product_name': 'nunique'
        }).round(2)
        
        category_summary.columns = ['total_quantity_sold', 'total_revenue', 'order_count', 'unique_products']
        category_summary['avg_order_value'] = (category_summary['total_revenue'] / category_summary['order_count']).round(2)
        category_summary = category_summary.reset_index()
        
        # Create monthly sales aggregations
        logger.info("Creating monthly sales aggregations...")
        monthly_sales = df.groupby(['year', 'month']).agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique'
        }).round(2)
        
        monthly_sales.columns = ['monthly_revenue', 'monthly_quantity', 'monthly_orders', 'unique_customers']
        monthly_sales['avg_order_value'] = (monthly_sales['monthly_revenue'] / monthly_sales['monthly_orders']).round(2)
        monthly_sales = monthly_sales.reset_index()
        
        # Create region-level aggregations
        logger.info("Creating region-level aggregations...")
        region_summary = df.groupby('region').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique',
            'product_name': 'nunique'
        }).round(2)
        
        region_summary.columns = ['total_revenue', 'total_quantity', 'total_orders', 'unique_customers', 'unique_products']
        region_summary['avg_order_value'] = (region_summary['total_revenue'] / region_summary['total_orders']).round(2)
        region_summary = region_summary.reset_index()
        
        # Create customer-level aggregations
        logger.info("Creating customer-level aggregations...")
        customer_summary = df.groupby('customer_id').agg({
            'total_amount': 'sum',
            'quantity': 'sum',
            'order_id': 'count',
            'product_name': 'nunique',
            'category': 'nunique'
        }).round(2)
        
        customer_summary.columns = ['total_spent', 'total_quantity', 'total_orders', 'unique_products', 'unique_categories']
        customer_summary['avg_order_value'] = (customer_summary['total_spent'] / customer_summary['total_orders']).round(2)
        customer_summary = customer_summary.reset_index()
        
        # Create time-based features
        logger.info("Creating time-based features...")
        df['day_of_week'] = df['order_date'].dt.day_name()
        df['quarter'] = df['order_date'].dt.quarter
        df['is_weekend'] = df['order_date'].dt.dayofweek >= 5
        
        # Create revenue segments
        logger.info("Creating revenue segments...")
        df['revenue_segment'] = pd.cut(df['total_amount'], 
                                     bins=[0, 100, 500, 1000, float('inf')], 
                                     labels=['Low', 'Medium', 'High', 'Very High'])
        
        # Create quantity segments
        df['quantity_segment'] = pd.cut(df['quantity'], 
                                       bins=[0, 1, 3, 5, float('inf')], 
                                       labels=['Single', 'Small', 'Medium', 'Large'])
        
        # Create comprehensive summary
        logger.info("Creating comprehensive summary...")
        summary_stats = {
            'total_revenue': df['total_amount'].sum(),
            'total_orders': len(df),
            'total_quantity': df['quantity'].sum(),
            'unique_customers': df['customer_id'].nunique(),
            'unique_products': df['product_name'].nunique(),
            'unique_categories': df['category'].nunique(),
            'avg_order_value': df['total_amount'].mean(),
            'date_range_days': (df['order_date'].max() - df['order_date'].min()).days,
            'most_popular_product': df.groupby('product_name')['quantity'].sum().idxmax(),
            'most_popular_category': df.groupby('category')['quantity'].sum().idxmax(),
            'top_region': df.groupby('region')['total_amount'].sum().idxmax()
        }
        
        # Save transformed data
        df.to_csv(output_file, index=False)
        logger.info(f"Transformed data saved to {output_file}")
        
        # Save summary files
        product_summary.to_csv('product_summary.csv', index=False)
        category_summary.to_csv('category_summary.csv', index=False)
        monthly_sales.to_csv('monthly_sales.csv', index=False)
        region_summary.to_csv('region_summary.csv', index=False)
        customer_summary.to_csv('customer_summary.csv', index=False)
        
        logger.info("Summary files created:")
        logger.info("- product_summary.csv")
        logger.info("- category_summary.csv")
        logger.info("- monthly_sales.csv")
        logger.info("- region_summary.csv")
        logger.info("- customer_summary.csv")
        
        # Display transformation summary
        logger.info("Transformation completed successfully!")
        logger.info(f"Transformed dataset shape: {df.shape}")
        logger.info(f"Total revenue: ${summary_stats['total_revenue']:,.2f}")
        logger.info(f"Total orders: {summary_stats['total_orders']}")
        logger.info(f"Average order value: ${summary_stats['avg_order_value']:.2f}")
        logger.info(f"Most popular product: {summary_stats['most_popular_product']}")
        logger.info(f"Most popular category: {summary_stats['most_popular_category']}")
        logger.info(f"Top region: {summary_stats['top_region']}")
        
        return df, summary_stats
        
    except Exception as e:
        logger.error(f"Error during data transformation: {str(e)}")
        raise

if __name__ == "__main__":
    transformed_df, stats = transform_sales_data()
    print("\nData transformation completed successfully!")
    print(f"Transformed dataset shape: {transformed_df.shape}")
    print("\nSummary statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
