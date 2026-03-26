kenya-macro-viz/
├── .streamlit/
│   └── config.toml          # Custom theme colors 
├── data/
│   └── cleaned/             # CSVs 
├── modules/
│   ├── __init__.py
│   ├── data_loader.py       # Centralized pandas loading logic
│   └── charts.py            # Reusable Plotly functions
├── app.py                   # Main entry point (The Dashboard)
├── requirements.txt         # Dependencies (streamlit, pandas, plotly)
└── README.md                # Project documentation