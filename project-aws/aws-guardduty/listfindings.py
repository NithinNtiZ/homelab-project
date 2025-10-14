import boto3
import sys

def list_all_guardduty_findings(region):
    client = boto3.client('guardduty', region_name=region)

    detectors = client.list_detectors()
    if not detectors.get('DetectorIds'):
        print("No GuardDuty detector found in region:", region)
        return []

    detector_id = detectors['DetectorIds'][0]
    print("Using Detector ID:", detector_id)

    finding_ids = []
    paginator = client.get_paginator('list_findings')
    for page in paginator.paginate(DetectorId=detector_id, MaxResults=50):
        finding_ids.extend(page.get('FindingIds', []))

    print(f"Total finding IDs listed: {len(finding_ids)}")

    all_findings = []
    for i in range(0, len(finding_ids), 50):
        batch_ids = finding_ids[i:i+50]
        resp = client.get_findings(DetectorId=detector_id, FindingIds=batch_ids)
        all_findings.extend(resp.get('Findings', []))

    print(f"Total detailed findings retrieved: {len(all_findings)}")
    return all_findings

if __name__ == "__main__":
    region = 'us-east-1'  # Change as needed
    findings = list_all_guardduty_findings(region)
    for f in findings:
        # print(f)
        if f.get('Severity') >= 5:
            print(f"ID: {f['Id']}, Type: {f['Type']}, Severity: {f['Severity']}, Description: {f['Description']}")
        # sys.exit()
