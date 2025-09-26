# Raw Tracking Dataset

Tento dataset obsahuje binární data sledování (tracking) objektů v průmyslovém prostředí. Data je nutné rozbalit pomocí modulu `struct` v Pythonu s formátem `"<iQHHffffffff"`.

## Formát binárních dat

Každý záznam v souboru odpovídá následující struktuře:

- **frame_id** (int32)
- **timestamp** (uint64)
- **rb_index** (uint16)
- **flags** (uint16) — obsahuje informace o stavu (viz níže)
- **mean_error** (float32)
- **pos** (float32 × 3) — pozice [x, y, z]
- **orientation** (float32 × 4) — orientace jako quaternion [x, y, z, w]

Použitý formát pro rozbalení jednoho záznamu:
```
"<iQHHffffffff"
```

## Význam hodnot

Po rozbalení jeden záznam odpovídá slovníku:
```python
{
    "frame_id": unpacked_data[0],
    "timestamp": unpacked_data[1],
    "rb_index": unpacked_data[2],
    "flags": {
        "enabled": bool(unpacked_data[3] & 0x01),
        "tracked": bool(unpacked_data[3] & 0x02),
        "valid": bool(unpacked_data[3] & 0x04),
    },
    "mean_error": unpacked_data[4],
    "pos": [unpacked_data[5], unpacked_data[6], unpacked_data[7]],
    "orientation": [
        unpacked_data[8],
        unpacked_data[9],
        unpacked_data[10],
        unpacked_data[11],
    ],
}
```

## Použití

1. Otevřete binární soubor v Pythonu.
2. Pro každý záznam načtěte 48 bajtů a rozbalte pomocí `struct.unpack("<iQHHffffffff", data)`.
3. Výsledná data lze dále analyzovat, vizualizovat nebo exportovat do CSV.
