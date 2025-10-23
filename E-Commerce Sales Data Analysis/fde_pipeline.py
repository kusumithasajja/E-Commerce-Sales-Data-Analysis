#!/usr/bin/env python3
"""
E-Commerce Sales Data Analysis - FDE Pipeline
=============================================

This script implements a complete Extract, Transform, Load (ETL) pipeline
for e-commerce sales data analysis.

Pipeline Steps:
1. Extract: Load raw sales data from CSV
2. Transform: Clean and transform the data
3. Load: Store data in multiple formats (CSV, JSON, SQLite)
4. Analyze: Generate insights and visualizations

Author: FDE Project
Date: 2024
"""

import os
import sys
import logging
from datetime import datetime
import pandas as pd

# Import our custom modules
from clean import clean_sales_data
from transform import transform_sales_data
from load import load_all_data
from analyze import run_complete_analysis

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fde_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class FDEPipeline:
    """
    Main FDE Pipeline class that orchestrates the entire data processing workflow.
    """
    
    def __init__(self, input_file='sales.csv'):
        """
        Initialize the FDE Pipeline.
        
        Args:
            input_file (str): Path to input sales data file
        """
        self.input_file = input_file
        self.start_time = datetime.now()
        self.results = {}
        
        logger.info("="*60)
        logger.info("FDE PIPELINE INITIALIZED")
        logger.info("="*60)
        logger.info(f"Input file: {self.input_file}")
        logger.info(f"Start time: {self.start_time}")
        
    def extract(self):
        """
        Extract phase: Load raw data from source.
        
        Returns:
            pd.DataFrame: Raw sales data
        """
        logger.info("\n" + "="*40)
        logger.info("PHASE 1: EXTRACT")
        logger.info("="*40)
        
        try:
            if not os.path.exists(self.input_file):
                raise FileNotFoundError(f"Input file {self.input_file} not found!")
            
            # Load raw data
            raw_data = pd.read_csv(self.input_file)
            logger.info(f"Successfully extracted {len(raw_data)} rows from {self.input_file}")
            logger.info(f"Columns: {list(raw_data.columns)}")
            
            # Basic data validation
            logger.info("Performing basic data validation...")
            logger.info(f"Data shape: {raw_data.shape}")
            logger.info(f"Memory usage: {raw_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            self.results['extract'] = {
                'status': 'success',
                'rows': len(raw_data),
                'columns': len(raw_data.columns),
                'file': self.input_file
            }
            
            return raw_data
            
        except Exception as e:
            logger.error(f"Extract phase failed: {str(e)}")
            self.results['extract'] = {'status': 'failed', 'error': str(e)}
            raise
    
    def transform(self, raw_data):
        """
        Transform phase: Clean and transform the data.
        
        Args:
            raw_data (pd.DataFrame): Raw sales data
            
        Returns:
            pd.DataFrame: Transformed data
        """
        logger.info("\n" + "="*40)
        logger.info("PHASE 2: TRANSFORM")
        logger.info("="*40)
        
        try:
            # Step 1: Clean the data
            logger.info("Step 1: Cleaning data...")
            cleaned_data = clean_sales_data(self.input_file, 'cleaned_sales.csv')
            
            # Step 2: Transform the data
            logger.info("Step 2: Transforming data...")
            transformed_data, summary_stats = transform_sales_data('cleaned_sales.csv', 'transformed_sales.csv')
            
            self.results['transform'] = {
                'status': 'success',
                'cleaned_rows': len(cleaned_data),
                'transformed_rows': len(transformed_data),
                'summary_stats': summary_stats
            }
            
            logger.info("Transform phase completed successfully!")
            return transformed_data
            
        except Exception as e:
            logger.error(f"Transform phase failed: {str(e)}")
            self.results['transform'] = {'status': 'failed', 'error': str(e)}
            raise
    
    def load(self, transformed_data):
        """
        Load phase: Store data in multiple formats.
        
        Args:
            transformed_data (pd.DataFrame): Transformed sales data
            
        Returns:
            dict: Loading results
        """
        logger.info("\n" + "="*40)
        logger.info("PHASE 3: LOAD")
        logger.info("="*40)
        
        try:
            # Load data in all formats
            load_results = load_all_data('transformed_sales.csv')
            
            self.results['load'] = {
                'status': 'success',
                'formats': list(load_results.keys()),
                'files': load_results
            }
            
            logger.info("Load phase completed successfully!")
            return load_results
            
        except Exception as e:
            logger.error(f"Load phase failed: {str(e)}")
            self.results['load'] = {'status': 'failed', 'error': str(e)}
            raise
    
    def analyze(self):
        """
        Analyze phase: Generate insights and visualizations.
        
        Returns:
            dict: Analysis results
        """
        logger.info("\n" + "="*40)
        logger.info("PHASE 4: ANALYZE")
        logger.info("="*40)
        
        try:
            # Run complete analysis
            analysis_results = run_complete_analysis('sales_analysis.db')
            
            self.results['analyze'] = {
                'status': 'success',
                'charts_generated': [
                    'top_products_analysis.png',
                    'revenue_analysis.png',
                    'monthly_trends_analysis.png'
                ],
                'report_generated': 'analysis_report.json',
                'analysis_results': analysis_results
            }
            
            logger.info("Analyze phase completed successfully!")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Analyze phase failed: {str(e)}")
            self.results['analyze'] = {'status': 'failed', 'error': str(e)}
            raise
    
    def run_pipeline(self):
        """
        Run the complete FDE pipeline.
        
        Returns:
            dict: Complete pipeline results
        """
        logger.info("\n" + "="*60)
        logger.info("STARTING FDE PIPELINE EXECUTION")
        logger.info("="*60)
        
        try:
            # Phase 1: Extract
            raw_data = self.extract()
            
            # Phase 2: Transform
            transformed_data = self.transform(raw_data)
            
            # Phase 3: Load
            load_results = self.load(transformed_data)
            
            # Phase 4: Analyze
            analysis_results = self.analyze()
            
            # Calculate execution time
            end_time = datetime.now()
            execution_time = end_time - self.start_time
            
            # Final results
            self.results['pipeline'] = {
                'status': 'success',
                'execution_time': str(execution_time),
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'phases_completed': 4
            }
            
            logger.info("\n" + "="*60)
            logger.info("FDE PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f"Total execution time: {execution_time}")
            logger.info(f"Phases completed: 4/4")
            
            # Print summary
            self.print_summary()
            
            return self.results
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            self.results['pipeline'] = {
                'status': 'failed',
                'error': str(e),
                'execution_time': str(datetime.now() - self.start_time)
            }
            raise
    
    def print_summary(self):
        """
        Print a summary of the pipeline execution.
        """
        print("\n" + "="*80)
        print("FDE PIPELINE EXECUTION SUMMARY")
        print("="*80)
        
        # Pipeline status
        pipeline_status = self.results.get('pipeline', {})
        print(f"Status: {pipeline_status.get('status', 'Unknown').upper()}")
        print(f"Execution Time: {pipeline_status.get('execution_time', 'N/A')}")
        
        # Phase results
        phases = ['extract', 'transform', 'load', 'analyze']
        for phase in phases:
            phase_result = self.results.get(phase, {})
            status = phase_result.get('status', 'Unknown')
            print(f"{phase.capitalize()}: {status.upper()}")
        
        # Generated files
        print("\nGenerated Files:")
        print("- cleaned_sales.csv (Cleaned data)")
        print("- transformed_sales.csv (Transformed data)")
        print("- sales_analysis.db (SQLite database)")
        print("- sales_data.json (JSON format)")
        print("- data_warehouse/ (Data warehouse)")
        print("- top_products_analysis.png (Top products chart)")
        print("- revenue_analysis.png (Revenue analysis charts)")
        print("- monthly_trends_analysis.png (Monthly trends)")
        print("- analysis_report.json (Comprehensive report)")
        print("- fde_pipeline.log (Execution log)")
        
        # Key insights
        if 'analyze' in self.results and self.results['analyze']['status'] == 'success':
            print("\nKey Insights:")
            print("- Top products by revenue identified")
            print("- Monthly sales trends analyzed")
            print("- Revenue distribution by category and region")
            print("- Customer behavior patterns analyzed")
        
        print("="*80)

def main():
    """
    Main function to run the FDE pipeline.
    """
    try:
        # Initialize and run pipeline
        pipeline = FDEPipeline('sales.csv')
        results = pipeline.run_pipeline()
        
        print("\nFDE Pipeline completed successfully!")
        print("Check the generated files and charts for detailed analysis results.")
        
        return results
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        print(f"\nPipeline execution failed: {str(e)}")
        print("Check the log file 'fde_pipeline.log' for detailed error information.")
        return None

if __name__ == "__main__":
    main()
