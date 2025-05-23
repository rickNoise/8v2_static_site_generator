from textnode import TextType, TextNode
import re

"""
Note: Markdown parsers often support nested inline elements. 
For example, you can have a bold word inside of italics:
This is an _italic and **bold** word_.
For simplicity's sake, we won't allow it!
"""

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # old_nodes is a list of TextNodes
    # this only needs to handle textual inline elements
    # namely bold, italic, and code

    if not old_nodes: # if input list is empty, just return it
        return old_nodes

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            processed_text = split_string_by_delimiter(node.text, delimiter)
            for obj in processed_text:
                new_nodes.append(
                    TextNode(
                        obj["text"],
                        text_type if obj["was_delimited"] == True else TextType.NORMAL
                    )
                )
    return new_nodes


# helper fn for split_nodes_delimiter
def split_string_by_delimiter(text, delimiter):
    # input 'text': a string; 'delimiter': a string
    # output: a list of objects of the form:
    # { "text": "slice of text", "was_delimited": bool }
    # "was_delimited" tells you whether or not that slice was surrounded by delimiters
    # delimiter characters are excluded for text slices
    # empty slices are ignored and thrown away in all instances
    # raise Exception if there is unmatched delimiter(s)
    
    if not text: # if input is the empty string
        return []

    # if the delimiter string is empty or not a string
    if len(delimiter) == 0 or not isinstance(delimiter, str):
        raise Exception("delimiter must be a non-empty string")

    try:
        delimiter_indexes = delim_index_builder(text, delimiter)
    except Exception as delim_index_builder_exception:
        raise delim_index_builder_exception

    # check for case of finding no delimiters
    if not delimiter_indexes:
        return [
            {
                "text": text,
                "was_delimited": False
            }
        ]

    # check for unmatched delimiter chars
    if len(delimiter_indexes) % 2 != 0:
        raise Exception("Unmatched delimiter! Formatting issue with input text.")

    return_lst = [] 
    # add the slice (if any) up to the first delimiter
    if delimiter_indexes[0][0] > 0:
        return_lst.append(
            {
                "text": text[:delimiter_indexes[0][0]],
                "was_delimited": False
            }
        )
    # iterate through delimiter_indexes, excluding the last one
    for i in range(len(delimiter_indexes) - 1):
        starting_char = delimiter_indexes[i][1] + 1 #start at the character after the end of the first delimiter 
        ending_char = delimiter_indexes[i + 1][0] #end at the first index of the next delimiter
        text_slice = text[ starting_char : ending_char ]
        if text_slice:
            was_delimited = (i % 2 == 0)
            return_lst.append(
                {
                    "text": text_slice,
                    "was_delimited": was_delimited
                }
            )
    # add the slice of remaining text after last delimiter
    if delimiter_indexes[-1][1] != len(text) - 1:
        starting_char = delimiter_indexes[-1][1] + 1
        return_lst.append(
            {
                "text": text[starting_char:],
                "was_delimited": False
            }
        )

    return return_lst


# helper fn for split_string_by_delimiter
def delim_index_builder(text, delimiter):
    """
    inputs -> text: str, delimiter: str
    output -> index_list: list of tuples
    each item in the list represents an occurence of the delimiter in the text string
    the first int in the tuple is the char index in the string in which the delimiter starts
    the second int in the tuple is the char index in the string in which the delimiter ends
    e.g. if the text is "012**b**89" and the delimiter is "**"
    ---> output should be: [(3, 4), (6, 7)]
    Assume the delimiter is a string and is not empty.
    """
    if len(delimiter) == 0 or not isinstance(delimiter, str):
        raise Exception("delimiter must be a non-empty string")
    delimiter_length = len(delimiter)
    delimiter_indexes = []
    for idx in range(len(text) - (delimiter_length - 1)):
        if text[idx:idx+delimiter_length] == delimiter:
            delimiter_indexes.append(
                (idx, idx+delimiter_length - 1)
            )
    return delimiter_indexes
