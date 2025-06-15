import re
import os
from datetime import datetime
from typing import List, Tuple
from connectivity_analyzer.domain.models import ConnectivityData
from connectivity_analyzer.domain.repositories import ConnectivityRepository

class LogFileConnectivityRepository(ConnectivityRepository):
    def _convert_cell_id(self, hex_cell_id: str) -> Tuple[int, int]:
        """
        Convert hexadecimal cell ID to eNodeB ID and Cell ID.
        
        Args:
            hex_cell_id: Hexadecimal cell ID string (e.g., '02D2E0C')
            
        Returns:
            Tuple containing (eNodeB ID, Cell ID) in decimal format
        """
        try:
            # Remove any whitespace and convert to uppercase
            hex_cell_id = hex_cell_id.strip().upper()
            
            # Convert to binary string, removing '0b' prefix
            binary = bin(int(hex_cell_id, 16))[2:].zfill(28)  # 28 bits total (20 + 8)
            
            # Split into eNodeB ID (20 bits) and Cell ID (8 bits)
            enodeb_binary = binary[:20]
            cell_binary = binary[20:]
            
            # Convert back to decimal
            enodeb_id = int(enodeb_binary, 2)
            cell_id = int(cell_binary, 2)
            
            return enodeb_id, cell_id
            
        except ValueError as e:
            raise ValueError(f"Invalid cell ID format: {hex_cell_id}. Error: {str(e)}")

    def _convert_hex_to_decimal(self, hex_value: str) -> int:
        """
        Convert hexadecimal value to decimal.
        
        Args:
            hex_value: Hexadecimal string (e.g., 'FFFE')
            
        Returns:
            Decimal integer value
        """
        try:
            # Remove any whitespace and convert to uppercase
            hex_value = hex_value.strip().upper()
            return int(hex_value, 16)
        except ValueError as e:
            raise ValueError(f"Invalid hexadecimal value: {hex_value}. Error: {str(e)}")

    def get_connectivity_data(self, log_file_path: str) -> List[ConnectivityData]:
        # Check if file exists
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"Log file not found: {log_file_path}")
            
        # Check if file is empty
        if os.path.getsize(log_file_path) == 0:
            raise ValueError(f"Log file is empty: {log_file_path}")
            
        connectivity_data = []
        
        with open(log_file_path, 'r') as file:
            current_timestamp = None
            
            for line in file:
                # Extract timestamp
                timestamp_match = re.search(r'\[(.*?)\]', line)
                if timestamp_match:
                    current_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S.%f')
                
                # Extract RFSTS data
                if '#RFSTS:' in line:
                    try:
                        # Parse the RFSTS line
                        data = line.split('#RFSTS:')[1].strip().strip('"').split(',')
                        
                        # Clean and parse the data according to AT#RFSTS format:
                        # 0      , 1      , 2    , 3    , 4    , 5   , 6   , 7       , 8   , 9  , 10  , 11    , 12              , 13           , 14 , 15   , 16    , 17    , 18
                        # <PLMN> ,<EARFCN>,<RSRP>,<RSSI>,<RSRQ>,<TAC>,<RAC>,[<TXPWR>],<DRX>,<MM>,<RRC>,<CID>  ,<IMSI>           ,[<NetNameAsc>],<SD>,<ABND>,<T3402>,<T3412>,<SINR>
                        #"730 01",1056    ,-69   ,-59   ,-10.0 ,814f ,88   ,20       ,256  ,3   ,1    ,036B227,"730013013527045","ENTEL PCS"   ,2   ,2     ,720    ,3240   ,192
                        plmn = data[0].strip('"')  # MCC-MNC format
                        earfcn = int(data[1])
                        rsrp = int(data[2])
                        rssi = int(data[3])
                        rsrq = float(data[4])
                        
                        # Convert TAC and RAC from hex to decimal
                        tac = str(data[5].strip('"'))
                        rac = str(data[6].strip('"'))
                        
                        # Optional tx_power (only in traffic)
                        tx_power = int(data[7]) if len(data) > 7 and data[7].strip() else None
                        
                        drx = int(data[8])
                        mm_state = int(data[9])
                        rrc_state = int(data[10])
                        
                        # Convert cell ID from hex to decimal format
                        hex_cell_id = data[11].strip('"')
                        enodeb_id, cell_id = self._convert_cell_id(hex_cell_id)
                        
                        imsi = data[12].strip('"')
                        operator_name = data[13].strip('"')
                        service_domain = data[14].strip('"')
                        active_band = int(data[15])
                        t3402 = int(data[16])
                        t3412 = int(data[17])
                        sinr = float(data[18]) * 0.25  # Convertir el valor raw a dB según documentación Telit
                        
                        connectivity_data.append(ConnectivityData(
                            timestamp=current_timestamp,
                            plmn=plmn,
                            earfcn=earfcn,
                            rsrp=rsrp,
                            rssi=rssi,
                            rsrq=rsrq,
                            tac=tac,
                            rac=rac,
                            drx=drx,
                            mm_state=mm_state,
                            rrc_state=rrc_state,
                            cell_id=f"{enodeb_id}-{cell_id}",  # Format as "eNodeB-Cell"
                            imsi=imsi,
                            operator_name=operator_name,
                            service_domain=service_domain,
                            active_band=active_band,
                            t3402=t3402,
                            t3412=t3412,
                            sinr=sinr,
                            tx_power=tx_power
                        ))
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line: {line}")
                        print(f"Error details: {str(e)}")
                        continue
        
        if not connectivity_data:
            raise ValueError(f"No valid RFSTS data found in log file: {log_file_path}")
            
        return connectivity_data 