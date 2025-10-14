# Create a VPC
resource "aws_vpc" "vpc" {
  cidr_block = var.cidr_block
  tags = {
    Name = var.name_vpc
  }
}
# create subnet

resource "aws_subnet" "subnet" {
  vpc_id               = aws_vpc.vpc.id
  cidr_block           = var.cidr_block_sbnt
  availability_zone   = var.availability_zone


  tags = {
    Name = var.name_subnet
  }
}

#create internet gateway for vpc
resource "aws_internet_gateway" "gatewat" {
  vpc_id = aws_vpc.vpc.id
    tags = {
    Name = var.name_ig
  }

}

#create route
resource "aws_route_table" "RT" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gatewat.id
  }
  tags = {
    Name = var.name_rt
  }
}

#routetable associate

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.RT.id
}


#Network access Control List

resource "aws_network_acl" "nacl" {
  vpc_id = aws_vpc.vpc.id

  egress {
    protocol   = "tcp"
    rule_no    = 200
    action     = "allow"
    cidr_block = var.cidr_block_0
    from_port  = 0
    to_port    = 65535
  }

  # ingress {
  #   protocol   = "tcp"
  #   rule_no    = 103
  #   action     = "allow"
  #   cidr_block = var.cidr_block_0
  #   from_port  = 22
  #   to_port    = 22
  # }
  ingress {
    protocol   = "tcp"
    rule_no    = 104
    action     = "allow"
    cidr_block = var.cidr_block_0
    from_port  = 0
    to_port    = 65535
  }
  tags = {
    Name = var.name_nacl
  }
}

resource "aws_network_acl_association" "main" {
  network_acl_id = aws_network_acl.nacl.id
  subnet_id      = aws_subnet.subnet.id
}   


##CREATE A SECURITY GROUP

resource "aws_default_security_group" "sg" {
  # name        = var.name_sg
  # description = "Allow inbound traffic"
  vpc_id      = aws_vpc.vpc.id

  #INGRESS'=

  ingress {
    description = "HTTPS"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #EGRESS

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = var.name_sg
  }
}
