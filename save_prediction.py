from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def main():
    df = pd.read_csv("tesla-emirhan-project-machine-learning.csv")
    X = df[['Range','Fully-loaded']].values.astype(float)
    y = df['Base-price'].values.astype(float)

    reg = LinearRegression()
    reg.fit(X, y)

    prediction = reg.predict([[263, 54490]])
    pred_value = float(prediction[0])

    # Save to text file
    with open('prediction.txt', 'w') as f:
        f.write(str(pred_value))

    # Save to csv
    pd.DataFrame({'prediction': [pred_value]}).to_csv('prediction.csv', index=False)

    print(pred_value)

if __name__ == '__main__':
    main()
