import argparse
import yaml
from pprint import pprint
from tabulate import tabulate
from . import IBDFileParser

def load_schema(schema_file: str) -> dict:
    with open(schema_file, 'r') as file:
        return yaml.safe_load(file)

def format_mysql_style(records, headers):
    """Format records in MySQL style output"""
    # Convert records to list of lists for tabulate
    table = [record.data for record in records]
    # Use 'psql' format which is close to MySQL style
    return tabulate(
        table,
        headers="keys",
        tablefmt="psql",
        numalign="left",  # Left align numbers like MySQL
        stralign="left"   # Left align strings
    )

def main():
    parser = argparse.ArgumentParser(description='InnoDB IBD file parser')
    parser.add_argument('-f', '--file', required=True, help='Path to .ibd file')
    parser.add_argument('-c', '--config', help='Path to schema config file (optional)')

    subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-command to run')

    # Sub-command: header
    header_parser = subparsers.add_parser('page-dump', help='Show page header')
    header_parser.add_argument('--page', type=int, required=True, help='Page number to analyze')

    args = parser.parse_args()

    # Load schema from config file if provided
    schema = load_schema(args.config) if args.config else None

    ibd_parser = IBDFileParser(args.file, schema)

    if args.command == 'page-dump':
        result = ibd_parser.page_dump(args.page)
        print("file header:")
        print(result['header'].format())
        print("\nfile trailer:")
        print(result['trailer'].format())
        if 'page_header' in result:
            print("\npage header:")
            print(result['page_header'].format_as_string())
        if 'page_directory' in result:
            print("\npage directory:")
            pprint(result['page_directory'])
        if not schema:
            print("\n(records not dumped due to missing record describer or data dictionary)")
        else:
            if 'records' in result:
                print("\nrecords:")
                print(format_mysql_style(result['records'], schema['fields']))

if __name__ == '__main__':
    main()
