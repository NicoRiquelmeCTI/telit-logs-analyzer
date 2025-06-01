#!/usr/bin/env python3
"""
Main entry point for the Connectivity Analyzer application.
This script serves as a development entry point and example usage.
For production use, use the analyze_log.py script instead.
"""

import logging
from pathlib import Path
from datetime import datetime

from connectivity_analyzer.infrastructure.repositories import LogFileConnectivityRepository
from connectivity_analyzer.application.use_cases import GenerateConnectivityReportUseCase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'connectivity_analyzer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Initialize application environment and validate configuration."""
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Validate environment
    logger.info("Validating environment...")
    # Add any environment validation here
    
    logger.info("Environment setup completed")

def example_usage():
    """Demonstrate example usage of the application."""
    logger.info("Starting example analysis...")
    
    # Example 1: Basic analysis
    try:
        repository = LogFileConnectivityRepository()
        use_case = GenerateConnectivityReportUseCase(repository)
        
        # Example with a specific log file
        log_file = "logs/cobertura-nunoa.log"
        logger.info(f"Analyzing log file: {log_file}")
        
        stats = use_case.execute(log_file)
        logger.info("Analysis completed successfully")
        
        # Print some key statistics
        logger.info(f"Analysis duration: {stats['time_range']['duration_minutes']:.2f} minutes")
        logger.info(f"Average RSSI: {stats['signal_quality']['rssi']['mean']:.2f} dBm")
        logger.info(f"Average RSRP: {stats['signal_quality']['rsrp']['mean']:.2f} dBm")
        
    except Exception as e:
        logger.error(f"Error in example analysis: {str(e)}")
        raise

def main():
    """Main entry point for development and testing."""
    try:
        # Setup environment
        setup_environment()
        
        # Run example usage
        example_usage()
        
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 