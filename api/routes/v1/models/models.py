from dataclasses import dataclass
from typing import List


class Account:
    slug: str
    address: str
    name: str
    description: str
    type: str


class Asset:
    coingecko: str
    description: str
    id: str
    logo: str
    name: str
    precision: int
    slugs: List[str]
    symbol: str
    type: str


class Code:
    slug: str
    id: int
    name: str
    description: str
    github: str


class Contract:
    slug: str
    name: str
    description: str
    address: str
    code: int
    github: str


class Module:
    slug: str
    address: str
    name: str
    description: str
    github: str


@dataclass
class Social:
    name: str
    url: str


class RawEntity:
    slug: str
    name: str
    description: str
    website: str
    logo: str
    github: str
    socials: List[Social]
    accounts: List[Account] = None
    codes: List[Code] = None
    contracts: List[Contract] = None
    modules: List[Module] = None


class EntityDetail:
    description: str
    github: str
    logo: str
    name: str
    socials: List[Social]
    website: str


class Entity:
    slug: str
    details: EntityDetail
    accounts: List[Account] = None
    codes: List[Code] = None
    contracts: List[Contract] = None
    modules: List[Module] = None
