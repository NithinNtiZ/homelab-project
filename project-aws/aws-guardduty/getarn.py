import boto3

# Create clients
ec2_client = boto3.client('ec2')
sts_client = boto3.client('sts')

# Get AWS account ID
account_id = sts_client.get_caller_identity()["Account"]

# Get all available AWS regions for EC2
regions = [r['RegionName'] for r in ec2_client.describe_regions(AllRegions=True)['Regions']]

instance_arns = []

for region in regions:
    print(f"Scanning region: {region}")
    regional_ec2 = boto3.client('ec2', region_name=region)

    try:
        response = regional_ec2.describe_instances()
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]
                arn = f"arn:aws:ec2:{region}:{account_id}:instance/{instance_id}"
                instance_arns.append(arn)
    except Exception as e:
        print(f"Error in region {region}: {e}")

# Print results
print("\nFound EC2 instance ARNs:")
for arn in instance_arns:
    print(arn)
