import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from eth_account.signers.local import LocalAccount
from web3 import Web3

from gnosis.eth.ethereum_client import EthereumNetwork
from gnosis.safe import SafeTx

from .base_api import BaseAPI, BaseAPIException


class TransactionService(BaseAPI):
    URL_BY_NETWORK = {
        EthereumNetwork.MAINNET: 'https://safe-transaction.mainnet.gnosis.io',
        EthereumNetwork.RINKEBY: 'https://safe-transaction.rinkeby.gnosis.io',
        EthereumNetwork.GOERLI: 'https://safe-transaction.goerli.gnosis.io',
        EthereumNetwork.XDAI: 'https://safe-transaction.xdai.gnosis.io',
        EthereumNetwork.VOLTA: 'https://safe-transaction.volta.gnosis.io',
        EthereumNetwork.ENERGY_WEB_CHAIN: 'https://safe-transaction.ewc.gnosis.io',
        EthereumNetwork.MATIC: 'https://safe-transaction.polygon.gnosis.io',
        EthereumNetwork.ARBITRUM: 'https://safe-transaction.arbitrum.gnosis.io',
        EthereumNetwork.BINANCE: 'https://safe-transaction.bsc.gnosis.io',
    }

    @classmethod
    def create_delegate_message_hash(cls, delegate_address: str) -> str:
        totp = int(time.time()) // 3600
        message = delegate_address + str(totp)
        print("mes",message)
        old_hash = Web3.keccak(text=message)
        hash_to_sign = Web3.keccak(text="\x19Ethereum Signed Message:\n" + str(len(message)) + message)
        print("hash", old_hash, hash_to_sign)
        return hash_to_sign

    def data_decoded_to_text(self, data_decoded: Dict[str, Any]) -> Optional[str]:
        """
        Decoded data decoded to text
        :param data_decoded:
        :return:
        """
        if not data_decoded:
            return None

        method = data_decoded['method']
        parameters = data_decoded.get('parameters', [])
        text = ''
        for parameter in parameters:  # Multisend or executeTransaction from another Safe
            if 'decodedValue' in parameter:
                text += (method + ':\n - ' + '\n - '.join([self.data_decoded_to_text(decoded_value.get('decodedData',
                                                                                                       {}))
                                                           for decoded_value in parameter.get('decodedValue', {})])
                         + '\n')
        if text:
            return text.strip()
        else:
            return (method + ': '
                    + ','.join([str(parameter['value'])
                                for parameter in parameters]))

    def get_balances(self, safe_address: str) -> List[Dict[str, Any]]:
        response = self._get_request(f'/api/v1/safes/{safe_address}/balances/')
        if not response.ok:
            raise BaseAPIException(f'Cannot get balances: {response.content}')
        else:
            return response.json()

    def get_transactions(self, safe_address: str) -> List[Dict[str, Any]]:
        response = self._get_request(f'/api/v1/safes/{safe_address}/multisig-transactions/')
        if not response.ok:
            raise BaseAPIException(f'Cannot get transactions: {response.content}')
        else:
            return response.json().get('results', [])

    def get_delegates(self, safe_address: str) -> List[Dict[str, Any]]:
        response = self._get_request(f'/api/v1/safes/{safe_address}/delegates/')
        if not response.ok:
            raise BaseAPIException(f'Cannot get delegates: {response.content}')
        else:
            return response.json().get('results', [])

    def add_delegate(self, safe_address: str, delegate_address: str, label: str, signer_account: LocalAccount):
        hash_to_sign = self.create_delegate_message_hash(delegate_address)
        # signature = signer_account.signHash(hash_to_sign)
        add_payload = {
            'safe': safe_address,
            'delegate': "0x460e497744f41E80BCb0D143Ee3aCA56f25F5E52", # "0x1000000000000000000000000000000000000003", #delegate_address,
            'signature': "0xcea43550131e473cd885b1f9c12d43da8c42e64f344352b7c4a1e8acd041b6c655595999e48d257c8d63a642217671eecfd82a6be9fb20f76b79d49b67552f4f00",
            'label': label
        }
        response = self._post_request(f'/api/v1/safes/{safe_address}/delegates/', add_payload)
        if not response.ok:
            raise BaseAPIException(f'Cannot add delegate: {response.content}')

    def remove_delegate(self, safe_address: str, delegate_address: str, signer_account: LocalAccount):
        hash_to_sign = self.create_delegate_message_hash(delegate_address)
        signature = signer_account.signHash(hash_to_sign)
        remove_payload = {
            'signature': signature.signature.hex()
        }
        response = self._delete_request(f'/api/v1/safes/{safe_address}/delegates/{delegate_address}/', remove_payload)
        if not response.ok:
            raise BaseAPIException(f'Cannot remove delegate: {response.content}')

    def post_transaction(self, safe_address: str, safe_tx: SafeTx):
        url = urljoin(self.base_url, f'/api/v1/safes/{safe_address}/multisig-transactions/')
        random_account = '0x1b95E981F808192Dc5cdCF92ef589f9CBe6891C4'
        sender = safe_tx.sorted_signers[0] if safe_tx.sorted_signers else random_account
        data = {
            'to': safe_tx.to,
            'value': safe_tx.value,
            'data': safe_tx.data.hex() if safe_tx.data else None,
            'operation': safe_tx.operation,
            'gasToken': safe_tx.gas_token,
            'safeTxGas': safe_tx.safe_tx_gas,
            'baseGas': safe_tx.base_gas,
            'gasPrice': safe_tx.gas_price,
            'refundReceiver': safe_tx.refund_receiver,
            'nonce': safe_tx.safe_nonce,
            'contractTransactionHash': safe_tx.safe_tx_hash.hex(),
            'sender': sender,
            'signature': safe_tx.signatures.hex() if safe_tx.signatures else None,
            'origin': 'Safe-CLI'
        }
        response = requests.post(url, json=data)
        if not response.ok:
            raise BaseAPIException(f'Error posting transaction: {response.content}')
