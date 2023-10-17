# Aldus Registry 📒

This repository acts as a catalogue of the different items that exists in a number of [Cosmos SDK](https://github.com/cosmos/cosmos-sdk) based chains.

## Supported Data

### Global

#### ⛓️ Chains

This file is currently intended only to be used with Celatone.

#### 🏢 Entities

Entities represent the individuals, teams, projects, and bodies that participate in the supported chains.

```ts
type Social = {
  // name of the social media channel
  // currently "twitter", "telegram", and "discord" are supported
  name: string,
  // the specific URL link to the entity's page on the channel
  url: string
}

type Entity = { 

  slug: string,
  // The entity's name
  name: string,
  // A short description of the entity
  description: string
  // The entity's website URL
  website: string,
  // The entity's GitHub organization/account
  github: string,
  // The entity's logo filename in /assets/entites
  logo: string,
  // The list of the entity's social media channel
  socials: []Social

}
```

#### 🪙 Assets

Assets represents the different fungible tokens found on the supported networks.

```ts
// An enum use to designate the type of asset
enum AssetType = {
  // Identifies the asset as a native coin
  Native = "native",
  // IDentifies the asset as as CW20 token
  Cw20 = "cw20"
}

type Asset = {
  // The name of the asset
  name: string,
  // A short description of the asset
  description: string,
  // A link to the asset's logo file
  logo: string,
  // The asset's decimal precision
  precision: number,
  // The list of the entity slugs that are related
  // or associated with the asset
  slugs: []string,
  // The asset's symbol
  symbol: string,
  // The type of asset
  type: AssetType,
  // A mapping of the asset's ID for different networks
  // This is the denom for native coins and
  // the token address for cw20 tokens
  id: object,
  // The asset's CoinGecko API slug. Used to pull price data
  coingecko: string,
  // The asset's CoinMarketCap API slug. Used to pull price data
  coinmarketcap: string,
}
```

### ⚛️ Core

#### 🙎‍♂️ Accounts

Accounts contains information on notable EOA, module, or multisig/smart contract accounts on a  network.

```ts
// An enum used to designate the account type for each entry
enum AccountType = {
  // Used to identify EOA or module addresses
  Account = "ACCOUNT",
  // Used to identify multisig and other smart contract accounts
  Contract = "CONTRACT",
}

type Account = {
  // The entity which created, ontrols, or are associated with the address
  slug: string,
  // The address of the account
  address: string,
  // The  label to apply to the account
  name: string,
  // A short description of the account
  description: string
  //  The type of account
  type: AccountType
}
```

### CosmWasm

#### #️⃣ Codes

Codes are notable CosmWasm codes uploaded onto a network.

```ts
type Code = {
  // The entity that uploaded or is associated with the code
  slug: string,
  // The label to apply to the code
  name: string,
  // The on-chain code ID
  id: number,
  // A short description of the code
  description: string,
  // A link to code's GitHub source code
  github: string
}
```

#### 🧩 Contracts

Contracts are notable CosmWasm contracts instantiated on a network. In most cases, for a given network, this list is a subset of the [`codes`](#️⃣-codes).

```ts
type Contract = {
  // The entity that instantiated or is associated with the code
  slug: string,
  // The label to apply to the contract
  name: string,
  // The address of the contract
  address: string,
  // The short description of the contract
  description: string,
  // The on-chain code ID the contract was instantiated from 
  code: number,
  // The link to the contract's Github source code
  github: string
}
```

### 🧪 Osmosis

#### 💧 Pools

Pools are a list of Osmosis pools identified by their asset list and pool ID.

```ts
type Pool = {
  // The on-chain ID of the pool
  id: number,
  // The name of the pool, typically the concatenated version of the list of assets
  name: string,
  // The on-chain pool address
  address: string,
  // The list of asset denoms in the pool
  assets: string[]
}
```

## Contributing

We welcome and accept pull requests to add or modify the registry data.

Before submitting any data and opening pull requests, please make sure that the information is not a duplicate and does not already exists in the registry.

### Contributing Assets

To add new assets to the registry or identify variants of existing ones on new chains, modify `data/assets.json` appropriately.

- For new assets that previously did not exist, create a new object entry in `assets.json` and fill out the necessary field outlined [above](#🪙-assets).
- For adding new IDs to existing assets, find the corresponding asset entry in `assets.json` and create a new key/value pair in the `ids` field.

Some general guidelines:

- All new entries to all files must contain a valid and existing `entity` slug. If the appropriate entity does not currently exist in the registry, create a new one in `entities.json` and fill in the necessary information.
- Avoid duplicates. Make sure that any data submitted are new and does not already exist in the repository.

### Contributing Chain Specific Data

To contribute chain-specific data such as accounts, codes, contracts, or pools, create a new JSON entry in the appropriate folder/file.
