import os
import random

# BUILD_ID is what via_eeprom_is_valid() compares the stored VIA/Vial EEPROM
# magic against (quantum/via.c:96-106 under VIAL_ENABLE). Generating it randomly
# means EVERY rebuild invalidates the stored layout, so Vial wipes the user's
# keymap on every single flash even when nothing about the layout changed.
#
# Honour VIAL_BUILD_ID when set, so a project can PIN it and keep layouts across
# rebuilds. Pinning changes the semantics from "changed on every build" to
# "changed when the maintainer says the layout changed", which is what the check
# actually wants: bump it deliberately when vial.json or the matrix changes.
#
# Unset still falls back to random, so upstream behaviour is unchanged.
pinned = os.environ.get("VIAL_BUILD_ID")
if pinned:
    value = int(pinned, 0) & 0xFFFFFF
else:
    value = random.randrange(0, 2 ** 24 - 1)

print("#define BUILD_ID ((uint32_t)0x{:08X})".format(value))
