from typing import Any, Dict, List, Optional, TypedDict


class Asprecision(TypedDict):
    contents: int
    tag: str


class Astyle(TypedDict):
    ascommodityside: str
    ascommodityspaces: bool
    asdecimalpoint: str
    asdigitgroups: List[Any]
    asprecision: Asprecision


class Aquantity(TypedDict):
    decimalMantissa: float
    decimalPlaces: int
    floatingPoint: float


class Amount(TypedDict):
    acommodity: str
    ismultiplier: bool
    aprice: Any
    aquantity: Aquantity
    astyle: Astyle


class Tposting(TypedDict):
    paccount: str
    pamount: List[Amount]
    pbalanceassertion: Optional[str]
    pcomment: str
    pdate: Optional[str]
    pdate2: Optional[str]
    poriginal: Optional[str]
    pstatus: str
    ptags: List[List[str]]
    ptransaction_: int
    ptype: str


class HledgerTxn(TypedDict):
    tcode: str
    tcomment: str
    tdate: str
    tdate2: Optional[str]
    tdescription: str
    tindex: int
    tpostings: List[Tposting]
    tprecedingcomment: str
    tsourcerepos: Dict[str, Any]
    tstatus: str
    ttags: List[List[str]]


HledgerTxns = List[HledgerTxn]
