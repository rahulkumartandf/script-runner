import boto3
import csv

def get_ec2_details(region_name="ap-south-1", output_file="ec2_details.csv"):
    ec2 = boto3.client("ec2", region_name=region_name)

    response = ec2.describe_instances()
    instances_data = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance.get("InstanceId", "")
            instance_type = instance.get("InstanceType", "")
            state = instance.get("State", {}).get("Name", "")
            private_ip = instance.get("PrivateIpAddress", "")
            public_ip = instance.get("PublicIpAddress", "")
            vpc_id = instance.get("VpcId", "")
            subnet_id = instance.get("SubnetId", "")

            # Security groups
            sg_names = [sg["GroupName"] for sg in instance.get("SecurityGroups", [])]
            sg_ids = [sg["GroupId"] for sg in instance.get("SecurityGroups", [])]

            # Tags
            tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])} if "Tags" in instance else {}

            instances_data.append({
                "InstanceId": instance_id,
                "Type": instance_type,
                "State": state,
                "PrivateIP": private_ip,
                "PublicIP": public_ip,
                "VPC": vpc_id,
                "Subnet": subnet_id,
                "SecurityGroups": ",".join(sg_names),
                "SecurityGroupIds": ",".join(sg_ids),
                "Tags": str(tags)
            })

    # Save to CSV
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["InstanceId", "Type", "State", "PrivateIP", "PublicIP",
                      "VPC", "Subnet", "SecurityGroups", "SecurityGroupIds", "Tags"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in instances_data:
            writer.writerow(data)

    print(f"✅ EC2 details saved to {output_file}")


if __name__ == "__main__":
    # Change region if needed
    get_ec2_details(region_name="ap-south-1")
