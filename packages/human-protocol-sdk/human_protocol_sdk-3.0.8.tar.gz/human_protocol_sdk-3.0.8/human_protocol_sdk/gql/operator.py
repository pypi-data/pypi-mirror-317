from typing import Optional

from human_protocol_sdk.operator import LeaderFilter

leader_fragment = """
fragment LeaderFields on Leader {
    id
    address
    amountStaked
    amountLocked
    lockedUntilTimestamp
    amountWithdrawn
    amountSlashed
    reward
    amountJobsProcessed
    role
    fee
    publicKey
    webhookUrl
    url
    jobTypes
    registrationNeeded
    registrationInstructions
    reputationNetworks {
      address
    }
}
"""


def get_leaders_query(filter: LeaderFilter):
    return """
query GetLeaders(
    $role: String
) {{
    leaders(
      where: {{
        {role_clause}
      }}
    ) {{
      ...LeaderFields
    }}
}}
{leader_fragment}
""".format(
        leader_fragment=leader_fragment,
        role_clause="role: $role" if filter.role else "",
    )


get_leader_query = """
query getLeader($address: String!) {{
    leader(id: $address) {{
      ...LeaderFields
    }}
}}
{leader_fragment}
""".format(
    leader_fragment=leader_fragment,
)


def get_reputation_network_query(role: Optional[str]):
    return """
query getReputationNetwork(
  $address: String,
  $role: String
) {{
  reputationNetwork(id: $address) {{
    operators(
      where: {{
        {role_clause}
      }} 
    ) {{
      address,
      role,
      url,
      jobTypes,
      registrationNeeded,
      registrationInstructions

    }}
  }}
}}
""".format(
        role_clause="role: $role" if role else "",
    )
