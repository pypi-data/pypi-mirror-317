# -*- coding: utf-8 -*-
import heimdall
import os as _os
import re as _re
from sys import version_info as _py
from urllib.parse import urlparse
from ..decorators import get_database, create_database
LENGTH_PREFIX = 'len:'


@create_database(['sql:mariadb', 'sql:mysql', ])
def dump(tree, url, **options):
    r"""Serialize a HERA elements tree into a MySQL dump like file

    :param tree: HERA elements tree
    :param url: Path of the MySQL dump file to create
    :param \**options: (optional) Keyword arguments, see below.
    :Keyword arguments:
        * **allow_multivalues** (``bool``) -- (optional, default: ``True``)
          If ``True`` multiple values for the same entity attribute will be
          put in the same SQL column, separated by ``multivalue_separator``.
          If ``False``, this function will raise an error
          should any attribute have a ``max`` greater than 1.
        * **multivalue_separator** (``str``) -- (optional, default: ``,``)
          "Character" separating multiple values for the same attribute
          in a given entity; used only if ``allow_multivalues`` is ``True``.
    """
    path = url
    if _os.path.exists(path):
        raise ValueError(f"File '{path}' already exists")

    allow = options.get('allow_multivalues', False)
    allow = True  # TODO
    comma = options.get('multivalue_separator', ',')
    with open(path, 'w', newline='') as f:
        f.write(f"{_pre_everything()}\n")
        for entity in heimdall.getEntities(tree):
            eid = entity.get('id')
            attributes = heimdall.getAttributes(entity)
            items = heimdall.getItems(tree, lambda n: n.get('eid') == eid)
            f.write(f"\n{_pre_create_table(eid)}\n")
            f.write(f"{_create_table(tree, eid, attributes, allow)}\n")
            f.write(f"{_pre_dump_data(eid)}\n")
            f.write(f"{_dump_data(items, eid, attributes, comma)}\n")
            f.write(f"{_post_dump_data()}\n")


def _pre_everything():
    text = "-- SQL dump, from a HERA database, using pyHeimdall\n"
    text += "-- ------------------------------------------------------\n"
    text += f"-- pyHeimdall version	{heimdall.__version__}"
    return text


def _pre_create_table(eid, drop=True):
    comment = f"--\n-- Table structure for table `{eid}`\n--"
    drop_table = f"\nDROP TABLE IF EXISTS `{eid}`;" if drop else ""
    return comment + drop_table


def _create_table(tree, eid, attributes, allow_multivalues):
    text = f"CREATE TABLE `{eid}` (\n"
    for attribute in attributes:
        (aid, pid) = _get_identifiers(attribute)
        if aid is None and pid is None:
            continue  # this unused attribute won't be part of the dump
        _id = aid if aid is not None else pid
        max = attribute.get('max')
        max = int(max) if max else None
        if not allow_multivalues and (max is None or max > 1):
            fault = f"{eid}.{aid}.max={max}"
            raise ValueError(f"Repeatable attributes not supported ({fault})")
        min = int(attribute.get('min') or 0)
        min = "NOT NULL" if min > 0 else "DEFAULT NULL"
        type = _get_type(tree, attribute)
        text += f"`{_id}` {type} {min},\n"
    if text.endswith(',\n'):
        text = text[:-2] + '\n'  # remove last comma
    text += ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;"
    return text


def _get_identifiers(attribute):
    return (attribute.get('id'), attribute.get('pid'))


def _get_type(tree, attribute):
    type_node = heimdall.util.get_node(attribute, 'type')
    if type_node is not None:
        type_ = type_node.text
    else:
        pid = attribute.get('pid')
        property_ = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
        type_node = heimdall.util.get_node(attribute, 'type')
        if type_node is not None:
            type_ = type_node.text
        else:
            type_ = 'text'
    if type_ == 'datetime':
        return 'date'
    if type_ == 'number':
        return 'int'  # TODO unsigned
    rules = heimdall.util.get_nodes(attribute, 'rule')
    length = 255
    for rule in rules:
        if rule.text.startswith(LENGTH_PREFIX):
            length = int(rule.text[len(LENGTH_PREFIX):])
    if length > 1:
        return f'varchar({length})'
    return 'char(1)'


def _pre_dump_data(eid, lock=True):
    comment = f"--\n-- Dumping data for table `{eid}`\n--"
    lock_table = f"\nLOCK TABLE `{eid}` WRITE;" if lock else ""
    return comment + lock_table


def _dump_data(items, eid, attributes, multivalues_separator):
    if len(items) == 0:
        return f"-- No data in table `{eid}`"
    text = f"INSERT INTO `{eid}` VALUES "
    dumps = list()
    for item in items:
        values = list()
        for attribute in attributes:
            values.append(_dump_value(item, attribute, multivalues_separator))
        dumps.append(f"({','.join(values)})")
    text += ','.join(dumps)
    text += ";"
    return text


def _dump_value(item, attribute, multivalues_separator):
    (aid, pid) = _get_identifiers(attribute)
    values = list()
    if aid is not None:
        if pid is not None:
            values = heimdall.getValues(item, pid=pid, aid=aid)
        else:
            values = heimdall.getValues(item, aid=aid)
    else:
        if pid is not None:
            values = heimdall.getValues(item, pid=pid)
    values = [f"'{v}'" for v in values]
    if len(values) < 1:
        return 'NULL'
    return multivalues_separator.join(values)


def _post_dump_data(lock=True):
    return "UNLOCK TABLES;"
