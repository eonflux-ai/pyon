# --------------------------------------------------------------------------------------------- #
""" Pyon: Collections Encoder """
# --------------------------------------------------------------------------------------------- #

import base64
import logging

# --------------------------------------------------------------------------------------------- #

from collections import ChainMap, Counter, deque, defaultdict
from typing import Any, Callable, TypeAlias, cast

# --------------------------------------------------------------------------------------------- #

from ..supported_types import SupportedTypes
from ..utils import EConst

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

from .base_encoder import BaseEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #

_CollectionPayload: TypeAlias = dict[str, Any]
_CollectionEncoder: TypeAlias = Callable[[object | None], _CollectionPayload | None]

# --------------------------------------------------------------------------------------------- #


class ColEnc(BaseEncoder):
    """ Collections Encoder """

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value: object | None) -> _CollectionPayload | None:
        """ Encodes the value """

        # 1. Prepare output...
        encoded = None

        # 2. Select encoder...
        if self.is_encode(value):
            encoded = self.__encode_collection_value(value)

        # 3. Return encoded...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value: object | None) -> Any | None:
        """ Decodes the value """

        # 1. Prepare output...
        decoded = None

        # 2. Select decoder...
        if isinstance(value, dict) and ut.is_decode_able(value):
            decoded = self.__decode_collection_value(value)

        # 3. Return decoded...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def __encode_collection_value(self, value: object | None) -> _CollectionPayload | None:
        """ Encodes a supported collection value through the matching helper. """

        # 1. Prepare output...
        output = None

        # 2. Prepare dispatch...
        encoders: tuple[tuple[Callable[[object | None], bool], _CollectionEncoder], ...] = (
            (
                lambda item: isinstance(item, bytearray),
                cast(_CollectionEncoder, self._encode_bytearray),
            ),
            (lambda item: isinstance(item, bytes), cast(_CollectionEncoder, self._encode_bytes)),
            (
                lambda item: isinstance(item, ChainMap),
                cast(_CollectionEncoder, self._encode_chainmap),
            ),
            (
                lambda item: isinstance(item, Counter),
                cast(_CollectionEncoder, self._encode_counter),
            ),
            (
                lambda item: isinstance(item, defaultdict),
                cast(_CollectionEncoder, self._encode_defaultdict),
            ),
            (lambda item: isinstance(item, deque), cast(_CollectionEncoder, self._encode_deque)),
            (
                lambda item: isinstance(item, frozenset),
                cast(_CollectionEncoder, self._encode_frozenset),
            ),
            (lambda item: isinstance(item, list), cast(_CollectionEncoder, self._encode_list)),
            (self._is_named_tuple, cast(_CollectionEncoder, self._encode_namedtuple)),
            (lambda item: isinstance(item, set), cast(_CollectionEncoder, self._encode_set)),
            (lambda item: isinstance(item, tuple), cast(_CollectionEncoder, self._encode_tuple)),
        )

        # 3. Match encoder...
        for matcher, encoder in encoders:
            if (output is None) and matcher(value):
                output = encoder(value)

        # 4. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __decode_collection_value(self, value: _CollectionPayload) -> Any | None:
        """ Decodes a supported collection payload through the matching helper. """

        # 1. Prepare output...
        output = None

        # 2. Prepare dispatch...
        decoders = {
            SupportedTypes.BYTEARRAY.value: self._decode_bytearray,
            SupportedTypes.BYTES.value: self._decode_bytes,
            SupportedTypes.CHAINMAP.value: self._decode_chainmap,
            SupportedTypes.COUNTER.value: self._decode_counter,
            SupportedTypes.DEFAULTDICT.value: self._decode_defaultdict,
            SupportedTypes.DEQUE.value: self._decode_deque,
            SupportedTypes.FROZENSET.value: self._decode_frozenset,
            SupportedTypes.LIST.value: self._decode_list,
            SupportedTypes.NAMEDTUPLE.value: self._decode_namedtuple,
            SupportedTypes.SET.value: self._decode_set,
            SupportedTypes.TUPLE.value: self._decode_tuple,
        }

        # 3. Run decoder...
        type_marker = value.get(EConst.TYPE)
        decoder = decoders.get(type_marker) if isinstance(type_marker, str) else None
        if decoder is not None:
            output = decoder(value)

        # 4. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value: object | None) -> bool:
        """ 
            Checks if Collection Types:
            - `bytearray`, `bytes`, `frozenset`, `list`, `set`, `tuple`
            - `ChainMap`, `Counter`, `defaultdict`, `deque`, `namedtuple` (from collections)
        """

        # 1. Check collection value...
        return isinstance(
            value,
            (
                bytearray, bytes, frozenset, list, set, tuple,
                ChainMap, Counter, defaultdict, deque
            )
        )

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value: object | None) -> bool:
        """ 
            Checks if Collection Types:
            - `bytearray`, `bytes`, `frozenset`, `list`, `set`, `tuple`
            - `ChainMap`, `Counter`, `defaultdict`, `deque`, `namedtuple` (from collections)
        """

        # 1. Prepare decode flag...
        is_decode = False

        # 2. Check collection payload...
        if isinstance(value, dict) and ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Prepare type set...
            collection_types = (
                SupportedTypes.BYTEARRAY.value,
                SupportedTypes.BYTES.value,
                SupportedTypes.CHAINMAP.value,
                SupportedTypes.COUNTER.value,
                SupportedTypes.DEFAULTDICT.value,
                SupportedTypes.DEQUE.value,
                SupportedTypes.FROZENSET.value,
                SupportedTypes.LIST.value,
                SupportedTypes.NAMEDTUPLE.value,
                SupportedTypes.SET.value,
                SupportedTypes.TUPLE.value,
            )

            # 1.2 Check type marker...
            if _type in collection_types:

                # 2.1 Accept collection type...
                is_decode = True

        # 3. Return decode flag...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _is_named_tuple(self, value: object | None) -> bool:
        """ If `value` is a named tuple """

        # 1. Check namedtuple protocol...
        return isinstance(value, tuple) and hasattr(value, EConst.FIELDS)

    # ----------------------------------------------------------------------------------------- #

    def _encode_bytearray(self, value: bytearray) -> dict[str, str] | None:
        """ Encodes a bytearray to a Base64 string """

        # 1. Prepare encoded bytearray...
        output = None
        if (value is not None) and isinstance(value, bytearray):

            # 1.1 Encode data...
            output = {
                EConst.TYPE: SupportedTypes.BYTEARRAY.value,
                EConst.DATA: base64.b64encode(value).decode('utf-8')
            }

        # 2. Log invalid bytearray...
        else:
            logger.error("Invalid input. Expected: bytearray. Received: %s", type(value))

        # 3. Return encoded bytearray...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_bytearray(self, value: _CollectionPayload) -> bytearray | None:
        """ Decodes a Base64 string back to bytearray """

        # 1. Prepare decoded bytearray...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decode content...
            output = bytearray(base64.b64decode(value[EConst.DATA]))

        # 2. Log invalid bytearray...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid bytearray input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return decoded bytearray...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_bytes(self, value: bytes) -> dict[str, str] | None:
        """ Encodes bytes to a Base64 string """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, bytes):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.BYTES.value,
                EConst.DATA: base64.b64encode(value).decode('utf-8')
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: bytes. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_bytes(self, value: _CollectionPayload) -> bytes | None:
        """ Decodes a Base64 string back to bytes """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = base64.b64decode(value[EConst.DATA])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid bytes input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_chainmap(self, value: ChainMap[Any, Any]) -> dict[str, Any] | None:
        """ Encodes a ChainMap object to a list of dictionaries. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, ChainMap):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.CHAINMAP.value,
                EConst.DATA: [
                    {k: self._encode_as_dict(v) for k, v in m.items()}
                    for m in value.maps
                ]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: ChainMap. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_chainmap(self, value: _CollectionPayload) -> ChainMap[Any, Any] | None:
        """ Decodes a list of dictionaries back to a ChainMap object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Reconstructs...
            maps = [
                {k: self._decode_from_dict(v) for k, v in m.items()}
                for m in value[EConst.DATA]
            ]

            # 1.2 Decodes...
            output = ChainMap(*maps)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid chainmap input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_counter(self, value: Counter[Any]) -> dict[str, Any] | None:
        """ Encodes a Counter object to a dictionary representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, Counter):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.COUNTER.value,
                EConst.DATA: {k: self._encode_as_dict(v) for k, v in value.items()}
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: Counter. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_counter(self, value: _CollectionPayload) -> Counter[Any] | None:
        """ Decodes a dictionary representation back to a Counter object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            decoded_data = {k: self._decode_from_dict(v) for k, v in value[EConst.DATA].items()}
            output = Counter(decoded_data)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid counter input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_defaultdict(self, value: defaultdict[Any, Any]) -> dict[str, Any] | None:
        """ Encodes a defaultdict object to a dictionary representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, defaultdict):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DEFAULTDICT.value,
                EConst.AUX1: ut.get_class_name(value.default_factory),
                EConst.DATA: {k: self._encode_as_dict(v) for k, v in value.items()}
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: defaultdict. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_defaultdict(self, value: _CollectionPayload) -> defaultdict[Any, Any] | None:
        """ Decodes a dictionary representation back to a defaultdict object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Default...
            default_factory = None

            # 1.2 Reconstructs...
            if (EConst.AUX1 in value) and value[EConst.AUX1]:
                default_factory = ut.get_class({EConst.CLASS: value[EConst.AUX1]})

            # 1.3 Decodes...
            decoded_data = {k: self._decode_from_dict(v) for k, v in value[EConst.DATA].items()}
            output = defaultdict(default_factory, decoded_data)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid defaultdict input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_deque(self, value: deque[Any]) -> dict[str, Any] | None:
        """ Encodes a deque object to a list representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, deque):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DEQUE.value,
                EConst.DATA: [self._encode_as_dict(item) for item in value]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: deque. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_deque(self, value: _CollectionPayload) -> deque[Any] | None:
        """ Decodes a list representation back to a deque object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = deque([self._decode_from_dict(item) for item in value[EConst.DATA]])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid deque input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_frozenset(self, value: frozenset[Any]) -> dict[str, Any] | None:
        """ Encodes a frozenset object to a list representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, frozenset):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.FROZENSET.value,
                EConst.DATA: [self._encode_as_dict(item) for item in value]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: frozenset. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_frozenset(self, value: _CollectionPayload) -> frozenset[Any] | None:
        """ Decodes a list representation back to a frozenset object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = frozenset([self._decode_from_dict(item) for item in value[EConst.DATA]])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid frozenset input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_list(self, value: list[Any]) -> dict[str, Any] | None:
        """ Encodes the List """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, list):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.LIST.value,
                EConst.DATA: [self._encode_as_dict(item) for item in value]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: set. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_list(self, value: _CollectionPayload) -> list[Any] | None:
        """ Decodes to List """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = [self._decode_from_dict(item) for item in value[EConst.DATA]]

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid set input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_namedtuple(self, value: tuple[Any, ...]) -> dict[str, Any] | None:
        """ Encodes a namedtuple object to a dictionary representation. """

        # 1. Checks input...
        output = None

        # 2. Validates...
        if (
            isinstance(value, tuple)
            and hasattr(value, "_fields")
            and isinstance(getattr(value, "_fields", None), tuple)
            and all(isinstance(f, str) for f in getattr(value, "_fields", ()))
            and getattr(value, "_fields", None)
        ):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.NAMEDTUPLE.value,
                EConst.CLASS: ut.get_class_name(value),
                EConst.DATA: {
                    field: self._encode_as_dict(getattr(value, field))
                    for field in getattr(value, "_fields", ())
                },
            }

        # 3. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: namedtuple. Received: %s", type(value))

        # 4. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_namedtuple(self, value: _CollectionPayload) -> Any | None:
        """ Decodes a dictionary representation back to a namedtuple object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Reconstructs...
            cls_namedtuple = ut.get_class(value)
            if cls_namedtuple is not None:

                # 2.1 Decodes individual fields...
                decoded_data = {
                    key: self._decode_from_dict(val) for key, val in value[EConst.DATA].items()
                }

                # 2.2 Creates the namedtuple...
                output = cls_namedtuple(**decoded_data)

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid namedtuple input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_set(self, value: set[Any]) -> dict[str, Any] | None:
        """ Encodes the Set """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, set):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.SET.value,
                EConst.DATA: [self._encode_as_dict(item) for item in value]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: set. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_set(self, value: _CollectionPayload) -> set[Any] | None:
        """ Decodes to Set """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = {self._decode_from_dict(item) for item in value[EConst.DATA]}

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid set input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_tuple(self, value: tuple[Any, ...]) -> dict[str, Any] | None:
        """ Encodes the Tuple """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, tuple):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.TUPLE.value,
                EConst.DATA: [self._encode_as_dict(item) for item in value]
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: tuple. Received: %s", type(value))

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_tuple(self, value: _CollectionPayload) -> tuple[Any, ...] | None:
        """ Decodes to Tuple """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = tuple(self._decode_from_dict(item) for item in value[EConst.DATA])

        # 2. Log invalid payload...
        else:

            # 1.1 Log invalid payload...
            logger.error(
                "Invalid tuple input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Return output...
        return output

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
