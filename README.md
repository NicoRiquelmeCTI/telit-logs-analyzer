# Connectivity Log Analyzer

A Python application for analyzing LTE connectivity logs from Telit modems. The application processes log files containing AT#RFSTS command outputs and generates detailed connectivity reports.

## Project Structure

```
connectivity-analyzer/
├── src/
│   └── connectivity_analyzer/
│       ├── domain/
│       │   └── models.py
│       ├── application/
│       │   └── use_cases.py
│       └── infrastructure/
│           └── repositories.py
├── scripts/
│   └── analyze_log.py
├── logs/
│   ├── cobertura-nunoa.log
│   └── ...
├── reports/
│   ├── connectivity_report_*.txt
│   └── connectivity_stats_*.json
├── docs/
│   ├── telit-RFSTS.md
│   └── Conversion-cell-id.md
├── main.py
├── pyproject.toml
└── README.md
```

## Features

- Analyzes LTE connectivity logs from Telit modems
- Processes AT#RFSTS command outputs
- Generates detailed connectivity reports including:
  - Time range analysis
  - Network information (PLMN, Cell ID, Band, etc.)
  - Connection state
  - Signal quality metrics (RSSI, RSRP, RSRQ, SINR)
  - Timer information
- Supports multiple log file formats
- Generates both text and JSON reports

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd connectivity-analyzer
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate virtual env (opcional si usas poetry run)
```bash
source $(poetry env info --path)/bin/activate
```

## Usage

### Development/Testing

For development and testing purposes, use the main entry point:

```bash
poetry run uvicorn src.connectivity_analyzer.interfaces.web.app:app --reload --port 8000
```

This will:
- Set up the development environment
- Create necessary directories
- Run an example analysis
- Generate detailed logs

### Production Use

For production use, use the analyze_log script:

```bash
# Basic usage
poetry run python scripts/analyze_log.py logs/your-log-file.log

# Specify output directory
poetry run python scripts/analyze_log.py logs/your-log-file.log -o custom_reports

# Only display in console without saving
poetry run python scripts/analyze_log.py logs/your-log-file.log --no-save
```

## Command Line Arguments

The `analyze_log.py` script supports the following arguments:

- `log_file`: Path to the log file to analyze (required)
- `--output-dir`, `-o`: Directory to save reports (default: 'reports')
- `--no-save`: Only display report in console without saving files

## Report Format

The generated reports include:

1. Time Range
   - Start time
   - End time
   - Duration

2. Network Information
   - PLMN
   - Cell ID
   - Active Band
   - EARFCN
   - TAC
   - RAC
   - IMSI

3. Connection State
   - MM State
   - RRC State
   - Operator Name
   - Service Domain
   - DRX

4. Signal Quality Metrics
   - RSSI (dBm)
   - RSRP (dBm)
   - RSRQ (dB)
   - SINR (ratio)

5. Timer Information
   - T3402
   - T3412

## Architecture

The project follows Clean Architecture and Hexagonal Architecture principles:

- **Domain Layer**: Core business logic and models
- **Application Layer**: Use cases and business rules
- **Infrastructure Layer**: External interfaces and implementations

## Error Handling

The application includes comprehensive error handling:

- File not found errors
- Invalid data format errors
- Parsing errors
- General error handling with descriptive messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here] 