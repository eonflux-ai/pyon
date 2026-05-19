# --------------------------------------------------------------------------------------------- #
""" Pyon: Mapping Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from dataclasses import is_dataclass
from enum import Enum
from typing import Any, cast

# --------------------------------------------------------------------------------------------- #

from ..supported_types import SupportedTypes
from ..utils import EConst
from ..annotations import core as ann

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

from .base_encoder import BaseEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class MapEnc(BaseEncoder):
    """ Mapping Encoder """

    # ----------------------------------------------------------------------------------------- #

    def __init__(self, encoder, enc_protected: bool = False, enc_private: bool = False):
        super().__init__(encoder)

        # 1. Store export policy...
        self.enc_protected = enc_protected
        self.enc_private = enc_private

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. Prepare encoded value...
        encoded = None
        if self.is_encode(value):

            # 1.1 Encode enum...
            if isinstance(value, Enum):
                encoded = self._encode_enum(value)

            # 1.2 Encode mapping object...
            else:
                encoded = self._encode_dict(value)

        # 2. Return encoded value...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. Prepare decoded value...
        decoded = None

        # 2. Check mapping payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Decode enum...
            if _type == SupportedTypes.ENUM.value:
                decoded = self._decode_enum(value)

            # 1.2 Decode mapping object...
            else:
                decoded = self._decode_dict(value)

        # 3. Return decoded value...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Mapping Types:
            - `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`
        """

        # 1. Check mapping value...
        return self._is_dict(value) or is_dataclass(value) or isinstance(value, Enum)

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Mapping Types:
            - `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`
        """

        # 1. Prepare decode flag...
        is_decode = False

        # 2. Check mapping payload...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Prepare type set...
            mapping_types = (
                SupportedTypes.CLASS.value,
                SupportedTypes.DATACLASS.value,
                SupportedTypes.DICT.value,
                SupportedTypes.ENUM.value
            )

            # 1.2 Check type marker...
            if _type in mapping_types:

                # 2.1 Accept mapping type...
                is_decode = True

        # 3. Return decode flag...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _is_dict(self, value):
        """ Checks if Dict Like Value """

        # 1. Check dictionary protocol...
        return isinstance(value, dict) or hasattr(value, EConst.DICT)

    # ----------------------------------------------------------------------------------------- #

    def _encode_enum(self, value: Enum):
        """ Encodes the Enum """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, Enum):

            # 1.1 Encode enum value...
            encoded_value = self._encode_as_dict(value.value)

            # 1.2 Build payload...
            output = {
                EConst.TYPE: SupportedTypes.ENUM.value,
                EConst.CLASS: ut.get_class_name(value),
                EConst.DATA: encoded_value
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: Enum. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_enum(self, value: dict):
        """ Decodes to Enum """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Reconstructs...
            cls_enum = ut.get_class(value)
            if cls_enum is not None:

                # 2.1 Decodes...
                val = self._decode_from_dict(value[EConst.DATA])
                output = cls_enum(val)

        # 2. If invalid...
        else:

            # 1.1 Log invalid enum...
            logger.error(
                "Invalid enum input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_dict(self, value):
        """ Encodes the value """

        # 1. Prepare encoded mapping...
        encoded = None
        if self._is_dict(value):

            # 1.1 Annotations...
            exp_info = ann.get_export_flags(value)

            # 1.2 Private and Protected...
            enc_private = exp_info[0] or self.enc_private
            enc_protected = exp_info[1] or self.enc_protected

            # 1.3 Serializes items...
            export_policy = (enc_private, enc_protected)
            serialized_dict = {}
            for key, val in vars(value).items() if hasattr(value, EConst.DICT) else value.items():
                self.__encode_dict_item(serialized_dict, value, (key, val), export_policy)

            # 1.4 Build output...
            encoded = {
                EConst.TYPE: self._get_defulat_type(value),
                EConst.CLASS: ut.get_class_name(value),
                EConst.DICT: serialized_dict,
            }

        # 2. Return encoded mapping...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def __encode_dict_item(self, serialized_dict, value, item, export_policy):
        """Encodes one dictionary/object item according to export visibility."""

        # 1. Unpack item...
        key, val = item

        # 2. Skip internal key...
        if isinstance(key, str) and key.startswith("___"):
            return

        # 3. Resolve visibility...
        enc_private, enc_protected = export_policy
        process = self.__can_encode_dict_key(value, key, enc_private, enc_protected)

        # 4. Encode key...
        enc_key = self._encode_as_str(key)

        # 5. Store item...
        serialized_dict[enc_key] = self._encode_as_dict(val) if process else None

    # ----------------------------------------------------------------------------------------- #

    def __can_encode_dict_key(self, value, key, enc_private, enc_protected):
        """Checks whether a dictionary/object key should expose its value."""

        # 1. Prepare visible flag...
        process = True

        # 2. Validate string key...
        if isinstance(key, str):
            process = self.__can_encode_string_key(value, key, enc_private, enc_protected)

        # 3. Return decision...
        return process

    # ----------------------------------------------------------------------------------------- #

    def __can_encode_string_key(self, value, key, enc_private, enc_protected):
        """Checks string key visibility against private/protected policies."""

        # 1. Prepare private marker...
        mangled_name = ut.get_mangled_name(value)

        # 2. Check private key...
        if key.startswith("__") or key.startswith(mangled_name):
            process = enc_private

        # 3. Check protected key...
        elif key.startswith("_"):
            process = enc_protected

        # 4. Keep public key...
        else:
            process = True

        # 5. Return decision...
        return process

    # ----------------------------------------------------------------------------------------- #

    def _decode_dict(self, value):
        """ Decodes the value """

        # 1. Prepare decoded mapping...
        decoded = {}
        if isinstance(value, dict) and (EConst.TYPE in value):

            # 1.1 Dict Items...
            dict_items = value[EConst.DICT].items() if (EConst.DICT in value) else value.items()
            if dict_items:

                # 2.1 Iterates to process...
                for key, val in dict_items:

                    # 3.1 Decodes item...
                    dec_key = self._decode_from_str(key)
                    decoded[dec_key] = self._decode_from_dict(val)

            # 1.2 If decoded and class was provided...
            cls = ut.get_class(value)
            if decoded and cls:

                # 2.1 Instance and Update...
                obj = cast(Any, cls).__new__(cls)
                if hasattr(obj, EConst.DICT):

                    # 3.1 Sets...
                    obj.__dict__.update(decoded)
                    decoded = obj

        # 2. Return decoded mapping...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def _get_defulat_type(self, obj):

        # 1. Prepare type marker...
        tp = None
        if obj is not None:

            # 1.1 Detects dictionary...
            if isinstance(obj, dict):
                tp = SupportedTypes.DICT.value

            # 1.2 Detects dataclass...
            elif is_dataclass(obj):
                tp = SupportedTypes.DATACLASS.value

            # 1.3 Detects class...
            else:
                tp = SupportedTypes.CLASS.value

        # 2. Return type marker...
        return tp

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
