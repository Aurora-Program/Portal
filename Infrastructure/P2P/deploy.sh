#!/bin/bash
# Aurora P2P Discovery Server - CloudFormation Deployment Script

set -e

# Configuration
STACK_NAME="aurora-p2p-discovery"
TEMPLATE_FILE="cloudformation.yaml"
REGION="us-east-1"
ENVIRONMENT="dev"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐹 Aurora P2P Discovery Server Deployment${NC}"
echo "============================================="

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --environment|-e)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --region|-r)
            REGION="$2"
            shift 2
            ;;
        --stack-name|-s)
            STACK_NAME="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Stack Name: $STACK_NAME"
echo ""

# Validate template
echo -e "${YELLOW}Validating CloudFormation template...${NC}"
aws cloudformation validate-template \
    --template-body file://$TEMPLATE_FILE \
    --region $REGION

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Template validation passed${NC}"
else
    echo -e "${RED}✗ Template validation failed${NC}"
    exit 1
fi

# Check if stack exists
STACK_EXISTS=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION 2>&1 | grep -c "does not exist" || true)

if [ "$STACK_EXISTS" -eq 0 ]; then
    echo -e "${YELLOW}Stack exists. Updating...${NC}"
    ACTION="update-stack"
else
    echo -e "${YELLOW}Stack does not exist. Creating...${NC}"
    ACTION="create-stack"
fi

# Deploy stack
echo -e "${YELLOW}Deploying CloudFormation stack...${NC}"
aws cloudformation $ACTION \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE_FILE \
    --parameters \
        ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION \
    --tags \
        Key=Project,Value=Aurora \
        Key=ManagedBy,Value=CloudFormation

if [ "$ACTION" == "create-stack" ]; then
    echo -e "${YELLOW}Waiting for stack creation to complete...${NC}"
    aws cloudformation wait stack-create-complete \
        --stack-name $STACK_NAME \
        --region $REGION
else
    echo -e "${YELLOW}Waiting for stack update to complete...${NC}"
    aws cloudformation wait stack-update-complete \
        --stack-name $STACK_NAME \
        --region $REGION 2>/dev/null || true
fi

# Get outputs
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""
echo -e "${GREEN}Stack Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

# Save outputs to file
OUTPUT_FILE="outputs-${ENVIRONMENT}.json"
aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs' \
    --output json > $OUTPUT_FILE

echo ""
echo -e "${GREEN}Outputs saved to: $OUTPUT_FILE${NC}"
echo ""
echo -e "${GREEN}🎉 Aurora P2P Discovery Server is ready!${NC}"
