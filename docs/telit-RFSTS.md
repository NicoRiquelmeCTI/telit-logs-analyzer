LTE network
#RFSTS:<PLMN>,<EARFCN>,<RSRP>,<RSSI>,<RSRQ>,<TAC>,<RAC>,[<TXPWR>],< DRX>, <MM>,<RRC>,<CID>,<IMSI>,[<NetNameAsc>],<SD>,<ABND>,<T3402>,<T3412>,<SI NR>

Parameters Description

<PLMN>: Country code and operator code(MCC, MNC) E-UTRA Assigned Radio Channel
<RSRP>: Reference Signal Received Power
<RSSI>: Received Signal Strength Indication Reference Signal Received Quality
<TAC>: Tracking Area Code
<RAC>: Routing Area Code
<TXPWR>: Tx Power (In traffic only)
<DRX>: Discontinuous reception cycle Length (cycle length in ms)

Mobility Management state (for debug purpose only) 

<MM> =0: NULL
<MM> =1: DEREGISTERED
<MM> =2: REGISTRATION INITIATED
<MM> =3: REGISTERED
<MM> =4: TRACKING AREA UPDATE INITIATED
<MM> =5: SERVICE REQUEST INITIATED
<MM> =6: DEREGISTRATION INITIATED


<RRC> Radio Resource state (for debug purpose only; see above) 
<CID> Cell ID
    
<IMSI> International Mobile Station ID <SD> -
<SD> =0: No Service
<SD> =1: CS only
<SD> =2: PS only
<SD> =3: CS+PS

<ABND> Active Band
<ABND>=1..63: According to 3GPP TS 36.101

<T3402> Timer T3402 in seconds 
<T3412> Timer T3412 in seconds
<SINR> Signal-to-Interface plus Noise Ratio
