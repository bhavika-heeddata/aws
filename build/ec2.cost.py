import boto3
from datetime import datetime

client = boto3.client('ce')

year = 2024
month = 10  
start_date = datetime(year, month, 1).strftime('%Y-%m-%d')  
end_date = datetime(year, month + 1, 1).strftime('%Y-%m-%d')  

ec2_response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost', 'UsageQuantity'],
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': ['Amazon Elastic Compute Cloud - Compute']
        }
    }
)

tax_response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    Filter={
        'Dimensions': {
            'Key': 'SERVICE',
            'Values': ['Tax']
        }
    }
)

print("API Responses:")
print("EC2 Response:", ec2_response)
print("Tax Response:", tax_response)

if 'ResultsByTime' in ec2_response and ec2_response['ResultsByTime']:
    for result in ec2_response['ResultsByTime']:
        date = result['TimePeriod']['Start']
        ec2_cost = float(result['Total']['UnblendedCost']['Amount'])
        usage = float(result['Total']['UsageQuantity']['Amount'])

        tax_cost = 0.0
        if 'ResultsByTime' in tax_response and tax_response['ResultsByTime']:
            tax_cost = float(tax_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
        
        total_cost_with_tax = ec2_cost + tax_cost

        print(f"Month: {date}")
        print(f"Total EC2 Cost: ${ec2_cost}")
        print(f"Total Tax Cost: ${tax_cost}")
        print(f"Total Usage Quantity: {usage}")
        print(f"Total Cost with Tax: ${total_cost_with_tax}")
        print("-" * 30)

