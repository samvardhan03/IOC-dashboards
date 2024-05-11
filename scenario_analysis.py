import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['net_zero_dashboard']

def fetch_data_from_sources():
    # Fetch data from MongoDB
    data_cursor = db['data'].find().sort('timestamp', -1).limit(1)
    data = next(data_cursor)['data']
    return data

def preprocess_data(data):
    # Perform data cleaning, transformation, and normalization
    processed_data = {
        # Combine and process data from various sources
    }
    return processed_data

def run_scenario_analysis():
    # Load latest data from MongoDB or fetch from sources
    data = fetch_data_from_sources()
    data_df = pd.DataFrame.from_dict(data, orient='index').transpose()

    # Data preparation
    X = data_df.drop(['target_variable'], axis=1)
    y = data_df['target_variable']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model training
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
    xgb_model.fit(X_train_scaled, y_train)

    # Model evaluation
    y_pred_rf = rf_model.predict(X_test_scaled)
    y_pred_xgb = xgb_model.predict(X_test_scaled)
    mse_rf = mean_squared_error(y_test, y_pred_rf)
    mse_xgb = mean_squared_error(y_test, y_pred_xgb)
    print(f'Random Forest MSE: {mse_rf}')
    print(f'XGBoost MSE: {mse_xgb}')

    # Scenario simulation
    scenario_data = {
        # Provide scenario input data
    }
    scenario_df = pd.DataFrame.from_dict(scenario_data, orient='index').transpose()
    scenario_scaled = scaler.transform(scenario_df)
    scenario_pred_rf = rf_model.predict(scenario_scaled)
    scenario_pred_xgb = xgb_model.predict(scenario_scaled)

    # Results analysis
    results = pd.DataFrame({
        'Input Variables': scenario_df.columns,
        'Input Values': scenario_df.values[0],
        'RF Prediction': scenario_pred_rf,
        'XGBoost Prediction': scenario_pred_xgb
    })

    # Store analysis results in MongoDB
    store_data(results.to_dict('records'), 'scenario_analysis')

def store_data(data, collection_name):
    db[collection_name].insert_one(data)