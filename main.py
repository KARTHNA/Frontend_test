from flask import Flask, request, jsonify
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io

app = Flask(__name__)

def foo(request_id, query):
    # Replace with your actual data retrieval and preparation logic
    # This example creates dummy data
    data = {
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [23, 45, 56, 28]
    }
    df = pd.DataFrame(data)

    # Generate all plots
    plots = {}
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Category', y='Values', data=df)
    img_bar = io.BytesIO()
    plt.savefig(img_bar, format='png')
    img_bar.seek(0)
    plots['bar'] = base64.b64encode(img_bar.getvalue()).decode()
    plt.close()  # Close the figure to avoid memory issues

    plt.figure(figsize=(10, 6))
    plt.plot(df['Category'], df['Values'])
    img_line = io.BytesIO()
    plt.savefig(img_line, format='png')
    img_line.seek(0)
    plots['line'] = base64.b64encode(img_line.getvalue()).decode()
    plt.close()  # Close the figure to avoid memory issues

    # Example pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(df['Values'], labels=df['Category'], autopct="%1.1f%%")
    img_pie = io.BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    plots['pie'] = base64.b64encode(img_pie.getvalue()).decode()
    plt.close()  # Close the figure to avoid memory issues

    # Set a flag value (adjust as needed)
    flag = 0
    remarks = "Here are some visualizations of your data."

    # Table data
    table_data = df.to_dict(orient='records')
    print("Backend table data:", table_data)  # Debugging line

    # Return results as a tuple
    return flag, request_id, plots, remarks, table_data

@app.route('/process_request', methods=['POST'])
def process_request():
    try:
        req_data = request.get_json()
        query = req_data.get('user_query')
        request_id = req_data.get('request_id')

        flag, request_id, plots, remarks, table_data = foo(request_id, query)

        response = {
            'flag': flag,
            'request_id': request_id,
            'plots': plots,
            'remarks': remarks,
            'table_data': table_data
        }
        return jsonify(response)

    except Exception as e:
        # Handle errors gracefully
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=8888, debug=True)
