import json

from google.cloud import aiplatform
from google.cloud import storage

import podsearch.utils

DistanceMeasureType = aiplatform.matching_engine.matching_engine_index_config.DistanceMeasureType

sentence = 'this is a test'

embeddings = [{
    'id': 'test-id',
    'embedding': podsearch.utils.encode(sentence).squeeze().tolist()
}]

project = 'podsearch-367715'
location = 'us-central1'

storage_client = storage.Client(project=project)
bucket = storage_client.bucket(f'{project}-matching_engine')
if not bucket.exists():
    storage_client.create_bucket(bucket, project=project, location=location)
blob = bucket.blob('embeddings.json')
blob.upload_from_string('\n'.join(map(json.dumps, embeddings)))

if False:
    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name='test_index',
        contents_delta_uri=f'gs://{project}-matching_engine',
        dimensions=len(embeddings[0]['embedding']),
        approximate_neighbors_count=128,
        distance_measure_type=DistanceMeasureType.COSINE_DISTANCE.value,
        project=project,
        location=location,
        #     leaf_node_embedding_count: Optional[int] = None,
        #     leaf_nodes_to_search_percent: Optional[float] = None,
        #     description: Optional[str] = None,
        #     labels: Optional[Dict[str, str]] = None,
        #     credentials: Optional[google.auth.credentials.Credentials] = None,
        #     request_metadata: Optional[Sequence[Tuple[str, str]]] = (),
        #     sync: bool = True,
    )

index = aiplatform.MatchingEngineIndex(
    index_name='7718052657499209728',
    project=project,
    location=location,
)

endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name='test_endpoint',
    network='projects/945366276631/global/networks/default',
    project=project,
    location=location,
)
'''
google.api_core.exceptions.InvalidArgument: 400 Cannot use vpc projects/945366276631/global/networks/default for project 945366276631.# Error SERVICE_NETWORKING_NOT_ENABLED


PROJECT='podsearch-367715'
NETWORK=default
PEERING_RANGE='test-peering-range'

gcloud compute addresses create "${PEERING_RANGE}" \
  --global \
  --prefix-length=16 \
  --network="${NETWORK}" \
  --purpose=VPC_PEERING \
  --project="${PROJECT}" \
  --description="test peering range."

gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --network="${DEFAULT}" \
  --ranges="${PEERING_RANGE}" \
  --project="${PROJECT}"
'''

endpoint.deploy_index(
    index=index,
    deployed_index_id='test_deployed_index',
)
'''
Deploying index MatchingEngineIndexEndpoint index_endpoint: projects/945366276631/locations/us-central1/indexEndpoints/3599510798268891136
Deploy index MatchingEngineIndexEndpoint index_endpoint backing LRO: projects/945366276631/locations/us-central1/indexEndpoints/3599510798268891136/operations/9052804042123640832
MatchingEngineIndexEndpoint index_endpoint Deployed index. Resource name: projects/945366276631/locations/us-central1/indexEndpoints/3599510798268891136
<google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint.MatchingEngineIndexEndpoint object at 0x123a0a1a0> 
resource name: projects/945366276631/locations/us-central1/indexEndpoints/3599510798268891136
'''

