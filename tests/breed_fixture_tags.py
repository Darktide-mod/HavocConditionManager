"""Read the two native tag assignment forms (both use string enum keys)."""
import re


def parse_tags(block):
    # Native BreedSettings.tags uses enum_from_array: t[value] = value.
    # Keep literal assignments for pre-1.13 source checkouts.
    assignments = re.findall(
        r'(?:\[\s*breed_tags\.(\w+)\s*\]|\b(\w+))\s*=\s*true\b', block)
    return {enum_key or literal_key: True for enum_key, literal_key in assignments}
