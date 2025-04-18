terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "5.35.0"
    }
  }
}


provider "aws" {
  # Configuration options
  region = var.region
}


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  owners = ["099720109477"] # Canonical

}

#Create KeyPair
resource "aws_key_pair" "terraform-demo" {
  key_name   = var.keypair
  public_key = file("D:\\PRODUCTION\\AWS\\k8_test_env_infra\\module-1\\labadmin-keypair-test-uswest-01.pem.pub")
}


resource "aws_eip" "eip" {
  count = var.vm_count
  instance = aws_instance.ec2[count.index].id

}


#Create Instances

resource "aws_instance" "ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.terraform-demo.key_name
  subnet_id = aws_subnet.subnet.id
  count = var.vm_count
  root_block_device {
    volume_size = 64
  }
  user_data = file("D:\\PRODUCTION\\AWS\\k8_test_env_infra\\module-1\\script.sh")

  tags = {
    Name = "${var.name_vm}-${count.index+1}"
  }
}
