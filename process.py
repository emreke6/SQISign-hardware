import re
import json
import sys
from pathlib import Path


# --------------------------------------------------
# Clean log (remove "30:" prefixes etc.)
# --------------------------------------------------
def clean_log(text):
    return re.sub(r"^\d+:\s*", "", text, flags=re.MULTILINE)


# --------------------------------------------------
# Safe extraction helpers
# --------------------------------------------------
def find_hex(pattern, text):
    m = re.search(pattern, text)
    return int(m.group(1), 16) if m else None


def find_int(pattern, text):
    m = re.search(pattern, text)
    return int(m.group(1)) if m else None


def find_bool(pattern, text):
    m = re.search(pattern, text)
    return bool(int(m.group(1))) if m else False


# --------------------------------------------------
# Signature parser
# --------------------------------------------------
def parse_signature(block):
    return {
        "E_aux_A": {
            "real": find_hex(r"E_aux_A\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
            "imag": find_hex(r"E_aux_A\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
        },
        "backtracking": find_int(r"backtracking\s*=\s*(\d+)", block),
        "two_resp_length": find_int(r"two_resp_length\s*=\s*(\d+)", block),
        "hint_aux": find_int(r"hint_aux\s*=\s*(\d+)", block),
        "hint_chall": find_int(r"hint_chall\s*=\s*(\d+)", block),
        "mat_Bchall_can_to_B_chall": [
            [
                find_hex(r"\[0\]\[0\]\s*=\s*(0x[0-9a-fA-F]+)", block),
                find_hex(r"\[0\]\[1\]\s*=\s*(0x[0-9a-fA-F]+)", block),
            ],
            [
                find_hex(r"\[1\]\[0\]\s*=\s*(0x[0-9a-fA-F]+)", block),
                find_hex(r"\[1\]\[1\]\s*=\s*(0x[0-9a-fA-F]+)", block),
            ],
        ],
        "chall_coeff": find_hex(r"chall_coeff\s*=\s*(0x[0-9a-fA-F]+)", block),
    }


# --------------------------------------------------
# Public key parser
# --------------------------------------------------
def parse_public_key(block):
    return {
        "curve": {
            "A": {
                "real": find_hex(r"A\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                "imag": find_hex(r"A\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
            },
            "C": {
                "real": find_hex(r"C\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                "imag": find_hex(r"C\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
            },
            "A24": None,
            "is_A24_computed_and_normalized": False,
        },
        "hint_pk": find_int(r"hint_pk\s*=\s*(\d+)", block),
    }


# --------------------------------------------------
# Ecom curve parser
# --------------------------------------------------
def parse_ecom(block):
    return {
        "curve": {
            "A": {
                "real": find_hex(r"A\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                "imag": find_hex(r"A\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
            },
            "C": {
                "real": find_hex(r"C\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                "imag": find_hex(r"C\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
            },
            "A24": {
                "x": {
                    "real": find_hex(r"A24\.x\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                    "imag": find_hex(r"A24\.x\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
                },
                "z": {
                    "real": find_hex(r"A24\.z\.real\s*=\s*(0x[0-9a-fA-F]+)", block),
                    "imag": find_hex(r"A24\.z\.imag\s*=\s*(0x[0-9a-fA-F]+)", block),
                },
            },
            "is_A24_computed_and_normalized": find_bool(
                r"is_A24_computed_and_normalized\s*=\s*(\d+)", block
            ),
        }
    }


# --------------------------------------------------
# Message parser
# --------------------------------------------------
def parse_messages(text):
    out = []
    for m in re.finditer(
        r"message\s*\((\d+)\s*bytes\):\s*([0-9a-fA-F]+)", text
    ):
        out.append(
            {
                "length": int(m.group(1)),
                "message": m.group(2),
            }
        )
    return out


# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main(path):
    raw = Path(path).read_text()
    text = clean_log(raw)

    signatures = [
        parse_signature(b)
        for b in re.findall(
            r"={5,}\s*SIGNATURE DUMP\s*={5,}(.*?)={5,}",
            text,
            re.DOTALL,
        )
    ]

    public_keys = [
        parse_public_key(b)
        for b in re.findall(
            r"={5,}\s*PUBLIC KEY DUMP\s*={5,}(.*?)={5,}",
            text,
            re.DOTALL,
        )
    ]

    ecoms = [
        parse_ecom(b)
        for b in re.findall(
            r"Ecom_Eaux_E1:\s*(.*?)(?:message length|pk:|===)",
            text,
            re.DOTALL,
        )
    ]

    messages = parse_messages(text)

    print(
        json.dumps(
            {
                "messages": messages,
                "signatures": signatures,
                "public_keys": public_keys,
                "Ecom_Eaux_E1": ecoms,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main(sys.argv[1])
