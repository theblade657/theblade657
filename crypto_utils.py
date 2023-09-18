from cryptos import *
from bitcoin import *
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL

def generando_billeteras_keys(entropia='b331ddcec575414f1f6dff77d032090',passphrase_='bot_telegram',simbolo='BTC',idioma='english',indice=0,passphrase_1='',passphrase_2='', texto_a_anadir=''):
  # Secret passphrase for mnemonic
  PASSPHRASE: Optional[str] = passphrase_+passphrase_1+passphrase_2
   # Initialize Bitcoin mainnet HDWallet
  hdwallet: HDWallet = HDWallet(symbol=simbolo, use_default_path=True)
  # Get Bitcoin HDWallet from entropy
  # Determina cuántos caracteres deseas reemplazar al final  
  num_caracteres_a_reemplazar = len(texto_a_anadir)
    # Reemplaza los últimos caracteres de la cadena
  if num_caracteres_a_reemplazar>0:
    entropia_nueva = entropia[:-num_caracteres_a_reemplazar] + texto_a_anadir
  else:     
    entropia_nueva=entropia
  hdwallet.from_entropy(
      entropy=entropia_nueva, language=idioma, passphrase=PASSPHRASE
  )
  direcciones={}
  billetera_info = {
        "Symbol": hdwallet.symbol(),
        "mnemonic": hdwallet.mnemonic(),
        "passphrase": hdwallet.passphrase(),
        "root_xprivate_key": hdwallet.root_xprivate_key(),
        "xpublic_key": hdwallet.xpublic_key(),
        "root_xpublic_key": hdwallet.root_xpublic_key(),
        "public_key": hdwallet.public_key(),
        "wif": hdwallet.wif(),
        "path": hdwallet.path(),
        "finger_print": hdwallet.finger_print(),
        "p2wpkh": hdwallet.p2wpkh_address()
    }
  """for address_index in range(1):
      # Drive Ethereum BIP44HDWallet
      hdwallet.clean_derivation()
      hdwallet.from_path(path="m/44'/0'/0'/0/"+str(address_index))
      # Print address_index, path, address and private_key
      address = hdwallet.p2wpkh_address()
      direcciones[address_index] = f"{address}"
      # Clean derivation indexes/paths
      hdwallet.clean_derivation()
    # Devolver el diccionario"""
  return billetera_info
# Función para obtener la tarifa según la prioridad
def obtener_tarifas(data, api_name):
    tarifas = {}
    if api_name == 'mempool':
        tarifas['alta'] = data['fastestFee']
        tarifas['media'] = data['halfHourFee']
        tarifas['baja'] = data['economyFee']
    elif api_name == 'blockchain':
        tarifas['alta'] = data['priority']
        tarifas['media'] = data['regular']
        tarifas['baja'] = data['limits']['min']
    elif api_name == 'blockstream':
        tarifas['alta'] = data['2']
        tarifas['media'] = data['25']
        tarifas['baja'] = data['144']
    elif api_name == 'bitcoiner':
        tarifas['alta'] = data['estimates']['30']['sat_per_vbyte']
        tarifas['media'] = data['estimates']['120']['sat_per_vbyte']
        tarifas['baja'] = data['estimates']['360']['sat_per_vbyte']
    return tarifas
# Función para obtener y calcular las tarifas medias por byte
def obtener_y_calcular_tarifas(lista_url):
    for url, api_name in lista_url:
        try:
            response = requests.get(url)
            data = response.json()

            # Verificar si la API proporcionó datos
            tarifas = obtener_tarifas(data, api_name)

            for prioridad, tarifa in tarifas.items():
                if tarifa is not None:
                    tarifas_por_categoria[prioridad].append(tarifa)

        except Exception as e:
            continue

# Mostrar los valores de tarifas medias por byte
def mostrar_valores_tarifas(lista_url):
    tarifas = obtener_y_calcular_tarifas(lista_url)
    return tarifas
