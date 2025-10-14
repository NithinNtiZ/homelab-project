import boto3

# Create EC2 client to get regions
ec2_client = boto3.client("ec2")
regions = [r["RegionName"] for r in ec2_client.describe_regions(AllRegions=True)["Regions"]]

for region in regions:
    print(f"Enabling GuardDuty in region: {region}")
    gd_client = boto3.client("guardduty", region_name=region)

    try:
        # Check if GuardDuty is already enabled
        detectors = gd_client.list_detectors()["DetectorIds"]
        if not detectors:
            response = gd_client.create_detector(Enable=True)
            print(f"✅ GuardDuty enabled in {region} - Detector ID: {response['DetectorId']}")
        else:
            detector_id = detectors[0]
            gd_client.update_detector(DetectorId=detector_id, Enable=True)
            print(f"🔄 GuardDuty already enabled in {region} - Detector ID: {detector_id}")
    except Exception as e:
        print(f"❌ Failed in {region}: {e}")
