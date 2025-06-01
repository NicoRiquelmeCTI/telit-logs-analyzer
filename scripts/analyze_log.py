#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from connectivity_analyzer.infrastructure.repositories import LogFileConnectivityRepository
from connectivity_analyzer.application.use_cases import GenerateConnectivityReportUseCase

def format_report(stats: dict) -> str:
    """Format the statistics into a readable report."""
    report = []
    report.append("=== CONNECTIVITY REPORT ===")
    report.append(f"\nTime Range:")
    report.append(f"Start: {stats['time_range']['start']}")
    report.append(f"End: {stats['time_range']['end']}")
    report.append(f"Duration: {stats['time_range']['duration_minutes']:.2f} minutes")
    
    report.append(f"\nNetwork Information:")
    report.append(f"PLMN: {stats['network_info']['plmn']}")
    report.append(f"Cell ID: {stats['network_info']['cell_id']}")
    report.append(f"Active Band: {stats['network_info']['active_band']}")
    report.append(f"EARFCN: {stats['network_info']['earfcn']}")
    report.append(f"TAC: {stats['network_info']['tac']}")
    report.append(f"RAC: {stats['network_info']['rac']}")
    report.append(f"IMSI: {stats['network_info']['imsi']}")
    
    report.append(f"\nConnection State:")
    report.append(f"MM State: {stats['connection_state']['mm_state']}")
    report.append(f"RRC State: {stats['connection_state']['rrc_state']}")
    report.append(f"Operator Name: {stats['network_info']['operator_name']}")
    report.append(f"Service Domain: {stats['connection_state']['service_domain']}")
    report.append(f"DRX: {stats['connection_state']['drx']} ms")
    
    report.append(f"\nTimers:")
    report.append(f"T3402: {stats['timers']['t3402']} seconds")
    report.append(f"T3412: {stats['timers']['t3412']} seconds")
    
    report.append(f"\nSignal Strength (RSSI) Statistics:")
    report.append(f"Mean: {stats['signal_quality']['rssi']['mean']:.2f} dBm")
    report.append(f"Std Dev: {stats['signal_quality']['rssi']['std']:.2f} dBm")
    report.append(f"Min: {stats['signal_quality']['rssi']['min']} dBm")
    report.append(f"Max: {stats['signal_quality']['rssi']['max']} dBm")
    report.append(f"Median: {stats['signal_quality']['rssi']['median']} dBm")
    report.append("\nRSSI Reference Ranges:")
    report.append("Excelente: > -65 dBm")
    report.append("Bueno: -65 a -75 dBm")
    report.append("Regular: -75 a -85 dBm")
    report.append("Pobre: < -85 dBm")
    
    report.append(f"\nRSRP Statistics:")
    report.append(f"Mean: {stats['signal_quality']['rsrp']['mean']:.2f} dBm")
    report.append(f"Std Dev: {stats['signal_quality']['rsrp']['std']:.2f} dBm")
    report.append(f"Min: {stats['signal_quality']['rsrp']['min']} dBm")
    report.append(f"Max: {stats['signal_quality']['rsrp']['max']} dBm")
    report.append(f"Median: {stats['signal_quality']['rsrp']['median']} dBm")
    report.append("\nRSRP Reference Ranges:")
    report.append("Excelente: > -80 dBm")
    report.append("Bueno: -80 a -90 dBm")
    report.append("Regular: -90 a -100 dBm")
    report.append("Pobre: < -100 dBm")
    
    report.append(f"\nRSRQ Statistics:")
    report.append(f"Mean: {stats['signal_quality']['rsrq']['mean']:.2f} dB")
    report.append(f"Std Dev: {stats['signal_quality']['rsrq']['std']:.2f} dB")
    report.append(f"Min: {stats['signal_quality']['rsrq']['min']} dB")
    report.append(f"Max: {stats['signal_quality']['rsrq']['max']} dB")
    report.append(f"Median: {stats['signal_quality']['rsrq']['median']} dB")
    report.append("\nRSRQ Reference Ranges:")
    report.append("Excelente: > -10 dB")
    report.append("Bueno: -10 a -15 dB")
    report.append("Regular: -15 a -20 dB")
    report.append("Pobre: < -20 dB")
    
    report.append(f"\nSINR Statistics:")
    report.append(f"Mean: {stats['signal_quality']['sinr']['mean']:.2f} dB")
    report.append(f"Std Dev: {stats['signal_quality']['sinr']['std']:.2f} dB")
    report.append(f"Min: {stats['signal_quality']['sinr']['min']:.2f} dB")
    report.append(f"Max: {stats['signal_quality']['sinr']['max']:.2f} dB")
    report.append(f"Median: {stats['signal_quality']['sinr']['median']:.2f} dB")
    report.append("\nSINR Reference Ranges:")
    report.append("Excelente: > 13 dB")
    report.append("Bueno: 10 a 13 dB")
    report.append("Regular: 0 a 10 dB")
    report.append("Pobre: < 0 dB")
    
    return "\n".join(report)

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Analyze LTE connectivity log files.')
    parser.add_argument('log_file', help='Path to the log file to analyze')
    parser.add_argument('--output-dir', '-o', default='reports',
                      help='Directory to save the reports (default: reports)')
    parser.add_argument('--no-save', action='store_true',
                      help='Do not save reports to files, only print to console')
    
    args = parser.parse_args()
    
    try:
        # Crear directorio de salida si no existe
        if not args.no_save:
            os.makedirs(args.output_dir, exist_ok=True)
        
        # Initialize components
        repository = LogFileConnectivityRepository()
        use_case = GenerateConnectivityReportUseCase(repository)
        
        # Process the log file
        stats = use_case.execute(args.log_file)
        
        # Generate and print the report
        report = format_report(stats)
        print(report)
        
        if not args.no_save:
            # Generate timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_name = Path(args.log_file).stem
            
            # Save the report to a file
            report_path = os.path.join(args.output_dir, f"connectivity_report_{log_name}_{timestamp}.txt")
            with open(report_path, "w") as f:
                f.write(report)
            
            # Save raw statistics to JSON
            stats_path = os.path.join(args.output_dir, f"connectivity_stats_{log_name}_{timestamp}.json")
            with open(stats_path, "w") as f:
                json.dump(stats, f, indent=2, default=str)
            
            print(f"\nReports saved to:")
            print(f"- Text report: {report_path}")
            print(f"- JSON stats: {stats_path}")
            
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please make sure the log file exists in the correct location.")
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Please check that the log file contains valid RFSTS data.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("An unexpected error occurred. Please check the log file format and try again.")

if __name__ == "__main__":
    main() 