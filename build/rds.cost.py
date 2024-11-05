import boto3
from datetime import datetime, timedelta

client = boto3.client('ce')

query_date = datetime(2024, 10, 6)  
start_date = query_date.strftime('%Y-%m-%d')  # Start of the specific date
end_date = (query_date + timedelta(days=1)).strftime('%Y-%m-%d')  

# Define your tax rate (e.g., 10% as 0.10)
tax_rate = 0.10

response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='DAILY',  
    Metrics=['UnblendedCost', 'UsageQuantity'],
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': ['Amazon Relational Database Service']
        }
    }
)

print("API Response:", response)

if 'ResultsByTime' in response and response['ResultsByTime']:
    for result in response['ResultsByTime']:
        date = result['TimePeriod']['Start']
        cost = float(result['Total']['UnblendedCost']['Amount'])
        usage = float(result['Total']['UsageQuantity']['Amount'])
        
        tax = cost * tax_rate
        total_cost_with_tax = cost + tax

        print(f"Date: {date}")
        print(f"Total Cost: ${cost}")
        print(f"Total Usage Quantity: {usage}")
        print(f"Calculated Tax: ${tax}")
        print(f"Total Cost with Tax: ${total_cost_with_tax}")
        print("-" * 30)
