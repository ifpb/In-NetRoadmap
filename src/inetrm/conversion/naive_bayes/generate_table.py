import copy
import re

from ..datatypes import get_datatype


def writeactionrule(writer, ranges, table_name, action, result):
    command = f"table_add {table_name} classify_exact {action} "
    for i in range(len(ranges)):
        command += f"{ranges[i][0]}->{ranges[i][1]} "
    command += f"=> {str(result)} 0\n"

    writer.write(command)
    # print("add action rule")


def writefeatureXrule(writer, range, table, action, ind):
    # print(range)
    # print(ind)
    # print(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)}")
    writer.write(f"table_add {table} {action} {range[0]}->{range[1]} => {str(ind)} 0\n")
    # print(f"add {table} rule")


def generate_table(rf_data: dict, output_path: str):
    raise NotImplementedError("TODO generate tables for naive bayes")