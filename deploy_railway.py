#!/usr/bin/env python3
"""
Railway Deployment Script for Terabytes Legal AI
This script helps deploy the Flask app to Railway platform
"""

import os
import subprocess
import sys

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI is installed")
            return True
        else:
            print("❌ Railway CLI not found")
            return False
    except FileNotFoundError:
        print("❌ Railway CLI not found")
        return False

def install_railway_cli():
    """Install Railway CLI"""
    print("📦 Installing Railway CLI...")
    try:
        if sys.platform == "win32":
            # Windows
            subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        else:
            # macOS/Linux
            subprocess.run(['curl', '-fsSL', 'https://railway.app/install.sh'], check=True)
        print("✅ Railway CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Railway CLI")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    try:
        # Login to Railway
        subprocess.run(['railway', 'login'], check=True)
        
        # Initialize Railway project
        subprocess.run(['railway', 'init'], check=True)
        
        # Deploy
        subprocess.run(['railway', 'up'], check=True)
        
        print("✅ Successfully deployed to Railway!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    print("🚀 Railway Deployment Script for Terabytes Legal AI")
    print("=" * 50)
    
    # Check Railway CLI
    if not check_railway_cli():
        if not install_railway_cli():
            print("❌ Cannot proceed without Railway CLI")
            return
    
    # Deploy
    if deploy_to_railway():
        print("\n🎉 Deployment successful!")
        print("Your app should be live on Railway!")
    else:
        print("\n❌ Deployment failed!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
