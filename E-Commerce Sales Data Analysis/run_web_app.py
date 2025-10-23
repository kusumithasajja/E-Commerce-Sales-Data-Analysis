#!/usr/bin/env python3
"""
Simple script to run the web application
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting E-Commerce Sales Analysis Web App...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔗 API endpoints available at: http://localhost:5000/api/")
    print("\nPress Ctrl+C to stop the server")
    print("="*60)
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Web application stopped by user")
    except Exception as e:
        print(f"\n❌ Error running web application: {e}")
        print("\n💡 Alternative: Open 'web_dashboard.html' in your browser for a static version")

if __name__ == "__main__":
    main()



