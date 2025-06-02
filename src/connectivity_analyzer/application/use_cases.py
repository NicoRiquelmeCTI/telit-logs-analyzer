import pandas as pd
import numpy as np
from typing import Dict, Any
from connectivity_analyzer.domain.repositories import ConnectivityRepository
from connectivity_analyzer.domain.models import ConnectivityData
from pathlib import Path

class GenerateConnectivityReportUseCase:
    def __init__(self, repository: ConnectivityRepository):
        self.repository = repository

    def _convert_timestamp_to_iso(self, timestamp) -> str:
        """Convert timestamp to ISO format string."""
        if pd.isna(timestamp):
            return None
        return timestamp.isoformat()

    def _extract_location_from_first_line(self, log_file_path: str) -> Dict[str, str]:
        """Extract location information from the first line of the log file."""
        try:
            with open(log_file_path, 'r') as file:
                first_line = file.readline().strip()
                # Buscar patrones como "Módulo: X, Piso: Y" o similares
                if 'Módulo:' in first_line and 'Piso:' in first_line:
                    module = first_line.split('Módulo:')[1].split(',')[0].strip()
                    floor = first_line.split('Piso:')[1].strip()
                    return {
                        'module': module,
                        'floor': floor
                    }
        except Exception:
            pass
        return None

    def execute(self, log_file_path: str) -> Dict[str, Any]:
        try:
            # Get connectivity data
            connectivity_data = self.repository.get_connectivity_data(log_file_path)
            
            # Extract location information from first line
            location = self._extract_location_from_first_line(log_file_path)
            
            # Convert to DataFrame
            df = pd.DataFrame([vars(data) for data in connectivity_data])
            
            # Check if DataFrame is empty
            if df.empty:
                raise ValueError("No connectivity data found in the log file")
            
            # Calculate statistics
            stats = {
                'signal_quality': {
                    'rssi': {
                        'mean': float(df['rssi'].mean()),
                        'std': float(df['rssi'].std()),
                        'min': float(df['rssi'].min()),
                        'max': float(df['rssi'].max()),
                        'median': float(df['rssi'].median())
                    },
                    'rsrp': {
                        'mean': float(df['rsrp'].mean()),
                        'std': float(df['rsrp'].std()),
                        'min': float(df['rsrp'].min()),
                        'max': float(df['rsrp'].max()),
                        'median': float(df['rsrp'].median())
                    },
                    'rsrq': {
                        'mean': float(df['rsrq'].mean()),
                        'std': float(df['rsrq'].std()),
                        'min': float(df['rsrq'].min()),
                        'max': float(df['rsrq'].max()),
                        'median': float(df['rsrq'].median())
                    },
                    'sinr': {
                        'mean': float(df['sinr'].mean()),
                        'std': float(df['sinr'].std()),
                        'min': float(df['sinr'].min()),
                        'max': float(df['sinr'].max()),
                        'median': float(df['sinr'].median())
                    }
                },
                'network_info': {
                    'plmn': str(df['plmn'].iloc[0]),
                    'cell_id': str(df['cell_id'].iloc[0]),
                    'active_band': int(df['active_band'].iloc[0]),
                    'earfcn': int(df['earfcn'].iloc[0]),
                    'tac': str(df['tac'].iloc[0]),
                    'rac': str(df['rac'].iloc[0]),
                    'imsi': str(df['imsi'].iloc[0]),
                    'operator_name': str(df['operator_name'].iloc[0])
                },
                'connection_state': {
                    'mm_state': int(df['mm_state'].iloc[0]),
                    'rrc_state': int(df['rrc_state'].iloc[0]),
                    'service_domain': str(df['service_domain'].iloc[0]),
                    'drx': int(df['drx'].iloc[0])
                },
                'timers': {
                    't3402': int(df['t3402'].iloc[0]),
                    't3412': int(df['t3412'].iloc[0])
                },
                'time_range': {
                    'start': self._convert_timestamp_to_iso(df['timestamp'].min()),
                    'end': self._convert_timestamp_to_iso(df['timestamp'].max()),
                    'duration_minutes': float((df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60)
                },
                # Add time series data for plotting
                'time_series': {
                    'timestamps': [self._convert_timestamp_to_iso(ts) for ts in df['timestamp'].tolist()],
                    'rssi': [float(x) for x in df['rssi'].tolist()],
                    'rsrp': [float(x) for x in df['rsrp'].tolist()],
                    'rsrq': [float(x) for x in df['rsrq'].tolist()],
                    'sinr': [float(x) for x in df['sinr'].tolist()]
                },
                # Add state distribution data
                'state_distribution': {
                    'mm_states': {str(k): int(v) for k, v in df['mm_state'].value_counts().to_dict().items()},
                    'rrc_states': {str(k): int(v) for k, v in df['rrc_state'].value_counts().to_dict().items()},
                    'service_domains': {str(k): int(v) for k, v in df['service_domain'].value_counts().to_dict().items()}
                }
            }
            
            # Add location if found
            if location:
                stats['location'] = location
            
            return stats
            
        except Exception as e:
            raise Exception(f"Error generating connectivity report: {str(e)}") 