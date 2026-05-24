import pandas as pd
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
except ImportError:
    pass

def tool(func):
    func._is_tool = True
    return func

@tool
def train_linear_model(x_col, y_col):
    """Fit a basic linear regression model to clean_data.csv."""
    try:
        df = pd.read_csv('clean_data.csv')
        df = df.dropna(subset=[x_col, y_col])
        X = df[[x_col]]
        y = df[y_col]
        
        model = LinearRegression()
        model.fit(X, y)
        preds = model.predict(X)
        score = r2_score(y, preds)
        
        return f"Model trained. Coefficient: {model.coef_[0]:.4f}, Intercept: {model.intercept_:.4f}, R2 Score: {score:.4f}"
    except Exception as e:
        return f"Error training model: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        print(train_linear_model(sys.argv[1], sys.argv[2]))
