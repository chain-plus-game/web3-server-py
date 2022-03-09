# web3-server-py
Easy Websocket Web3 Wrapper

This project implements a simple web3 json rpc wrapper, in order to solve the problem of responsible code for unreal C++ code access to on-chain contracts

The linker route receives a uri parameter to connect to the corresponding rpc port, example

```
127.0.01:5000/ws?uri=https://data-seed-prebsc-1-s1.binance.org:8545/
```
This will connect and forward messages from the bsc test chain  

Before calling a contract, you need to initialize the corresponding contract abi related information. Example
```
{
    "func": "init_contract",
    "data": {
        "address": "0x376E47aD4C4eEc72d1723dD343B46fF5B9e07b85",
        "abi_url": "https://raw.githubusercontent.com/chain-plus-game/MiracleWarGame/master/src/abstract/MiracleCard.json"
    }
}
```
This will initialize the MiracleCard contract's abi related data  

After the return is successful, the contract can be called through the call method  
```
{
    "func": "call",
    "data": {
        "to": "0x376E47aD4C4eEc72d1723dD343B46fF5B9e07b85",
        "func": "balanceOf",
        "params": {
            "owner":"0xe5e0Bd2EdBa9a9AD09CBA7081c31272953Eb8948"
        }
    }
}
```
The coding part uses python web3. Compared with the conversion of complex abi to contract binary in C++ code, the python part greatly simplifies our development progress  