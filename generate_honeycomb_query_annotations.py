#!/usr/bin/python3

'''
Usage: ./script_name <terraform_file_with_data_blocks> <dataset_variable_name>
'''


import sys, re

filename = sys.argv[1]
dataset_var_name = sys.argv[2]

def build_query_resource_block(name):
    return (
f'''resource "honeycombio_query" "{name}" {{
    dataset     = var.{dataset_var_name}
    query_json  = data.honeycombio_query_specification.{name}.json
}}\n\n''')

def build_query_annotation_resource_block(name):
    return (
f'''resource "honeycombio_query_annotation" "{name}" {{
    dataset     = var.{dataset_var_name}
    query_id    = honeycombio_query.{name}.id
    name        = "{snake_casing_to_capitalized_string(name)}"
}}\n\n''')

def snake_casing_to_capitalized_string(input):
    words = input.split("_")
    words[0] = words[0].capitalize()
    return ' '.join(words)

def main():
    with open(filename) as file:
        queries_file = open('query_resource.tf', 'a+')
        query_annotation_file = open('query_annotations.tf', 'a+')
        for line in file:
            l = line.strip()
            if l.startswith('data'):
                name = re.split('"(.*?)"', l)[3]
                queries_file.writelines(build_query_resource_block(name))
                query_annotation_file.writelines(build_query_annotation_resource_block(name))


main()