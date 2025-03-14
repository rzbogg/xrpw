from xrpl.clients import JsonRpcClient

def get_default_jsonrpc_client():
    return JsonRpcClient('https://xrplcluster.com')

def get_default_jsonrpc_client_testnet():
    return JsonRpcClient('https://s.altnet.rippletest.net:51234/')
