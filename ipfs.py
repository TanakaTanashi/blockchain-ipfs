import requests
import json

PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxZjY4MTRlNi0xYzM3LTQxZmMtOGFiOS1iN2I1NzdlNDA1NGEiLCJlbWFpbCI6ImtldmlubGluOTYxMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiZTYxNDNmZjY5OWZlN2YwNzcxMWIiLCJzY29wZWRLZXlTZWNyZXQiOiI3YmFjYjg4MzQ4ZmI4MjI4NzE2NTFiMTI0ZjlhYTE2ZDNmYmQ5OTY1MDcyZjUxN2NlZGIyYjgwYTA0MWJhNGJkIiwiZXhwIjoxNzgyODY0MDUxfQ.ZvDteCaLlAkB8a_SRc9eL1jfSPx21mik-u4aKz7Eb60"
PINATA_GATEWAY = "amber-many-termite-502.mypinata.cloud"

def pin_to_ipfs(data):
    """
		Pin to IPFS
    """
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {PINATA_JWT}"
    }

    payload = {
        "pinataContent": data
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    result = resp.json()
    # Pinata will return IpfsHash
    cid = result.get("IpfsHash")
    return cid

def get_from_ipfs(cid, content_type="json"):
    """
		Pull by CID
    """
    assert isinstance(cid, str), "get_from_ipfs get CID"
    # private gateway
    primary_url = f"https://{PINATA_GATEWAY}/ipfs/{cid}"
    try:
        resp = requests.get(primary_url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            # fall back to public gateway
            fallback_url = f"https://ipfs.io/ipfs/{cid}"
            resp = requests.get(fallback_url, timeout=10)
            resp.raise_for_status()
        else:
            # error
            raise

    if content_type.lower() == "json":
        return resp.json()
    else:
        return resp.text
