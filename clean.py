import pandas as pd
import numpy as np
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_sales_data(input_file='sales.csv', output_file='cleaned_sales.csv'):
    """
    Clean the sales data by handling missing values, duplicates, and data type issues.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output cleaned CSV file
    
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    logger.info(f"Starting data cleaning process for {input_file}")
    
    try:
        # Load the data
        df = pd.read_csv(input_file)
        logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
        
        # Display initial data info
        logger.info("Initial data info:")
        logger.info(f"Shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        logger.info(f"Data types:\n{df.dtypes}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        logger.info(f"Missing values:\n{missing_values}")
        
        # Handle missing values
        if missing_values.sum() > 0:
            logger.info("Handling missing values...")
            # For numeric columns, fill with median
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
                    logger.info(f"Filled missing values in {col} with median")
            
            # For categorical columns, fill with mode
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                if df[col].isnull().sum() > 0:
                    mode_value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                    df[col].fillna(mode_value, inplace=True)
                    logger.info(f"Filled missing values in {col} with mode: {mode_value}")
        
        # Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        # Convert data types
        logger.info("Converting data types...")
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['quantity'] = df['quantity'].astype(int)
        df['unit_price'] = df['unit_price'].astype(float)
        df['total_amount'] = df['total_amount'].astype(float)
        
        # Validate data consistency
        logger.info("Validating data consistency...")
        
        # Check if total_amount = quantity * unit_price
        calculated_total = df['quantity'] * df['unit_price']
        inconsistent_rows = abs(df['total_amount'] - calculated_total) > 0.01
        if inconsistent_rows.sum() > 0:
            logger.warning(f"Found {inconsistent_rows.sum()} rows with inconsistent total_amount")
            df.loc[inconsistent_rows, 'total_amount'] = calculated_total[inconsistent_rows]
            logger.info("Corrected inconsistent total_amount values")
        
        # Remove rows with negative values
        negative_rows = (df['quantity'] < 0) | (df['unit_price'] < 0) | (df['total_amount'] < 0)
        if negative_rows.sum() > 0:
            logger.warning(f"Removing {negative_rows.sum()} rows with negative values")
            df = df[~negative_rows]
        
        # Clean text data
        logger.info("Cleaning text data...")
        df['product_name'] = df['product_name'].str.strip()
        df['category'] = df['category'].str.strip()
        df['region'] = df['region'].str.strip()
        
        # Add derived columns for analysis
        df['month'] = df['order_date'].dt.month
        df['year'] = df['order_date'].dt.year
        df['month_year'] = df['order_date'].dt.to_period('M')
        
        # Save cleaned data
        df.to_csv(output_file, index=False)
        logger.info(f"Cleaned data saved to {output_file}")
        logger.info(f"Final cleaned data shape: {df.shape}")
        
        # Display summary statistics
        logger.info("Cleaned data summary:")
        logger.info(f"Date range: {df['order_date'].min()} to {df['order_date'].max()}")
        logger.info(f"Total revenue: ${df['total_amount'].sum():,.2f}")
        logger.info(f"Total orders: {len(df)}")
        logger.info(f"Unique products: {df['product_name'].nunique()}")
        logger.info(f"Unique customers: {df['customer_id'].nunique()}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error during data cleaning: {str(e)}")
        raise

if __name__ == "__main__":
    cleaned_df = clean_sales_data()
    print("\nData cleaning completed successfully!")
    print(f"Cleaned dataset shape: {cleaned_df.shape}")
    print("\nFirst 5 rows of cleaned data:")
    print(cleaned_df.head())
