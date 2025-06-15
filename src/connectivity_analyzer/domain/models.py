from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ConnectivityData:
    """
    Data model representing LTE network connectivity information from AT#RFSTS command.
    
    Attributes:
        timestamp: When the measurement was taken
        plmn: Public Land Mobile Network (MCC-MNC format)
        earfcn: E-UTRA Absolute Radio Frequency Channel Number
        rsrp: Reference Signal Received Power (dBm)
        rssi: Received Signal Strength Indication (dBm)
        rsrq: Reference Signal Received Quality (dB)
        tac: Tracking Area Code
        rac: Routing Area Code
        drx: Discontinuous Reception Cycle Length (ms)
        mm_state: Mobility Management State
            (0: NULL, 1: DEREGISTERED, 2: REGISTRATION INITIATED,
             3: REGISTERED, 4: TRACKING AREA UPDATE INITIATED,
             5: SERVICE REQUEST INITIATED, 6: DEREGISTRATION INITIATED)
        rrc_state: Radio Resource Control State
        cell_id: Cell ID in format "eNodeB-Cell" (e.g., "11566-12")
        imsi: International Mobile Station Identity
        operator_name: Service operator name
        service_domain: Service Domain
            (0: No Service, 1: CS only, 2: PS only, 3: CS+PS)
        active_band: Active Band (1-63 according to 3GPP TS 36.101)
        t3402: Timer T3402 in seconds
        t3412: Timer T3412 in seconds
        sinr: Signal-to-Interference plus Noise Ratio (dB)
        tx_power: Optional[Transmit Power (dBm), only available in traffic]
    """
    timestamp: datetime
    plmn: str  # MCC-MNC format
    earfcn: int
    rsrp: int
    rssi: int
    rsrq: float
    tac: str
    rac: str
    drx: int
    mm_state: int
    rrc_state: int
    cell_id: str
    imsi: str
    operator_name: str
    service_domain: str
    active_band: int
    t3402: int
    t3412: int
    sinr: float
    tx_power: Optional[int] = None 