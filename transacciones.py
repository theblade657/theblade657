
def get_unspent_outputs(address):
    try:
        unspent_outputs = NetworkAPI.get_unspent(address)
        confirmed_value = 0
        pending_value = 0
        for output in unspent_outputs:
            if output.confirmations > 1:
                confirmed_value += output.amount
            if output.confirmations < 2:
                pending_value += output.amount
        return confirmed_value, unspent_outputs, pending_value
    except Exception as e:
        print(f"Error: {e}")
        return 0, [], 0