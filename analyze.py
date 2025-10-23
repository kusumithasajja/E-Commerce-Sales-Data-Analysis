import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def analyze_top_products(db_file='sales_analysis.db', top_n=10):
    """
    Analyze and visualize top products by revenue and quantity.
    
    Args:
        db_file (str): Path to SQLite database
        top_n (int): Number of top products to show
    
    Returns:
        pd.DataFrame: Top products analysis
    """
    logger.info(f"Analyzing top {top_n} products...")
    
    try:
        conn = sqlite3.connect(db_file)
        
        # Query top products by revenue
        query = """
        SELECT 
            product_name,
            SUM(total_amount) as total_revenue,
            SUM(quantity) as total_quantity,
            COUNT(*) as order_count,
            AVG(unit_price) as avg_unit_price
        FROM sales_data 
        GROUP BY product_name 
        ORDER BY total_revenue DESC 
        LIMIT ?
        """
        
        top_products = pd.read_sql_query(query, conn, params=(top_n,))
        conn.close()
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Top products by revenue
        ax1.barh(top_products['product_name'], top_products['total_revenue'])
        ax1.set_xlabel('Total Revenue ($)')
        ax1.set_title(f'Top {top_n} Products by Revenue')
        ax1.invert_yaxis()
        
        # Top products by quantity
        ax2.barh(top_products['product_name'], top_products['total_quantity'])
        ax2.set_xlabel('Total Quantity Sold')
        ax2.set_title(f'Top {top_n} Products by Quantity')
        ax2.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('top_products_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f"Top products analysis completed. Chart saved as 'top_products_analysis.png'")
        return top_products
        
    except Exception as e:
        logger.error(f"Error analyzing top products: {str(e)}")
        raise

def analyze_revenue_chart(db_file='sales_analysis.db'):
    """
    Create comprehensive revenue analysis charts.
    
    Args:
        db_file (str): Path to SQLite database
    
    Returns:
        dict: Revenue analysis results
    """
    logger.info("Creating revenue analysis charts...")
    
    try:
        conn = sqlite3.connect(db_file)
        
        # Monthly revenue trend
        monthly_query = """
        SELECT 
            year || '-' || printf('%02d', month) as month_year,
            SUM(total_amount) as monthly_revenue,
            COUNT(*) as monthly_orders
        FROM sales_data 
        GROUP BY year, month 
        ORDER BY year, month
        """
        
        monthly_data = pd.read_sql_query(monthly_query, conn)
        
        # Category revenue
        category_query = """
        SELECT 
            category,
            SUM(total_amount) as category_revenue,
            COUNT(*) as category_orders
        FROM sales_data 
        GROUP BY category 
        ORDER BY category_revenue DESC
        """
        
        category_data = pd.read_sql_query(category_query, conn)
        
        # Region revenue
        region_query = """
        SELECT 
            region,
            SUM(total_amount) as region_revenue,
            COUNT(*) as region_orders
        FROM sales_data 
        GROUP BY region 
        ORDER BY region_revenue DESC
        """
        
        region_data = pd.read_sql_query(region_query, conn)
        
        conn.close()
        
        # Create comprehensive revenue charts
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Monthly revenue trend
        ax1.plot(monthly_data['month_year'], monthly_data['monthly_revenue'], marker='o', linewidth=2)
        ax1.set_title('Monthly Revenue Trend')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Revenue ($)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Category revenue pie chart
        ax2.pie(category_data['category_revenue'], labels=category_data['category'], autopct='%1.1f%%')
        ax2.set_title('Revenue by Category')
        
        # Region revenue bar chart
        ax3.bar(region_data['region'], region_data['region_revenue'])
        ax3.set_title('Revenue by Region')
        ax3.set_xlabel('Region')
        ax3.set_ylabel('Revenue ($)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Monthly orders trend
        ax4.plot(monthly_data['month_year'], monthly_data['monthly_orders'], marker='s', color='orange', linewidth=2)
        ax4.set_title('Monthly Orders Trend')
        ax4.set_xlabel('Month')
        ax4.set_ylabel('Number of Orders')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('revenue_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Revenue analysis charts created and saved as 'revenue_analysis.png'")
        
        return {
            'monthly_data': monthly_data,
            'category_data': category_data,
            'region_data': region_data
        }
        
    except Exception as e:
        logger.error(f"Error creating revenue charts: {str(e)}")
        raise

def analyze_monthly_sales_trend(db_file='sales_analysis.db'):
    """
    Analyze monthly sales trends with detailed insights.
    
    Args:
        db_file (str): Path to SQLite database
    
    Returns:
        pd.DataFrame: Monthly trends analysis
    """
    logger.info("Analyzing monthly sales trends...")
    
    try:
        conn = sqlite3.connect(db_file)
        
        # Detailed monthly analysis
        monthly_query = """
        SELECT 
            year,
            month,
            SUM(total_amount) as monthly_revenue,
            SUM(quantity) as monthly_quantity,
            COUNT(*) as monthly_orders,
            COUNT(DISTINCT customer_id) as unique_customers,
            COUNT(DISTINCT product_name) as unique_products,
            AVG(total_amount) as avg_order_value
        FROM sales_data 
        GROUP BY year, month 
        ORDER BY year, month
        """
        
        monthly_trends = pd.read_sql_query(monthly_query, conn)
        
        # Calculate growth rates
        monthly_trends['revenue_growth'] = monthly_trends['monthly_revenue'].pct_change() * 100
        monthly_trends['orders_growth'] = monthly_trends['monthly_orders'].pct_change() * 100
        
        conn.close()
        
        # Create monthly trends visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Revenue trend
        ax1.plot(monthly_trends.index, monthly_trends['monthly_revenue'], marker='o', linewidth=2)
        ax1.set_title('Monthly Revenue Trend')
        ax1.set_xlabel('Month Index')
        ax1.set_ylabel('Revenue ($)')
        ax1.grid(True, alpha=0.3)
        
        # Orders trend
        ax2.plot(monthly_trends.index, monthly_trends['monthly_orders'], marker='s', color='green', linewidth=2)
        ax2.set_title('Monthly Orders Trend')
        ax2.set_xlabel('Month Index')
        ax2.set_ylabel('Number of Orders')
        ax2.grid(True, alpha=0.3)
        
        # Growth rates
        ax3.bar(monthly_trends.index[1:], monthly_trends['revenue_growth'][1:], alpha=0.7)
        ax3.set_title('Month-over-Month Revenue Growth (%)')
        ax3.set_xlabel('Month Index')
        ax3.set_ylabel('Growth Rate (%)')
        ax3.grid(True, alpha=0.3)
        
        # Average order value
        ax4.plot(monthly_trends.index, monthly_trends['avg_order_value'], marker='d', color='red', linewidth=2)
        ax4.set_title('Average Order Value Trend')
        ax4.set_xlabel('Month Index')
        ax4.set_ylabel('Average Order Value ($)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('monthly_trends_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("Monthly trends analysis completed. Chart saved as 'monthly_trends_analysis.png'")
        
        # Print summary statistics
        logger.info("Monthly Trends Summary:")
        logger.info(f"Average monthly revenue: ${monthly_trends['monthly_revenue'].mean():,.2f}")
        logger.info(f"Average monthly orders: {monthly_trends['monthly_orders'].mean():.1f}")
        logger.info(f"Average order value: ${monthly_trends['avg_order_value'].mean():.2f}")
        logger.info(f"Best performing month: {monthly_trends.loc[monthly_trends['monthly_revenue'].idxmax(), 'month']}/{monthly_trends.loc[monthly_trends['monthly_revenue'].idxmax(), 'year']}")
        
        return monthly_trends
        
    except Exception as e:
        logger.error(f"Error analyzing monthly trends: {str(e)}")
        raise

def generate_comprehensive_report(db_file='sales_analysis.db'):
    """
    Generate a comprehensive analysis report.
    
    Args:
        db_file (str): Path to SQLite database
    
    Returns:
        dict: Comprehensive analysis results
    """
    logger.info("Generating comprehensive analysis report...")
    
    try:
        conn = sqlite3.connect(db_file)
        
        # Overall statistics
        stats_query = """
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            SUM(quantity) as total_quantity,
            COUNT(DISTINCT customer_id) as unique_customers,
            COUNT(DISTINCT product_name) as unique_products,
            COUNT(DISTINCT category) as unique_categories,
            AVG(total_amount) as avg_order_value,
            MIN(order_date) as first_order_date,
            MAX(order_date) as last_order_date
        FROM sales_data
        """
        
        overall_stats = pd.read_sql_query(stats_query, conn).iloc[0]
        
        # Top performers
        top_products = pd.read_sql_query("""
            SELECT product_name, SUM(total_amount) as revenue 
            FROM sales_data 
            GROUP BY product_name 
            ORDER BY revenue DESC 
            LIMIT 5
        """, conn)
        
        top_categories = pd.read_sql_query("""
            SELECT category, SUM(total_amount) as revenue 
            FROM sales_data 
            GROUP BY category 
            ORDER BY revenue DESC 
            LIMIT 5
        """, conn)
        
        top_regions = pd.read_sql_query("""
            SELECT region, SUM(total_amount) as revenue 
            FROM sales_data 
            GROUP BY region 
            ORDER BY revenue DESC 
            LIMIT 5
        """, conn)
        
        conn.close()
        
        # Create summary report
        report = {
            'overall_statistics': overall_stats.to_dict(),
            'top_products': top_products.to_dict('records'),
            'top_categories': top_categories.to_dict('records'),
            'top_regions': top_regions.to_dict('records'),
            'analysis_date': datetime.now().isoformat()
        }
        
        # Save report to JSON
        import json
        with open('analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info("Comprehensive report generated and saved as 'analysis_report.json'")
        
        # Print summary to console
        print("\n" + "="*60)
        print("E-COMMERCE SALES DATA ANALYSIS REPORT")
        print("="*60)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Date Range: {overall_stats['first_order_date']} to {overall_stats['last_order_date']}")
        print(f"Total Revenue: ${overall_stats['total_revenue']:,.2f}")
        print(f"Total Orders: {overall_stats['total_orders']:,}")
        print(f"Total Quantity Sold: {overall_stats['total_quantity']:,}")
        print(f"Unique Customers: {overall_stats['unique_customers']:,}")
        print(f"Unique Products: {overall_stats['unique_products']:,}")
        print(f"Average Order Value: ${overall_stats['avg_order_value']:.2f}")
        
        print("\nTOP 5 PRODUCTS BY REVENUE:")
        for i, product in enumerate(top_products.iterrows(), 1):
            print(f"{i}. {product[1]['product_name']}: ${product[1]['revenue']:,.2f}")
        
        print("\nTOP 5 CATEGORIES BY REVENUE:")
        for i, category in enumerate(top_categories.iterrows(), 1):
            print(f"{i}. {category[1]['category']}: ${category[1]['revenue']:,.2f}")
        
        print("\nTOP 5 REGIONS BY REVENUE:")
        for i, region in enumerate(top_regions.iterrows(), 1):
            print(f"{i}. {region[1]['region']}: ${region[1]['revenue']:,.2f}")
        
        print("="*60)
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating comprehensive report: {str(e)}")
        raise

def run_complete_analysis():
    """
    Run the complete analysis pipeline.
    
    Returns:
        dict: Complete analysis results
    """
    logger.info("Starting complete analysis pipeline...")
    
    try:
        results = {}
        
        # Analyze top products
        top_products = analyze_top_products()
        results['top_products'] = top_products
        
        # Analyze revenue charts
        revenue_analysis = analyze_revenue_chart()
        results['revenue_analysis'] = revenue_analysis
        
        # Analyze monthly trends
        monthly_trends = analyze_monthly_sales_trend()
        results['monthly_trends'] = monthly_trends
        
        # Generate comprehensive report
        comprehensive_report = generate_comprehensive_report()
        results['comprehensive_report'] = comprehensive_report
        
        logger.info("Complete analysis pipeline finished successfully!")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in complete analysis pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    results = run_complete_analysis()
    print("\nAnalysis completed successfully!")
    print("Generated files:")
    print("- top_products_analysis.png")
    print("- revenue_analysis.png") 
    print("- monthly_trends_analysis.png")
    print("- analysis_report.json")
