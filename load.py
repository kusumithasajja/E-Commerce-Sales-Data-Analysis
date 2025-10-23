import pandas as pd
import sqlite3
import json
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_to_database(input_file='transformed_sales.csv', db_name='sales_analysis.db'):
    """
    Load transformed data into SQLite database for analysis.
    
    Args:
        input_file (str): Path to transformed CSV file
        db_name (str): Name of SQLite database file
    
    Returns:
        str: Database file path
    """
    logger.info(f"Loading data from {input_file} to database {db_name}")
    
    try:
        # Load transformed data
        df = pd.read_csv(input_file)
        df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Create database connection
        conn = sqlite3.connect(db_name)
        
        # Load main sales data
        df.to_sql('sales_data', conn, if_exists='replace', index=False)
        logger.info("Loaded main sales data to 'sales_data' table")
        
        # Load summary tables if they exist
        summary_files = [
            'product_summary.csv',
            'category_summary.csv', 
            'monthly_sales.csv',
            'region_summary.csv',
            'customer_summary.csv'
        ]
        
        for summary_file in summary_files:
            if os.path.exists(summary_file):
                summary_df = pd.read_csv(summary_file)
                table_name = summary_file.replace('.csv', '').replace('_', '')
                summary_df.to_sql(table_name, conn, if_exists='replace', index=False)
                logger.info(f"Loaded {summary_file} to '{table_name}' table")
        
        # Create indexes for better query performance
        logger.info("Creating database indexes...")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales_data(order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON sales_data(product_name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales_data(category)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON sales_data(region)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_customer_id ON sales_data(customer_id)")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database {db_name} created successfully with indexes")
        return db_name
        
    except Exception as e:
        logger.error(f"Error loading data to database: {str(e)}")
        raise

def load_to_json(input_file='transformed_sales.csv', output_file='sales_data.json'):
    """
    Load transformed data to JSON format for web applications.
    
    Args:
        input_file (str): Path to transformed CSV file
        output_file (str): Path to output JSON file
    
    Returns:
        str: JSON file path
    """
    logger.info(f"Converting {input_file} to JSON format")
    
    try:
        # Load transformed data
        df = pd.read_csv(input_file)
        df['order_date'] = pd.to_datetime(df['order_date'])
        
        # Convert datetime to string for JSON serialization
        df['order_date'] = df['order_date'].dt.strftime('%Y-%m-%d')
        
        # Convert to JSON
        df.to_json(output_file, orient='records', date_format='iso')
        
        logger.info(f"Data converted to JSON and saved to {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Error converting to JSON: {str(e)}")
        raise

def create_data_warehouse():
    """
    Create a comprehensive data warehouse structure.
    
    Returns:
        dict: Data warehouse information
    """
    logger.info("Creating data warehouse structure...")
    
    try:
        # Create data warehouse directory
        warehouse_dir = 'data_warehouse'
        os.makedirs(warehouse_dir, exist_ok=True)
        
        # Load all summary data
        summary_data = {}
        
        summary_files = {
            'products': 'product_summary.csv',
            'categories': 'category_summary.csv',
            'monthly': 'monthly_sales.csv',
            'regions': 'region_summary.csv',
            'customers': 'customer_summary.csv'
        }
        
        for key, filename in summary_files.items():
            if os.path.exists(filename):
                df = pd.read_csv(filename)
                summary_data[key] = df.to_dict('records')
                logger.info(f"Loaded {key} summary data")
        
        # Create comprehensive data warehouse JSON
        warehouse_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'version': '1.0',
                'description': 'E-Commerce Sales Data Warehouse'
            },
            'summary_statistics': summary_data,
            'data_sources': {
                'raw_data': 'sales.csv',
                'cleaned_data': 'cleaned_sales.csv',
                'transformed_data': 'transformed_sales.csv',
                'database': 'sales_analysis.db'
            }
        }
        
        # Save warehouse data
        warehouse_file = os.path.join(warehouse_dir, 'warehouse_data.json')
        with open(warehouse_file, 'w') as f:
            json.dump(warehouse_data, f, indent=2, default=str)
        
        logger.info(f"Data warehouse created at {warehouse_file}")
        
        # Create data dictionary
        data_dictionary = {
            'sales_data': {
                'order_id': 'Unique identifier for each order',
                'product_name': 'Name of the product',
                'category': 'Product category',
                'quantity': 'Number of items ordered',
                'unit_price': 'Price per unit',
                'total_amount': 'Total amount for the order',
                'customer_id': 'Unique customer identifier',
                'order_date': 'Date of the order',
                'region': 'Geographic region',
                'month': 'Month of the order',
                'year': 'Year of the order',
                'day_of_week': 'Day of the week',
                'quarter': 'Quarter of the year',
                'is_weekend': 'Boolean indicating if order was placed on weekend',
                'revenue_segment': 'Revenue category (Low, Medium, High, Very High)',
                'quantity_segment': 'Quantity category (Single, Small, Medium, Large)'
            }
        }
        
        dictionary_file = os.path.join(warehouse_dir, 'data_dictionary.json')
        with open(dictionary_file, 'w') as f:
            json.dump(data_dictionary, f, indent=2)
        
        logger.info(f"Data dictionary created at {dictionary_file}")
        
        return {
            'warehouse_dir': warehouse_dir,
            'warehouse_file': warehouse_file,
            'dictionary_file': dictionary_file,
            'summary_data': summary_data
        }
        
    except Exception as e:
        logger.error(f"Error creating data warehouse: {str(e)}")
        raise

def load_all_data():
    """
    Main function to load data in all formats.
    
    Returns:
        dict: Loading results
    """
    logger.info("Starting comprehensive data loading process...")
    
    results = {}
    
    try:
        # Load to database
        db_file = load_to_database()
        results['database'] = db_file
        
        # Load to JSON
        json_file = load_to_json()
        results['json'] = json_file
        
        # Create data warehouse
        warehouse_info = create_data_warehouse()
        results['warehouse'] = warehouse_info
        
        logger.info("Data loading completed successfully!")
        logger.info(f"Database: {db_file}")
        logger.info(f"JSON: {json_file}")
        logger.info(f"Warehouse: {warehouse_info['warehouse_dir']}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in data loading process: {str(e)}")
        raise

if __name__ == "__main__":
    results = load_all_data()
    print("\nData loading completed successfully!")
    print("Files created:")
    for format_type, file_path in results.items():
        if isinstance(file_path, dict):
            print(f"{format_type}: {file_path.get('warehouse_dir', 'N/A')}")
        else:
            print(f"{format_type}: {file_path}")
