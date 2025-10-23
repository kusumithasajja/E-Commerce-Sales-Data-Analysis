#!/usr/bin/env python3
"""
Flask Web Application for E-Commerce Sales Data Analysis
========================================================

This Flask app serves the analysis results from the FDE pipeline
and provides a web interface to view all insights and visualizations.

Author: FDE Project
Date: 2024
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3
import json
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class DataService:
    """Service class to handle data operations"""
    
    def __init__(self, db_path='sales_analysis.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_overall_stats(self):
        """Get overall statistics"""
        try:
            conn = self.get_connection()
            
            query = """
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
            
            stats = pd.read_sql_query(query, conn).iloc[0]
            conn.close()
            
            return {
                'total_revenue': float(stats['total_revenue']),
                'total_orders': int(stats['total_orders']),
                'total_quantity': int(stats['total_quantity']),
                'unique_customers': int(stats['unique_customers']),
                'unique_products': int(stats['unique_products']),
                'unique_categories': int(stats['unique_categories']),
                'avg_order_value': float(stats['avg_order_value']),
                'first_order_date': stats['first_order_date'],
                'last_order_date': stats['last_order_date']
            }
            
        except Exception as e:
            logger.error(f"Error getting overall stats: {str(e)}")
            return {}
    
    def get_monthly_data(self):
        """Get monthly sales data"""
        try:
            conn = self.get_connection()
            
            query = """
            SELECT 
                year || '-' || printf('%02d', month) as month_year,
                SUM(total_amount) as monthly_revenue,
                COUNT(*) as monthly_orders,
                SUM(quantity) as monthly_quantity,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM sales_data 
            GROUP BY year, month 
            ORDER BY year, month
            """
            
            monthly_data = pd.read_sql_query(query, conn)
            conn.close()
            
            return monthly_data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting monthly data: {str(e)}")
            return []
    
    def get_category_data(self):
        """Get category analysis data"""
        try:
            conn = self.get_connection()
            
            query = """
            SELECT 
                category,
                SUM(total_amount) as category_revenue,
                SUM(quantity) as category_quantity,
                COUNT(*) as category_orders,
                COUNT(DISTINCT product_name) as unique_products
            FROM sales_data 
            GROUP BY category 
            ORDER BY category_revenue DESC
            """
            
            category_data = pd.read_sql_query(query, conn)
            conn.close()
            
            return category_data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting category data: {str(e)}")
            return []
    
    def get_region_data(self):
        """Get region analysis data"""
        try:
            conn = self.get_connection()
            
            query = """
            SELECT 
                region,
                SUM(total_amount) as region_revenue,
                SUM(quantity) as region_quantity,
                COUNT(*) as region_orders,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM sales_data 
            GROUP BY region 
            ORDER BY region_revenue DESC
            """
            
            region_data = pd.read_sql_query(query, conn)
            conn.close()
            
            return region_data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting region data: {str(e)}")
            return []
    
    def get_top_products(self, limit=10):
        """Get top products analysis"""
        try:
            conn = self.get_connection()
            
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
            
            top_products = pd.read_sql_query(query, conn, params=(limit,))
            conn.close()
            
            return top_products.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting top products: {str(e)}")
            return []
    
    def get_customer_analysis(self):
        """Get customer analysis data"""
        try:
            conn = self.get_connection()
            
            query = """
            SELECT 
                customer_id,
                SUM(total_amount) as total_spent,
                SUM(quantity) as total_quantity,
                COUNT(*) as total_orders,
                COUNT(DISTINCT product_name) as unique_products,
                COUNT(DISTINCT category) as unique_categories
            FROM sales_data 
            GROUP BY customer_id 
            ORDER BY total_spent DESC 
            LIMIT 10
            """
            
            customer_data = pd.read_sql_query(query, conn)
            conn.close()
            
            return customer_data.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error getting customer analysis: {str(e)}")
            return []

# Initialize data service
data_service = DataService()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """API endpoint for overall statistics"""
    try:
        stats = data_service.get_overall_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/monthly')
def get_monthly():
    """API endpoint for monthly data"""
    try:
        monthly_data = data_service.get_monthly_data()
        return jsonify({
            'success': True,
            'data': monthly_data
        })
    except Exception as e:
        logger.error(f"Error in get_monthly: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories')
def get_categories():
    """API endpoint for category data"""
    try:
        category_data = data_service.get_category_data()
        return jsonify({
            'success': True,
            'data': category_data
        })
    except Exception as e:
        logger.error(f"Error in get_categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/regions')
def get_regions():
    """API endpoint for region data"""
    try:
        region_data = data_service.get_region_data()
        return jsonify({
            'success': True,
            'data': region_data
        })
    except Exception as e:
        logger.error(f"Error in get_regions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/top-products')
def get_top_products():
    """API endpoint for top products"""
    try:
        limit = request.args.get('limit', 10, type=int)
        top_products = data_service.get_top_products(limit)
        return jsonify({
            'success': True,
            'data': top_products
        })
    except Exception as e:
        logger.error(f"Error in get_top_products: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/customers')
def get_customers():
    """API endpoint for customer analysis"""
    try:
        customer_data = data_service.get_customer_analysis()
        return jsonify({
            'success': True,
            'data': customer_data
        })
    except Exception as e:
        logger.error(f"Error in get_customers: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/complete-data')
def get_complete_data():
    """API endpoint for all data at once"""
    try:
        complete_data = {
            'stats': data_service.get_overall_stats(),
            'monthly': data_service.get_monthly_data(),
            'categories': data_service.get_category_data(),
            'regions': data_service.get_region_data(),
            'top_products': data_service.get_top_products(),
            'customers': data_service.get_customer_analysis(),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': complete_data
        })
    except Exception as e:
        logger.error(f"Error in get_complete_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check if database exists and is accessible
        if os.path.exists(data_service.db_path):
            conn = data_service.get_connection()
            conn.execute("SELECT 1")
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'not_found',
                'timestamp': datetime.now().isoformat()
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('sales_analysis.db'):
        print("⚠️  Database not found! Please run the FDE pipeline first:")
        print("   python fde_pipeline.py")
        print("\nStarting web app anyway for demo purposes...")
    
    print("🚀 Starting E-Commerce Sales Analysis Web App...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔗 API endpoints available at: http://localhost:5000/api/")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)



