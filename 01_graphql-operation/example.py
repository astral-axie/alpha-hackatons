#╔═════════════════════════════════════════════════════════════════════════════╗
#║══════════════════❯ 💫 Example 💫
#╚═════════════════════════════════════════════════════════════════════════════╝


# ═════════════════════════════════════════════════════════════════════════════❯ 📦 Dependencies 📦
# ╚════════❯ 📦 Built-in Dependencies:
# ╚════════❯ 📦 External Dependencies:
import requests
# ╚════════❯ 📦 Internal Dependencies:
import operation
# ═════════════════════════════════════════════════════════════════════════════╝


# ═════════════════════════════════════════════════════════════════════════════❯ Example
url = "https://graphql-gateway.axieinfinity.com/graphql"

def get_recentlyListed_axies(criteria:dict={}, sort:str="Latest", pagination:tuple=(0,100)) -> dict:
    """
    Fetches recently listed 'Axies' from the Marketplace.

    Returns:
        ➤ dict: A dictionary that contains recently listed 'Axies' GraphQL data (cf. 'AxieBrief').
    """

    # Prepare request:
    payload = operation.GraphQLOperation("GetRecentlyListedAxies").payload
    payload["variables"]["auctionType"] = "Sale"
    payload["variables"]["criteria"] = criteria
    payload["variables"]["sort"] = sort
    payload["variables"]["from"] = pagination[0]
    payload["variables"]["size"] = pagination[-1]

    # Send request & Return the data:
    response = requests.post(url, json=payload)
    data = response.json().get("data", None)
    if data:
        return response.json()["data"].get("axies", None)
    else:
        return response.json().get("errors", None)

res = get_recentlyListed_axies(criteria={}, sort="Latest", pagination=(0,100))
print(res)
# ═════════════════════════════════════════════════════════════════════════════╝
