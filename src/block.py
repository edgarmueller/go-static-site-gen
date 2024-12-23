from enum import StrEnum
import re

class BlockType(StrEnum):
	HEADING_1 = "HEADING_1"
	HEADING_2 = "HEADING_2"
	HEADING_3 = "HEADING_3"
	HEADING_4 = "HEADING_4"
	HEADING_5 = "HEADING_5"
	HEADING_6 = "HEADING_6"
	CODE = "CODE"
	QUOTE = "QUOTE"
	UNORDERED_LIST = "UNORDERED_LIST"
	ORDERED_LIST = "ORDERED_LIST"
	PARAGRAPH = "PARAGRAPH"

ORDERED_LIST_PATTERN = r"^\d+\. "

def block_to_block_type(block):
		match block:
				case _ if block.startswith("######"):
						return BlockType.HEADING_6
				case _ if block.startswith("#####"):
						return BlockType.HEADING_5
				case _ if block.startswith("####"):
						return BlockType.HEADING_4
				case _ if block.startswith("###"):
						return BlockType.HEADING_3
				case _ if block.startswith("##"):
						return BlockType.HEADING_2
				case _ if block.startswith("#"):
						return BlockType.HEADING_1
				case _ if block.startswith("```"):
						return BlockType.CODE
				case _ if block.startswith(">"):
						return BlockType.QUOTE
				case _ if block.startswith("*") or block.startswith("-"):
						return BlockType.UNORDERED_LIST
				case _ if re.match(ORDERED_LIST_PATTERN, block):
						return BlockType.ORDERED_LIST
				case _:
						return BlockType.PARAGRAPH