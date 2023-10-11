# Aldus Registry 📒

## Supported Data

### Global

#### ⛓️ Chains

#### 🏢 Entities

#### 🪙 Assets

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

#### ✅ Verified

Verified codes are on-chain codes that have been [verified](./CONTRIBUTING.md#code-verification). This list does not necessarily need to correspond with the items in the [codes](#️⃣-codes) registry for a given network.

```ts
type VerifiedCode = {
  // The on-chain ID of the verified code
  id: number,
  // The code's compiled checksum
  checksum: string,
  // The compiler/optimizer version used
  build_info: string,
  // The build environment used when compiling
  build_env: string,
  // The path to the code's directory
  module_name: string,
  // The GitHub repository hosting the code
  repository: string,
  // The Git commit hash to reference
  commit_hash: string,
  // A link to the source of information for security-related contact
  security_contact: string,
  // A boolean flag to determine whether a schema is available for the code
  schema: boolean
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
