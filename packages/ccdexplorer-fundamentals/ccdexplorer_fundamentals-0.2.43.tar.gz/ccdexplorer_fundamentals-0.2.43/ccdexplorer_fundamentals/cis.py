from __future__ import annotations

import datetime as dt
import io
from enum import Enum
from typing import Optional, Any, Union

import base58
import leb128
from pydantic import BaseModel, ConfigDict, Field
from pymongo import ReplaceOne
from pymongo.collection import Collection
from rich.console import Console

from ccdexplorer_fundamentals.enums import NET
from ccdexplorer_fundamentals.GRPCClient import GRPCClient
from ccdexplorer_fundamentals.GRPCClient.CCD_Types import (
    CCD_AccountAddress,
    CCD_ContractAddress,
    CCD_BlockItemSummary,
    microCCD,
)
from ccdexplorer_fundamentals.mongodb import Collections

console = Console()

LEN_ACCOUNT_ADDRESS = 50


class MongoTypeTokenForAddress(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    token_address: str
    contract: str
    token_id: str
    token_amount: str


class MongoTypeTokenLink(BaseModel):
    id: str = Field(..., alias="_id")
    account_address: Optional[str] = None
    account_address_canonical: Optional[str] = None
    token_holding: Optional[MongoTypeTokenForAddress] = None


class MongoTypeTokenHolderAddress(BaseModel):
    id: str = Field(..., alias="_id")
    account_address_canonical: Optional[str] = None
    tokens: dict[str, MongoTypeTokenForAddress]


class MongoTypeLoggedEvent(BaseModel):
    id: str = Field(..., alias="_id")
    logged_event: str
    result: dict
    tag: int
    event_type: str
    block_height: int
    slot_time: Optional[dt.datetime] = None
    tx_index: int  #####################################################################
    ordering: int
    tx_hash: str
    token_address: str
    contract: str
    date: Optional[str] = None
    to_address_canonical: Optional[str] = None
    from_address_canonical: Optional[str] = None


class MongoTypeTokensTag(BaseModel):
    id: str = Field(..., alias="_id")
    contracts: list[str]
    tag_template: Optional[bool] = None
    single_use_contract: Optional[bool] = None
    logo_url: Optional[str] = None
    decimals: Optional[int] = None
    exchange_rate: Optional[float] = None
    get_price_from: Optional[str] = None
    logged_events_count: Optional[int] = None
    owner: Optional[str] = None
    module_name: Optional[str] = None
    token_type: Optional[str] = None
    display_name: Optional[str] = None
    tvl_for_token_in_usd: Optional[float] = None
    token_tag_id: Optional[str] = None


class FailedAttempt(BaseModel):
    attempts: int
    do_not_try_before: dt.datetime
    last_error: str


class MongoTypeTokenAddress(BaseModel):
    id: str = Field(..., alias="_id")
    contract: str
    token_id: str
    token_amount: Optional[str] = None
    metadata_url: Optional[str] = None
    last_height_processed: int
    token_holders: Optional[dict[str, str]] = None
    tag_information: Optional[MongoTypeTokensTag] = None
    exchange_rate: Optional[float] = None
    domain_name: Optional[str] = None
    token_metadata: Optional[TokenMetaData] = None
    failed_attempt: Optional[FailedAttempt] = None
    hidden: Optional[bool] = None


class CISProcessEventRequest(BaseModel):
    tx: CCD_BlockItemSummary
    event_index: int  # this is the index of events from either contract_initialized of contract_update_issued
    standard: Optional[StandardIdentifiers] = None  # None for unrecognized events
    instance_address: str
    event: str
    event_name: Optional[str] = None  # None for unrecognized events
    tag: int
    recognized_event: Optional[Any] = None  # None for unrecognized events
    effect_type: Optional[str] = (
        None  # for contract_update_issued, these are either interrupted or updated
    )
    effect_index: int = 0  # its index in the list


# CIS


# CIS-2 Metadata classes
class TokenAttribute(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    type: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None


class TokenURLJSON(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    url: Optional[str] = None
    hash: Optional[str] = None


class TokenMetaData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    name: Optional[str] = None
    symbol: Optional[str] = None
    unique: Optional[bool] = None
    decimals: Optional[int] = None
    description: Optional[str] = None
    thumbnail: Optional[TokenURLJSON] = None
    display: Optional[TokenURLJSON] = None
    artifact: Optional[TokenURLJSON] = None
    assets: Optional[list[TokenMetaData]] = None
    attributes: Optional[list[TokenAttribute]] = None
    localization: Optional[dict[str, TokenURLJSON]] = None


class StandardIdentifiers(Enum):
    CIS_0 = "CIS-0"
    CIS_1 = "CIS-1"
    CIS_2 = "CIS-2"
    CIS_3 = "CIS-3"
    CIS_4 = "CIS-4"
    CIS_5 = "CIS-5"
    CIS_6 = "CIS-6"


class LoggedEvents(Enum):
    transfer_event = 255
    mint_event = 254
    burn_event = 253
    operator_event = 252
    metadata_event = 251
    nonce_event = 250
    register_credential_event = 249
    revoke_credential_event = 248
    issuer_metadata_event = 247
    credential_metadata_event = 246
    credential_schemaref_event = 245
    recovation_key_event = 244
    item_created_event = 237
    item_status_changed = 236


class LEEventInfo(BaseModel):
    contract: Optional[str] = None
    standard: Optional[str] = None
    logged_event: str
    effect_index: int
    event_index: int
    event_type: Optional[str] = None
    token_address: Optional[str] = None


class LETxInfo(BaseModel):
    date: str
    tx_hash: str
    tx_index: int
    block_height: int


class MongoTypeLoggedEventV2(BaseModel):
    id: str = Field(..., alias="_id")
    event_info: LEEventInfo
    tx_info: LETxInfo
    recognized_event: Optional[
        mintEvent
        | transferEvent
        | burnEvent
        | updateOperatorEvent
        | tokenMetadataEvent
        | registerCredentialEvent
        | revokeCredentialEvent
        | issuerMetadataEvent
        | credentialMetadataEvent
        | credentialSchemaRefEvent
        | revocationKeyEvent
        | itemCreatedEvent
        | itemStatusChangedEvent
        | nonceEvent
        | depositCCDEvent
        | depositCIS2TokensEvent
        | transferCCDEvent
        | transferCIS2TokensEvent
        | withdrawCCDEvent
        | withdrawCIS2TokensEvent
    ] = None
    to_address_canonical: Optional[str] = None
    from_address_canonical: Optional[str] = None


# CIS-2 Logged Event Types


class transferEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None


class mintEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    to_address: Optional[str] = None


class burnEvent(BaseModel):
    tag: int
    token_id: Optional[str] = None
    token_amount: Optional[int] = None
    from_address: Optional[str] = None


class updateOperatorEvent(BaseModel):
    tag: int
    operator_update: Optional[str] = None
    owner: Optional[str] = None
    operator: Optional[str] = None


class SchemaRef(BaseModel):
    url: str
    checksum: Optional[str] = None


class registerCredentialEvent(BaseModel):
    tag: int
    credential_id: Optional[str] = None
    schema_ref: Optional[SchemaRef] = None
    credential_type: Optional[str] = None


class revokeCredentialEvent(BaseModel):
    tag: int
    credential_id: Optional[str] = None
    revoker: Optional[str] = None
    reason: Optional[str] = None


class issuerMetadataEvent(BaseModel):
    tag: int
    metadata: MetadataUrl


class credentialMetadataEvent(BaseModel):
    tag: int
    id: str  # credentialHolderId
    metadata: MetadataUrl


class credentialSchemaRefEvent(BaseModel):
    tag: int
    type: Optional[str] = None
    schema_ref: Optional[str] = None


class revocationKeyEvent(BaseModel):
    tag: int
    public_key_ed25519: Optional[str] = None
    action: Optional[str] = None


class MetadataUrl(BaseModel):
    url: str
    checksum: Optional[str] = None


class tokenMetadataEvent(BaseModel):
    tag: int
    token_id: str
    metadata: MetadataUrl


class itemCreatedEvent(BaseModel):
    tag: int
    item_id: str
    metadata: MetadataUrl
    initial_status: str | int


class itemStatusChangedEvent(BaseModel):
    tag: int
    item_id: str
    new_status: str | int
    additional_data: str


class nonceEvent(BaseModel):
    tag: int
    nonce: Optional[str] = None
    sponsoree: Optional[str] = None


class depositCCDEvent(BaseModel):
    tag: int
    ccd_amount: Optional[microCCD] = None
    from_address: Optional[str] = None
    to_public_key_ed25519: Optional[str] = None


class depositCIS2TokensEvent(BaseModel):
    tag: int
    token_amount: Optional[int] = None
    token_id: Optional[str] = None
    cis2_token_contract_address: Optional[str] = None
    from_address: Optional[str] = None
    to_public_key_ed25519: Optional[str] = None


class withdrawCCDEvent(BaseModel):
    tag: int
    ccd_amount: Optional[microCCD] = None
    from_public_key_ed25519: Optional[str] = None
    to_address: Optional[str] = None


class withdrawCIS2TokensEvent(BaseModel):
    tag: int
    token_amount: Optional[int] = None
    token_id: Optional[str] = None
    cis2_token_contract_address: Optional[str] = None
    from_public_key_ed25519: Optional[str] = None
    to_address: Optional[str] = None


class transferCCDEvent(BaseModel):
    tag: int
    ccd_amount: Optional[microCCD] = None
    from_public_key_ed25519: Optional[str] = None
    to_public_key_ed25519: Optional[str] = None


class transferCIS2TokensEvent(BaseModel):
    tag: int
    token_amount: Optional[int] = None
    token_id: Optional[str] = None
    cis2_token_contract_address: Optional[str] = None
    from_public_key_ed25519: Optional[str] = None
    to_public_key_ed25519: Optional[str] = None


class CIS:
    def __init__(
        self,
        grpcclient: GRPCClient = None,
        instance_index=None,
        instance_subindex=None,
        entrypoint=None,
        net: NET.MAINNET = None,
    ):
        self.grpcclient = grpcclient
        self.instance_index = instance_index
        self.instance_subindex = instance_subindex
        # self.contract_as_str = CCD_ContractAddress.from_index(
        #     instance_index, instance_subindex
        # ).to_str()
        self.entrypoint = entrypoint
        self.net = net

    ###############
    def format_address(self, address):
        if type(address) is not tuple:
            # it's an account address
            if len(address) != LEN_ACCOUNT_ADDRESS:
                return None

        if isinstance(address, tuple):
            address = f"<{address[0]},{address[1]}>"

        return address

    def execute_save(self, collection: Collection, replacement, _id: str):
        repl_dict = replacement.dict()
        if "id" in repl_dict:
            del repl_dict["id"]

        # sort tokens and token_holders
        if "tokens" in repl_dict:
            sorted_tokens = list(repl_dict["tokens"].keys())
            sorted_tokens.sort()
            tokens_sorted = {i: repl_dict["tokens"][i] for i in sorted_tokens}
            repl_dict["tokens"] = tokens_sorted

        if "token_holders" in repl_dict:
            sorted_holders = list(repl_dict["token_holders"].keys())
            sorted_holders.sort()
            token_holders_sorted = {
                i: repl_dict["token_holders"][i] for i in sorted_holders
            }
            repl_dict["token_holders"] = token_holders_sorted

        _ = collection.bulk_write(
            [
                ReplaceOne(
                    {"_id": _id},
                    replacement=repl_dict,
                    upsert=True,
                )
            ]
        )

    def restore_state_for_token_address(
        self,
        db_to_use: dict[Collections, Collection],
        token_address: str,
    ):
        d: dict = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )

        d.update(
            {
                "token_amount": str(int(0)),  # mongo limitation on int size
                "token_holders": {},  # {CCD_AccountAddress, str(token_amount)}
                "last_height_processed": 0,
            }
        )

        d = MongoTypeTokenAddress(**d)
        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def copy_token_holders_state_to_address_and_save(
        self,
        db_to_use: dict[Collections, Collection],
        token_address_info: MongoTypeTokenAddress,
        address: str,
    ):
        token_address = token_address_info.id
        d = db_to_use[Collections.tokens_accounts].find_one({"_id": address})
        # if this account doesn't have tokens, create empty dict.
        if not d:
            d = MongoTypeTokenHolderAddress(
                **{
                    "_id": address,
                    "tokens": {},
                }
            )  # keyed on token_address
        else:
            d = MongoTypeTokenHolderAddress(**d)

        token_to_save = MongoTypeTokenForAddress(
            **{
                "token_address": token_address,
                "contract": token_address_info.contract,
                "token_id": token_address_info.token_id,
                "token_amount": str(token_address_info.token_holders.get(address, 0)),
            }
        )

        d.tokens[token_address] = token_to_save

        if token_to_save.token_amount == str(0):
            del d.tokens[token_address]

        self.execute_save(db_to_use[Collections.tokens_accounts], d, address)

    def save_mint(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: mintEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "token_amount": str(int(0)),  # mongo limitation on int size
                    "token_holders": {},  # {CCD_AccountAddress, str(token_amount)}
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        token_holders: dict[CCD_AccountAddress, str] = d.token_holders  # noqa: F405
        token_holders[result.to_address] = str(
            int(token_holders.get(result.to_address, "0")) + result.token_amount
        )
        d.token_amount = str((int(d.token_amount) + result.token_amount))
        d.token_holders = token_holders

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )
        self.copy_token_holders_state_to_address_and_save(
            db_to_use, d, result.to_address
        )

    def save_metadata(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: tokenMetadataEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        d.metadata_url = result.metadata.url

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def save_operator(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: tokenMetadataEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            d = MongoTypeTokenAddress(
                **{
                    "_id": token_address,
                    "contract": instance_address,
                    "token_id": result.token_id,
                    "last_height_processed": height,
                }
            )
        else:
            d = MongoTypeTokenAddress(**d)

        d.metadata_url = result.metadata.url

        self.execute_save(
            db_to_use[Collections.tokens_token_addresses], d, token_address
        )

    def save_transfer(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: transferEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"
        d = db_to_use[Collections.tokens_token_addresses].find_one(
            {"_id": token_address}
        )
        if not d:
            return None

        d = MongoTypeTokenAddress(**d)

        try:
            token_holders: dict[CCD_AccountAddress, str] = d.token_holders  # noqa: F405
        except:  # noqa: E722
            console.log(
                f"{result.tag}: {token_address} | {d} has no field token_holders?"
            )
            Exception(
                console.log(
                    f"{result.tag}: {token_address} | {d} has no field token_holders?"
                )
            )

        token_holders[result.to_address] = str(
            int(token_holders.get(result.to_address, "0")) + result.token_amount
        )
        try:
            token_holders[result.from_address] = str(
                int(token_holders.get(result.from_address, None)) - result.token_amount
            )
            if int(token_holders[result.from_address]) >= 0:
                d.token_holders = token_holders
                d.last_height_processed = height
                self.execute_save(
                    db_to_use[Collections.tokens_token_addresses], d, token_address
                )

                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.from_address
                )
                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.to_address
                )

        except:  # noqa: E722
            if result.token_amount > 0:
                console.log(
                    f"""{result.tag}: {result.from_address} is not listed 
                    as token holder for {token_address}?"""
                )

    def save_burn(
        self,
        db_to_use: dict[Collections, Collection],
        instance_address: str,
        result: burnEvent,
        height: int,
    ):
        token_address = f"{instance_address}-{result.token_id}"

        d = MongoTypeTokenAddress(
            **db_to_use[Collections.tokens_token_addresses].find_one(
                {"_id": token_address}
            )
        )

        token_holders: dict[CCD_AccountAddress, str] = d.token_holders  # noqa: F405
        try:
            token_holders[result.from_address] = str(
                int(token_holders.get(result.from_address, "0")) - result.token_amount
            )
            if token_holders[result.from_address] == str(0):
                del token_holders[result.from_address]

            d.token_amount = str((int(d.token_amount) - result.token_amount))
            d.token_holders = token_holders
            d.last_height_processed = height

            if int(d.token_amount) >= 0:
                self.execute_save(
                    db_to_use[Collections.tokens_token_addresses], d, token_address
                )
                self.copy_token_holders_state_to_address_and_save(
                    db_to_use, d, result.from_address
                )

        except:  # noqa: E722
            console.log(
                f"""{result.tag}: {result.from_address} is not listed as 
                token holder for {token_address}?"""
            )
            # exit

    def formulate_logged_event(
        self,
        slot_time: dt.datetime,
        tag_: int,
        result: Union[
            mintEvent, burnEvent, transferEvent, updateOperatorEvent, tokenMetadataEvent
        ],
        instance_address: str,
        event: str,
        height: int,
        tx_hash: str,
        tx_index: int,
        ordering: int,
        _id_postfix: str,
    ) -> Union[ReplaceOne, None]:
        if tag_ in [255, 254, 253, 252, 251, 250]:
            if tag_ == 252:
                token_address = f"{instance_address}-operator"
            elif tag_ == 250:
                token_address = f"{instance_address}-nonce"
            else:
                token_address = f"{instance_address}-{result.token_id}"
            _id = f"{height}-{token_address}-{event}-{_id_postfix}"
            if result:
                result_dict = result.model_dump()
            else:
                result_dict = {}
            if "token_amount" in result_dict:
                result_dict["token_amount"] = str(result_dict["token_amount"])

            d = {
                "_id": _id,
                "logged_event": event,
                "result": result_dict,
                "tag": tag_,
                "event_type": LoggedEvents(tag_).name,
                "block_height": height,
                "tx_hash": tx_hash,
                "tx_index": tx_index,
                "ordering": ordering,
                "token_address": token_address,
                "contract": instance_address,
                "date": f"{slot_time:%Y-%m-%d}",
            }
            if "to_address" in result_dict:
                d.update({"to_address_canonical": result_dict["to_address"][:29]})
            if "from_address" in result_dict:
                d.update({"from_address_canonical": result_dict["from_address"][:29]})
            return (
                MongoTypeLoggedEvent(**d),
                ReplaceOne(
                    {"_id": _id},
                    replacement=d,
                    upsert=True,
                ),
            )

        else:
            return (None, None)

    # # not used
    # def execute_logged_event(
    #     self,
    #     db_to_use,
    #     tag_: int,
    #     result: Union[mintEvent, burnEvent, transferEvent, tokenMetadataEvent],
    #     instance_address: str,
    #     height: int,
    # ):
    #     if tag_ == 255:
    #         self.save_transfer(db_to_use, instance_address, result, height)
    #     elif tag_ == 254:
    #         self.save_mint(db_to_use, instance_address, result, height)
    #     elif tag_ == 253:
    #         self.save_burn(db_to_use, instance_address, result, height)
    #     elif tag_ == 252:
    #         pass
    #         # we only save the logged event, but to not process this in
    #         # token_address or accounts.
    #         # save_operator(db_to_use, instance_address, result, height)
    #     elif tag_ == 251:
    #         self.save_metadata(db_to_use, instance_address, result, height)
    #     elif tag_ == 250:
    #         pass  # nonceEvent

    def process_event(
        self,
        slot_time: dt.datetime,
        instance_address: str,
        event: str,
        height: int,
        tx_hash: str,
        tx_index: int,
        ordering: int,
        _id_postfix: str,
    ):
        tag_, result = self.process_log_events(event)
        logged_event = None
        logged_event_for_queue = None
        token_address = None
        if result:
            # if tag_ in [255, 254, 253, 252, 251, 250]:
            if tag_ in [255, 254, 253, 251]:
                token_address = f"{instance_address}-{result.token_id}"

                (logged_event, logged_event_for_queue) = self.formulate_logged_event(
                    slot_time,
                    tag_,
                    result,
                    instance_address,
                    event,
                    height,
                    tx_hash,
                    tx_index,
                    ordering,
                    _id_postfix,
                )

        return tag_, logged_event, logged_event_for_queue, token_address

    ###############

    def standard_identifier(self, identifier: StandardIdentifiers) -> bytes:
        si = io.BytesIO()
        # write the length of ASCII characters for the identifier
        number = len(identifier.value)
        byte_array = number.to_bytes(1, "little")
        si.write(byte_array)
        # write the identifier
        si.write(bytes(identifier.value, encoding="ASCII"))
        # convert to bytes
        return si.getvalue()

    def supports_parameter(self, standard_identifier: StandardIdentifiers) -> bytes:
        sp = io.BytesIO()
        # write the number of standardIdentifiers present
        number = 1
        byte_array = number.to_bytes(2, "little")
        sp.write(byte_array)
        # write the standardIdentifier
        sp.write(self.standard_identifier(standard_identifier))
        # convert to bytes
        return sp.getvalue()

    def support_result(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(2), byteorder="little")
        if t == 0:
            return t, "Standard is not supported"
        elif t == 1:
            return t, "Standard is supported by this contract"
        elif t == 2:
            contracts = []
            n = int.from_bytes(bs.read(1), byteorder="little")
            for _ in range(n):
                contracts.append(self.contract_address(bs))
                return (
                    t,
                    "Standard is supported by using one of these contract addresses: "
                    + [x for x in contracts],
                )

    def supports_response(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        if bs.getbuffer().nbytes > 0:
            n = int.from_bytes(bs.read(2), byteorder="little")
            responses = []
            for _ in range(n):
                responses.append(self.support_result(bs))
            if len(responses) > 0:
                if responses[0] is not None:
                    return responses[0]
                else:
                    return False, "Lookup Failure"
            else:
                return False, "Lookup Failure"
        else:
            return False, "Lookup Failure"

    def supports_standard(self, standard_identifier: StandardIdentifiers) -> bool:
        parameter_bytes = self.supports_parameter(standard_identifier)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result, support_result_text = self.supports_response(res)

        return support_result == 1

    def supports_standards(
        self, standard_identifiers: list[StandardIdentifiers]
    ) -> bool:
        support = False
        for si in standard_identifiers:
            parameter_bytes = self.supports_parameter(si)

            ii = self.grpcclient.invoke_instance(
                "last_final",
                self.instance_index,
                self.instance_subindex,
                self.entrypoint,
                parameter_bytes,
                self.net,
            )

            res = ii.success.return_value
            support_result, _ = self.supports_response(res)

            support = support_result == 1
        return support

    # CIS-2
    def balanceOf(self, block_hash: str, tokenID: str, addresses: list[str]):
        parameter_bytes = self.balanceOfParameter(tokenID, addresses)

        ii = self.grpcclient.invoke_instance(
            block_hash,
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result = self.balanceOfResponse(res)

        return support_result, ii

    # CIS-5
    def CCDbalanceOf(self, block_hash: str, public_keys: list[str]):
        parameter_bytes = self.CCDbalanceOfParameter(public_keys)

        ii = self.grpcclient.invoke_instance(
            block_hash,
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result = self.CCDbalanceOfResponse(res)

        return support_result, ii

    def CIS2balanceOf(
        self,
        block_hash: str,
        cis2_contract: CCD_ContractAddress,
        token_id: str,
        public_keys: list[str],
    ):
        parameter_bytes = self.CIS2balanceOfParameter(
            cis2_contract, token_id, public_keys
        )

        ii = self.grpcclient.invoke_instance(
            block_hash,
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        support_result = self.CIS2balanceOfResponse(res)

        return support_result, ii

    # CIS Components
    def account_address(self, bs: io.BytesIO):
        addr = bs.read(32)
        return base58.b58encode_check(b"\x01" + addr).decode()

    def contract_address(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little"), int.from_bytes(
            bs.read(8), byteorder="little"
        )

    def address(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs)
        else:
            raise Exception("invalid type")

    def receiver(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return self.account_address(bs)
        elif t == 1:
            return self.contract_address(bs), self.receiveHookName(bs)
        else:
            raise Exception("invalid type")

    def url(self, n: int, bs: io.BytesIO):
        data = bs.read(n)
        return data

    def metadataChecksum(self, bs: io.BytesIO):
        t = int.from_bytes(bs.read(1), byteorder="little")
        if t == 0:
            return None
        elif t == 1:
            try:
                return bs.read(32).hex()
            except:  # noqa: E722
                return -1
        else:
            # should not happen
            return -2

    def metadataUrl(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        url = bs.read(n).decode()
        checksum = self.metadataChecksum(bs)
        return MetadataUrl(**{"url": url, "checksum": checksum})

    def schema_ref(self, bs: io.BytesIO):
        metadata_url_proxy = self.metadataUrl(bs)
        return SchemaRef(
            **{"url": metadata_url_proxy.url, "checksum": metadata_url_proxy.checksum}
        )

    def receiveHookName(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        name = bs.read(n)
        return bytes.decode(name, "UTF-8")

    def additionalData(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(2), byteorder="little")
        return bytes.hex(bs.read(n))

    def tokenID(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def balanceOfQuery(self, tokenID: str, address: str):
        sp = io.BytesIO()

        tokenID = self.generate_tokenID(tokenID)
        address = self.generate_address(address)
        sp.write(tokenID)
        sp.write(address)
        return sp.getvalue()

    def CIS2balanceOfQuery(
        self, cis2_contract: CCD_ContractAddress, tokenID: str, public_key: str
    ):
        sp = io.BytesIO()

        tokenID = self.generate_tokenID(tokenID)
        contract_ = self.generate_contract_address(cis2_contract.to_str())
        public_key_ = self.generate_public_key_ed25519(public_key)

        sp.write(tokenID)
        sp.write(contract_)
        sp.write(public_key_)
        return sp.getvalue()

    def CIS2balanceOfParameter(
        self, cis2_contract: CCD_ContractAddress, token_id: str, public_keys: list[str]
    ) -> bytes:
        sp = io.BytesIO()
        sp.write(int(len(public_keys)).to_bytes(2, "little"))
        for public_key in public_keys:
            sp.write(self.CIS2balanceOfQuery(cis2_contract, token_id, public_key))
        return sp.getvalue()

    def CCDbalanceOfParameter(self, public_keys: list[str]) -> bytes:
        sp = io.BytesIO()
        sp.write(int(len(public_keys)).to_bytes(2, "little"))
        for public_key in public_keys:
            sp.write(self.generate_public_key_ed25519(public_key))
        return sp.getvalue()

    def balanceOfParameter(self, tokenID: str, addresses: list[str]) -> bytes:
        sp = io.BytesIO()
        sp.write(int(len(addresses)).to_bytes(2, "little"))
        for address in addresses:
            sp.write(self.balanceOfQuery(tokenID, address))
        return sp.getvalue()

    def CIS2balanceOfResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")

        results = []
        for _ in range(n):
            results.append(self.token_amount(bs))

        return results

    def CCDbalanceOfResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")

        results = []
        for _ in range(n):
            results.append(self.ccd_amount(bs))

        return results

    def balanceOfResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")

        results = []
        for _ in range(n):
            results.append(self.token_amount(bs))

        return results

    def generate_public_key_ed25519(self, public_key: str):
        sp = io.BytesIO()
        public_key_in_bytes = bytes.fromhex(public_key)
        sp.write(public_key_in_bytes)
        return sp.getvalue()

    def generate_tokenID(self, tokenID: str):
        sp = io.BytesIO()
        tokenID_in_bytes = bytes.fromhex(tokenID)
        sp.write(int(len(tokenID_in_bytes)).to_bytes(1, "little"))
        sp.write(tokenID_in_bytes)
        return sp.getvalue()

    def generate_account_address(self, address: str):
        return bytearray(base58.b58decode_check(address)[1:])

    def generate_contract_address(self, address: str):
        contract_address = CCD_ContractAddress.from_str(address)

        sp = io.BytesIO()
        sp.write(int(contract_address.index).to_bytes(8, "little"))
        sp.write(int(contract_address.subindex).to_bytes(8, "little"))

        return sp.getvalue()

    def generate_address(self, address: str):
        sp = io.BytesIO()

        if len(address) == 50:
            sp.write(int(0).to_bytes(1, "little"))
            sp.write(self.generate_account_address(address))
        else:
            sp.write(int(1).to_bytes(1, "little"))
            sp.write(self.generate_contract_address(address))

        return sp.getvalue()

    def invoke_token_metadataUrl(self, tokenID: str) -> bool:
        parameter_bytes = self.tokenMetadataParameter(tokenID)

        ii = self.grpcclient.invoke_instance(
            "last_final",
            self.instance_index,
            self.instance_subindex,
            self.entrypoint,
            parameter_bytes,
            self.net,
        )

        res = ii.success.return_value
        return self.tokenMetadataResultParameter(res)

    def viewOwnerHistoryRequest(self, tokenID: str):
        return self.generate_tokenID(tokenID)

    def viewOwnerHistoryResponse(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(1), byteorder="little")
        _ = bs.read(3)  # own_str
        results = []
        for _ in range(0, n):
            results.append(self.address(bs))

        return results

    def tokenMetadataParameter(self, tokenID: str):
        sp = io.BytesIO()
        sp.write(int(1).to_bytes(2, "little"))
        sp.write(self.generate_tokenID(tokenID))
        return sp.getvalue()

    def metadata_result(self, bs: bytes):
        n = int(bs[:2].decode("ASCII"))
        bs = io.BytesIO(bs)
        bs.read(2)
        url = self.url(n, bs)
        return url

    def metadata_response(self, bs: bytes):
        # bs: io.BytesIO = io.BytesIO(bs)
        if len(bs) > 0:
            n = int(bs[:2].decode("ASCII"))
            # n = int.from_bytes(bs.read(2), byteorder="big")
            responses = []
            for _ in range(n):
                responses.append(self.metadata_result(bs))
            return responses[0]
        else:
            return False, "Lookup Failure"

    def tokenMetadataResultParameter(self, res: bytes):
        bs = io.BytesIO(bytes.fromhex(res.decode()))
        n = int.from_bytes(bs.read(2), byteorder="little")
        results = []
        for _ in range(0, n):
            results.append(self.metadataUrl(bs))

        return results

    def operator_update(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Remove operator"
        elif n == 1:
            return "Add operator"

    def token_id(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def item_id(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def status(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(1), byteorder="little")

    def nonce(self, bs: io.BytesIO):
        return int.from_bytes(bs.read(8), byteorder="little")

    def token_amount(self, bs: io.BytesIO):
        return leb128.u.decode_reader(bs)[0]

    def credential_id(self, bs: io.BytesIO):
        return bytes.hex(bs.read(32))

    def credential_type(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def reason_string(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        return bytes.hex(bs.read(n))

    def revoker(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Issuer"
        elif n == 1:
            return "Holder"
        elif n == 2:
            key_ = self.credential_id(bs)
            return f"Other ({key_})"

    def optional_reason(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return None
        elif n == 2:
            reason_string_ = self.reason_string(bs)
            return reason_string_

    def signature_ed25519(self, bs: io.BytesIO) -> str:
        return bytes.hex(bs.read(64))

    def genesis_hash(self, bs: io.BytesIO) -> str:
        return bytes.hex(bs.read(32))

    def chain_context(self, bs: io.BytesIO):
        genesis_hash_ = self.genesis_hash(bs)
        contract_index_ = self.contract_index(bs)
        contract_subindex_ = self.contract_subindex(bs)
        return genesis_hash_, contract_index_, contract_subindex_

    def revocation_key_action(self, bs: io.BytesIO):
        n = int.from_bytes(bs.read(1), byteorder="little")
        if n == 0:
            return "Register"
        elif n == 1:
            return "Remove"

    def ccd_amount(self, bs: io.BytesIO) -> int:
        return int.from_bytes(bs.read(8), byteorder="little")

    def contract_index(self, bs: io.BytesIO) -> str:
        return bytes.hex(bs.read(8))

    def contract_subindex(self, bs: io.BytesIO) -> str:
        return bytes.hex(bs.read(8))

    def public_key_ed25519(self, bs: io.BytesIO) -> str:
        return bytes.hex(bs.read(32))

    # CIS events
    def transferEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)

        from_ = self.address(bs)
        from_ = self.format_address(from_)

        # if type(from_) is not tuple:
        #     # it's an account address
        #     if len(from_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(from_) == tuple:
        #     from_ = f"<{from_[0]},{from_[1]}>"
        to_ = self.address(bs)
        to_ = self.format_address(to_)
        # if type(to_) is not tuple:
        #     # it's an account address
        #     if len(to_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(to_) == tuple:
        #     to_ = f"<{to_[0]},{to_[1]}>"

        return transferEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
                "to_address": to_,
            }
        )

    def updateOperatorEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        # token_id_ = self.token_id(bs)
        update_ = self.operator_update(bs)

        owner_ = self.address(bs)
        owner_ = self.format_address(owner_)
        # if type(owner_) is not tuple:
        #     # it's an account address
        #     if len(owner_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(owner_) == tuple:
        #     owner_ = f"<{owner_[0]},{owner_[1]}>"
        operator_ = self.address(bs)
        operator_ = self.format_address(operator_)
        # if type(operator_) is not tuple:
        #     # it's an account address
        #     if len(operator_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(operator_) == tuple:
        #     operator_ = f"<{operator_[0]},{operator_[1]}>"

        return updateOperatorEvent(
            **{
                "tag": tag_,
                "operator_update": update_,
                "owner": owner_,
                "operator": operator_,
            }
        )

    def mintEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        to_ = self.address(bs)
        to_ = self.format_address(to_)
        # if type(to_) is not tuple:
        #     # it's an account address
        #     if len(to_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(to_) == tuple:
        #     to_ = f"<{to_[0]},{to_[1]}>"

        return mintEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "to_address": to_,
            }
        )

    def burnEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_id_ = self.token_id(bs)
        amount_ = self.token_amount(bs)
        from_ = self.address(bs)
        from_ = self.format_address(from_)
        # if type(from_) is not tuple:
        #     # it's an account address
        #     if len(from_) != LEN_ACCOUNT_ADDRESS:
        #         return None

        # if type(from_) == tuple:
        #     from_ = f"<{from_[0]},{from_[1]}>"

        return burnEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "token_amount": amount_,
                "from_address": from_,
            }
        )

    def tokenMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        token_id_ = self.token_id(bs)
        metadata_ = self.metadataUrl(bs)

        return tokenMetadataEvent(
            **{
                "tag": tag_,
                "token_id": token_id_,
                "metadata": metadata_,
            }
        )

    def nonceEvent(self, hexParameter: str) -> nonceEvent:
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        nonce_ = self.nonce(bs)
        sponsoree_ = self.account_address(bs)

        return nonceEvent(
            **{
                "tag": tag_,
                "nonce": str(
                    nonce_
                ),  # to cover for strangely large nonces being bounced by Mongo.
                "sponsoree": sponsoree_,
            }
        )

    def registerCredentialEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        schema_ref_ = self.schema_ref(bs)
        credential_type_ = self.credential_type(bs)
        return registerCredentialEvent(
            **{
                "tag": tag_,
                "credential_id": credential_id_,
                "schema_ref": schema_ref_,
                "credential_type": credential_type_,
            }
        )

    def revokeCredentialEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        revoker_ = self.revoker(bs)
        reason_ = self.optional_reason(bs)
        return revokeCredentialEvent(
            **{
                "tag": tag_,
                "credential_id": credential_id_,
                "revoker": revoker_,
                "reason": reason_,
            }
        )

    def issuerMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        metadata_ = self.metadataUrl(bs)

        return issuerMetadataEvent(
            **{
                "tag": tag_,
                "metadata": metadata_,
            }
        )

    def credentialMetaDataEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        credential_id_ = self.credential_id(bs)
        metadata_ = self.metadataUrl(bs)

        return credentialMetadataEvent(
            **{
                "tag": tag_,
                "id": credential_id_,
                "metadata": metadata_,
            }
        )

    def credentialSchemaRefEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        schema_ref_ = self.schema_ref(bs)
        credential_type_ = self.credential_type(bs)
        return credentialSchemaRefEvent(
            **{
                "tag": tag_,
                "type": credential_type_,
                "schema_ref": schema_ref_,
            }
        )

    def revocationKeyEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        public_key_ = self.public_key_ed25519(bs)
        action = self.revocation_key_action(bs)

        return revocationKeyEvent(
            **{
                "tag": tag_,
                "public_key_ed25519": public_key_,
                "action": action,
            }
        )

    def ItemCreatedEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        item_id_ = self.item_id(bs)
        metadata_ = self.metadataUrl(bs)
        initial_status_ = self.status(bs)

        return itemCreatedEvent(
            **{
                "tag": tag_,
                "item_id": item_id_,
                "metadata": metadata_,
                "initial_status": initial_status_,
            }
        )

    def ItemStatusChangedEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        item_id_ = self.item_id(bs)
        new_status_ = self.status(bs)
        additional_data_ = self.additionalData(bs)

        return itemStatusChangedEvent(
            **{
                "tag": tag_,
                "item_id": item_id_,
                "new_status": new_status_,
                "additional_data": additional_data_,
            }
        )

    def itemCreatedEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        item_id_ = self.item_id(bs)
        metadata_ = self.metadataUrl(bs)
        initial_status_ = self.status(bs)

        return itemCreatedEvent(
            **{
                "tag": tag_,
                "item_id": item_id_,
                "metadata": metadata_,
                "initial_status": initial_status_,
            }
        )

    def itemStatusChangedEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")

        item_id_ = self.item_id(bs)
        new_status_ = self.status(bs)
        additional_data_ = self.additionalData(bs)

        return itemStatusChangedEvent(
            **{
                "tag": tag_,
                "item_id": item_id_,
                "new_status": new_status_,
                "additional_data": additional_data_,
            }
        )

    def process_tnt_log_event(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        if tag_ == 237:
            try:
                event = self.ItemCreatedEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 236:
            try:
                event = self.ItemStatusChangedEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        else:
            return tag_, f"Custom even with tag={tag_}."

    def process_log_events(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        if tag_ == 255:
            try:
                event = self.transferEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 254:
            try:
                event = self.mintEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 253:
            try:
                event = self.burnEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 252:
            try:
                event = self.updateOperatorEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 251:
            try:
                event = self.tokenMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 250:
            try:
                event = self.nonceEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 249:
            try:
                event = self.registerCredentialEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 248:
            try:
                event = self.revokeCredentialEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 247:
            try:
                event = self.issuerMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 246:
            try:
                event = self.credentialMetaDataEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 245:
            try:
                event = self.credentialSchemaRefEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        elif tag_ == 244:
            try:
                event = self.revocationKeyEvent(hexParameter)
                return tag_, event
            except:  # noqa: E722
                return tag_, None
        else:
            return tag_, f"Custom even with tag={tag_}."

    def depositCCDEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        ccd_amount_ = self.ccd_amount(bs)
        address_ = self.address(bs)
        to_ = self.public_key_ed25519(bs)
        address_ = self.format_address(address_)

        return depositCCDEvent(
            **{
                "tag": tag_,
                "ccd_amount": ccd_amount_,
                "from_address": address_,
                "to_public_key_ed25519": to_,
            }
        )

    def depositCIS2TokensEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_amount_ = self.token_amount(bs)
        token_id_ = self.token_id(bs)
        cis2_token_contract_address_ = self.contract_address(bs)
        from_ = self.address(bs)
        from_ = self.format_address(from_)
        to_ = self.public_key_ed25519(bs)

        # transform contract_address into string
        cis2_token_contract_address_str = CCD_ContractAddress.from_index(
            cis2_token_contract_address_[0], cis2_token_contract_address_[1]
        ).to_str()

        return depositCIS2TokensEvent(
            **{
                "tag": tag_,
                "token_amount": token_amount_,
                "token_id": token_id_,
                "cis2_token_contract_address": cis2_token_contract_address_str,
                "from_address": from_,
                "to_public_key_ed25519": to_,
            }
        )

    def withdrawCCDEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        ccd_amount_ = self.ccd_amount(bs)
        from_ = self.public_key_ed25519(bs)
        to_ = self.address(bs)
        to_ = self.format_address(to_)

        return withdrawCCDEvent(
            **{
                "tag": tag_,
                "ccd_amount": ccd_amount_,
                "from_public_key_ed25519": from_,
                "to_address": to_,
            }
        )

    def withdrawCIS2TokensEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_amount_ = self.token_amount(bs)
        token_id_ = self.token_id(bs)
        cis2_token_contract_address_ = self.contract_address(bs)
        from_ = self.public_key_ed25519(bs)
        to_ = self.address(bs)
        to_ = self.format_address(to_)

        # transform contract_address into string
        cis2_token_contract_address_str = CCD_ContractAddress.from_index(
            cis2_token_contract_address_[0], cis2_token_contract_address_[1]
        ).to_str()

        return withdrawCIS2TokensEvent(
            **{
                "tag": tag_,
                "token_amount": token_amount_,
                "token_id": token_id_,
                "cis2_token_contract_address": cis2_token_contract_address_str,
                "from_public_key_ed25519": from_,
                "to_address": to_,
            }
        )

    def transferCCDEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        ccd_amount_ = self.ccd_amount(bs)
        from_ = self.public_key_ed25519(bs)
        to_ = self.public_key_ed25519(bs)

        return transferCCDEvent(
            **{
                "tag": tag_,
                "ccd_amount": ccd_amount_,
                "from_public_key_ed25519": from_,
                "to_public_key_ed25519": to_,
            }
        )

    def transferCIS2TokensEvent(self, hexParameter: str):
        bs = io.BytesIO(bytes.fromhex(hexParameter))

        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        token_amount_ = self.token_amount(bs)
        token_id_ = self.token_id(bs)
        cis2_token_contract_address_ = self.contract_address(bs)
        from_ = self.public_key_ed25519(bs)
        to_ = self.public_key_ed25519(bs)

        # transform contract_address into string
        cis2_token_contract_address_str = CCD_ContractAddress.from_index(
            cis2_token_contract_address_[0], cis2_token_contract_address_[1]
        ).to_str()

        return transferCIS2TokensEvent(
            **{
                "tag": tag_,
                "token_amount": token_amount_,
                "token_id": token_id_,
                "cis2_token_contract_address": cis2_token_contract_address_str,
                "from_public_key_ed25519": from_,
                "to_public_key_ed25519": to_,
            }
        )

    # Recognize event
    def recognize_event(self, event: str, standards: list[StandardIdentifiers]):
        """
        Contracts can support multiple standards. Hence, depending on the tag we try
        to figure our which standard such an event is specified in and try to parse it.
        """
        bs = io.BytesIO(bytes.fromhex(event))
        tag_ = int.from_bytes(bs.read(1), byteorder="little")
        if StandardIdentifiers.CIS_2 in standards:
            if tag_ == 255:
                try:
                    event = self.transferEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-2.transfer_event",
                        StandardIdentifiers.CIS_2,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 254:
                try:
                    event = self.mintEvent(event)
                    return tag_, event, "CIS-2.mint_event", StandardIdentifiers.CIS_2
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 253:
                try:
                    event = self.burnEvent(event)
                    return tag_, event, "CIS-2.burn_event", StandardIdentifiers.CIS_2
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 252:
                try:
                    event = self.updateOperatorEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-2.operator_event",
                        StandardIdentifiers.CIS_2,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 251:
                try:
                    event = self.tokenMetaDataEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-2.metadata_event",
                        StandardIdentifiers.CIS_2,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
        if StandardIdentifiers.CIS_3 in standards:
            if tag_ == 250:
                try:
                    event = self.nonceEvent(event)
                    return tag_, event, "CIS-3.nonce_event", StandardIdentifiers.CIS_3
                except:  # noqa: E722
                    return tag_, None, None, None
        if StandardIdentifiers.CIS_4 in standards:
            if tag_ == 249:
                try:
                    event = self.registerCredentialEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.register_credential_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 248:
                try:
                    event = self.revokeCredentialEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.revoke_credential_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 247:
                try:
                    event = self.issuerMetaDataEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.issuer_metadata_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 246:
                try:
                    event = self.credentialMetaDataEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.credential_metadata_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 245:
                try:
                    event = self.credentialSchemaRefEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.credential_schemaref_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 244:
                try:
                    event = self.revocationKeyEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-4.recovation_key_event",
                        StandardIdentifiers.CIS_4,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
        if StandardIdentifiers.CIS_5 in standards:
            if tag_ == 250:
                try:
                    event = self.nonceEvent(event)
                    return tag_, event, "CIS-5.nonce_event", StandardIdentifiers.CIS_5
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 249:
                try:
                    event = self.depositCCDEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.deposit_ccd_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 248:
                try:
                    event = self.depositCIS2TokensEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.deposit_cis2_tokens_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 247:
                try:
                    event = self.withdrawCCDEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.withdraw_ccd_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 246:
                try:
                    event = self.withdrawCIS2TokensEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.withdraw_cis2_tokens_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 245:
                try:
                    event = self.transferCCDEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.transfer_ccd_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 244:
                try:
                    event = self.transferCIS2TokensEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-5.transfer_cis2_tokens_event",
                        StandardIdentifiers.CIS_5,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
        if StandardIdentifiers.CIS_6 in standards:
            if tag_ == 237:
                try:
                    event = self.itemCreatedEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-6.item_created_event",
                        StandardIdentifiers.CIS_6,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            elif tag_ == 236:
                try:
                    event = self.itemStatusChangedEvent(event)
                    return (
                        tag_,
                        event,
                        "CIS-6.item_status_changed_event",
                        StandardIdentifiers.CIS_6,
                    )
                except:  # noqa: E722
                    return tag_, None, None, None
            else:
                return (
                    tag_,
                    None,
                    None,
                    None,
                )
        else:
            return tag_, None, None, None
