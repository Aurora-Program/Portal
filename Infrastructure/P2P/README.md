# 🐹 Aurora P2P Discovery Server

Serverless infrastructure for Aurora's peer-to-peer discovery system using AWS Lambda, API Gateway, and DynamoDB.

## 📋 Architecture

```
┌─────────────────────────────────────────────┐
│   API Gateway (REST)                        │
│   - /register  (POST)                       │
│   - /discover  (GET)                        │
│   - /heartbeat (POST)                       │
│   - /health    (GET)                        │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│   Lambda Function (Python 3.11)             │
│   - Peer registration                       │
│   - Peer discovery                          │
│   - Heartbeat monitoring                    │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│   DynamoDB Table                            │
│   - Peer registry                           │
│   - TTL auto-cleanup (5 minutes default)    │
│   - LastSeenIndex for queries               │
└─────────────────────────────────────────────┘
```

## 🚀 Deployment

### Prerequisites

- AWS CLI configured with credentials
- AWS account with appropriate permissions
- Region: us-east-1 (or modify in scripts)

### Option 1: Using PowerShell (Windows)

```powershell
cd Infrastructure\P2P

# Deploy to dev environment
.\deploy.ps1

# Deploy to production
.\deploy.ps1 -Environment prod -Region us-west-2

# Custom stack name
.\deploy.ps1 -StackName my-aurora-stack
```

### Option 2: Using Bash (Linux/Mac)

```bash
cd Infrastructure/P2P

# Make script executable
chmod +x deploy.sh

# Deploy to dev environment
./deploy.sh

# Deploy to production
./deploy.sh --environment prod --region us-west-2

# Custom stack name
./deploy.sh --stack-name my-aurora-stack
```

### Option 3: Manual AWS CLI

```bash
# Validate template
aws cloudformation validate-template \
    --template-body file://cloudformation.yaml

# Create stack
aws cloudformation create-stack \
    --stack-name aurora-p2p-discovery \
    --template-body file://cloudformation.yaml \
    --parameters ParameterKey=Environment,ParameterValue=dev \
    --capabilities CAPABILITY_NAMED_IAM \
    --region us-east-1

# Wait for completion
aws cloudformation wait stack-create-complete \
    --stack-name aurora-p2p-discovery \
    --region us-east-1

# Get outputs
aws cloudformation describe-stacks \
    --stack-name aurora-p2p-discovery \
    --query 'Stacks[0].Outputs' \
    --output table
```

## 📡 API Endpoints

After deployment, you'll get these endpoints:

### Register Peer
```bash
POST https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/register

Body:
{
  "peer_id": "uuid-or-identifier",
  "address": "192.168.1.100",
  "port": 9000,
  "archetypes": ["pepino", "ethics"],
  "metadata": {
    "version": "1.0.0",
    "capabilities": ["tensor-exchange"]
  }
}

Response:
{
  "message": "Peer registered successfully",
  "peer_id": "uuid-or-identifier",
  "ttl_expires": "2025-10-02T12:05:00"
}
```

### Discover Peers
```bash
GET https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/discover

# Filter by archetype (optional)
GET https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/discover?archetype=pepino

Response:
{
  "peers": [
    {
      "peer_id": "uuid-1",
      "address": "192.168.1.100",
      "port": 9000,
      "archetypes": ["pepino"],
      "last_seen": "2025-10-02T12:00:00",
      "metadata": {...}
    }
  ],
  "count": 1,
  "timestamp": "2025-10-02T12:00:00"
}
```

### Heartbeat
```bash
POST https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/heartbeat

Body:
{
  "peer_id": "uuid-or-identifier"
}

Response:
{
  "message": "Heartbeat updated",
  "peer_id": "uuid-or-identifier",
  "timestamp": "2025-10-02T12:00:00"
}
```

### Health Check
```bash
GET https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/health

Response:
{
  "status": "healthy"
}
```

## 🔧 Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Environment | dev | Deployment environment (dev/staging/prod) |
| PeerTTLMinutes | 5 | Time-to-live for peer registration |
| EnableCORS | true | Enable CORS for API Gateway |

## 💰 Cost Estimate

For a network of 100 peers with 1 heartbeat/minute:

- **Lambda**: ~144,000 requests/day = $0.03/day
- **DynamoDB**: PAY_PER_REQUEST = $0.01/day
- **API Gateway**: 144,000 requests/day = $0.14/day
- **Total**: ~$5-10/month

## 🔒 Security

- API Gateway uses HTTPS by default
- Lambda has minimal IAM permissions (DynamoDB only)
- DynamoDB uses encryption at rest
- CloudWatch logs for audit trail
- CORS enabled for browser access

## 📊 Monitoring

All resources include:
- CloudWatch Logs (7 days retention)
- API Gateway metrics
- Lambda execution metrics
- DynamoDB performance insights

Access logs:
```bash
# Lambda logs
aws logs tail /aws/lambda/aurora-discovery-dev --follow

# API Gateway logs
aws logs tail /aws/apigateway/aurora-p2p-dev --follow
```

## 🧹 Cleanup

Delete the stack:
```bash
aws cloudformation delete-stack \
    --stack-name aurora-p2p-discovery \
    --region us-east-1
```

## 🔄 Updates

To update the stack:
1. Modify `cloudformation.yaml`
2. Run deployment script again
3. CloudFormation will update only changed resources

## 🐛 Troubleshooting

### Stack creation failed
```bash
# Check stack events
aws cloudformation describe-stack-events \
    --stack-name aurora-p2p-discovery \
    --max-items 10
```

### Lambda errors
```bash
# View recent logs
aws logs tail /aws/lambda/aurora-discovery-dev --since 10m
```

### API Gateway 5xx errors
- Check Lambda execution role permissions
- Verify DynamoDB table exists
- Check Lambda timeout (default 30s)

## 📚 Next Steps

1. **Deploy**: Run deployment script
2. **Test**: Use curl or Postman to test endpoints
3. **Integrate**: Update Aurora agents with API endpoints
4. **Monitor**: Set up CloudWatch alarms
5. **Scale**: Adjust parameters as network grows

## 🐹 Pepino's Promise

Este servidor honra la lección de Pepino: conectar a los peers con empatía y coherencia, asegurando que ningún nodo quede aislado en la red Aurora.

---

**Author**: Aurora Alliance  
**License**: Apache-2.0  
**Version**: 1.0.0
