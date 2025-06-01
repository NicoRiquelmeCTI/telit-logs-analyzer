import pandas as pd
import numpy as np
from typing import Dict, Any
from connectivity_analyzer.domain.repositories import ConnectivityRepository
from connectivity_analyzer.domain.models import ConnectivityData

class GenerateConnectivityReportUseCase:
    def __init__(self, repository: ConnectivityRepository):
        self.repository = repository

    def execute(self, log_file_path: str) -> Dict[str, Any]:
        try:
            # Get connectivity data
            connectivity_data = self.repository.get_connectivity_data(log_file_path)
            
            # Convert to DataFrame
            df = pd.DataFrame([vars(data) for data in connectivity_data])
            
            # Check if DataFrame is empty
            if df.empty:
                raise ValueError("No connectivity data found in the log file")
            
            # Calculate statistics
            stats = {
                'signal_quality': {
                    'rssi': {
                        'mean': df['rssi'].mean(),
                        'std': df['rssi'].std(),
                        'min': df['rssi'].min(),
                        'max': df['rssi'].max(),
                        'median': df['rssi'].median()
                    },
                    'rsrp': {
                        'mean': df['rsrp'].mean(),
                        'std': df['rsrp'].std(),
                        'min': df['rsrp'].min(),
                        'max': df['rsrp'].max(),
                        'median': df['rsrp'].median()
                    },
                    'rsrq': {
                        'mean': df['rsrq'].mean(),
                        'std': df['rsrq'].std(),
                        'min': df['rsrq'].min(),
                        'max': df['rsrq'].max(),
                        'median': df['rsrq'].median()
                    },
                    'sinr': {
                        'mean': df['sinr'].mean(),
                        'std': df['sinr'].std(),
                        'min': df['sinr'].min(),
                        'max': df['sinr'].max(),
                        'median': df['sinr'].median()
                    }
                },
                'network_info': {
                    'plmn': df['plmn'].iloc[0],
                    'cell_id': df['cell_id'].iloc[0],
                    'active_band': df['active_band'].iloc[0],
                    'earfcn': df['earfcn'].iloc[0],
                    'tac': df['tac'].iloc[0],
                    'rac': df['rac'].iloc[0],
                    'imsi': df['imsi'].iloc[0],
                    'operator_name': df['operator_name'].iloc[0]
                },
                'connection_state': {
                    'mm_state': df['mm_state'].iloc[0],
                    'rrc_state': df['rrc_state'].iloc[0],
                    'service_domain': df['service_domain'].iloc[0],
                    'drx': df['drx'].iloc[0]
                },
                'timers': {
                    't3402': df['t3402'].iloc[0],
                    't3412': df['t3412'].iloc[0]
                },
                'time_range': {
                    'start': df['timestamp'].min(),
                    'end': df['timestamp'].max(),
                    'duration_minutes': (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60
                }
            }
            
            return stats
            
        except Exception as e:
            raise Exception(f"Error generating connectivity report: {str(e)}") 