results = endpoint.match(
    deployed_index_id='test_deployed_index',
    queries=[[0.0 for _ in range(384)]],
    num_neighbors=1,
)
'''
PROJECT='podsearch-367715'
NETWORK='matching-engine-network'
PEERING_RANGE='matching-engine-network-peering-range'

# Create a VPC network
gcloud compute networks create "${NETWORK}" \
  --bgp-routing-mode=regional \
  --subnet-mode=auto \
  --project=${PROJECT}

# Add necessary firewall rules
gcloud compute firewall-rules create "${NETWORK}-allow-icmp" \
  --network "${NETWORK}" \
  --priority 65534 \
  --project "${PROJECT}" \
  --allow icmp

gcloud compute firewall-rules create "${NETWORK}-allow-internal" \
  --network "${NETWORK}" \
  --priority 65534 \
  --project "${PROJECT}" \
  --allow all \
  --source-ranges 10.128.0.0/9

gcloud compute firewall-rules create "${NETWORK}-allow-rdp" \
  --network "${NETWORK}" \
  --priority 65534 \
  --project "${PROJECT}" \
  --allow tcp:3389

gcloud compute firewall-rules create "${NETWORK}-allow-ssh" \
  --network "${NETWORK}" \
  --priority 65534 \
  --project "${PROJECT}" \
  --allow tcp:22

# Reserve IP range
gcloud compute addresses create "${PEERING_RANGE}" \
  --global \
  --prefix-length=16 \
  --network="${NETWORK}" \
  --purpose=VPC_PEERING \
  --project="${PROJECT}" \
  --description="peering range for matching engine network."

# Set up peering with service networking
gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --network="${NETWORK}" \
  --ranges="${PEERING_RANGE}" \
  --project="${PROJECT}"
'''


# function setup_network() {
#     NETWORK=default
#     PEERING_RANGE='test-peering-range'
#     # ERROR: (gcloud.compute.firewall-rules.create) Could not fetch resource:
#     # - The resource 'projects/podsearch-367715/global/firewalls/default-allow-icmp' already exists
#     # gcloud compute firewall-rules create "${NETWORK}-allow-icmp" \
#     #        --network "${NETWORK}" \
#     #        --priority 65534 \
#     #        --project "${PROJECT}" \
#     #        --allow icmp

#     # ERROR: (gcloud.compute.firewall-rules.create) Could not fetch resource:
#     # - The resource 'projects/podsearch-367715/global/firewalls/default-allow-internal' already exists
#     # gcloud compute firewall-rules create "${NETWORK}-allow-internal" \
#     #        --network "${NETWORK}" \
#     #        --priority 65534 \
#     #        --project "${PROJECT}" \
#     #        --allow all \
#     #        --source-ranges 10.128.0.0/9

#     # ERROR: (gcloud.compute.firewall-rules.create) Could not fetch resource:
#     # - The resource 'projects/podsearch-367715/global/firewalls/default-allow-rdp' already exists
#     # gcloud compute firewall-rules create "${NETWORK}-allow-rdp" \
#     #        --network "${NETWORK}" \
#     #        --priority 65534 \
#     #        --project "${PROJECT}" \
#     #        --allow tcp:3389

#     # ERROR: (gcloud.compute.firewall-rules.create) Could not fetch resource:
#     # - The resource 'projects/podsearch-367715/global/firewalls/default-allow-ssh' already exists
#     # gcloud compute firewall-rules create "${NETWORK}-allow-ssh" \
#     #        --network "${NETWORK}" \
#     #        --priority 65534 \
#     #        --project "${PROJECT}" \
#     #        --allow tcp:22

#     # Created [https://www.googleapis.com/compute/v1/projects/podsearch-367715/global/addresses/test-peering-range].
#     # ERROR: (gcloud.compute.addresses.create) Could not fetch resource: The resource 'projects/podsearch-367715/global/addresses/test-peering-range' already exists
#     # gcloud compute addresses create "${PEERING_RANGE}" \
#     #        --global \
#     #        --prefix-length=16 \
#     #        --network="${NETWORK}" \
#     #        --purpose=VPC_PEERING \
#     #        --project="${PROJECT}" \
#     #        --description="test peering range."

#     # API [servicenetworking.googleapis.com] not enabled on project [945366276631]. Would you like to enable and retry (this will take a few minutes)? (y/N)?  y
#     # Operation "operations/pssn.p24-945366276631-680e483c-9468-4451-9e54-001e1c916e62" finished successfully.
#     # gcloud services vpc-peerings connect \
#     #        --service=servicenetworking.googleapis.com \
#     #        --network="${NETWORK}" \
#     #        --ranges="${PEERING_RANGE}" \
#     #        --project="${PROJECT}"

# }
