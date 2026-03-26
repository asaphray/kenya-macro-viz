kenya-macro-viz/
├── .streamlit/
│   └── config.toml          # Custom theme colors (Marketing flair!)
├── data/
│   └── cleaned/             # Keep your CSVs here
├── modules/
│   ├── __init__.py
│   ├── data_loader.py       # Centralized pandas loading logic
│   └── charts.py            # Reusable Plotly functions
├── app.py                   # Main entry point (The Dashboard)
├── requirements.txt         # Dependencies (streamlit, pandas, plotly)
└── README.md                # Project documentation