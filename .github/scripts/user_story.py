import argparse
import datetime
import pathlib
import re
import platform


try:
    from extract_content import extract_content, Config
    from parse_md_table import MarkDownTable, Row
except ImportError:
    print('err')
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    from extract_content import extract_content, Config
    from parse_md_table import MarkDownTable, Row


def add_create_args(create: argparse.ArgumentParser) -> None:
    # Add the --content flags
    create.add_argument('--content', '-c', type=str, required=True,
                        help='Content to build user story entry from')

    create.add_argument('--issue-number', '-n', type=int, required=True,
                        help='Related issue number')

    create.add_argument('--issue-html-url', '--url', type=str, default='',
                        help='URL to the related issue')

    create.add_argument('--status', '-s', type=str, required=True,
                        help='Status of the user story entry')


def add_update_args(update: argparse.ArgumentParser) -> None:
    # Add the --content flags
    update.add_argument('--issue-number', '-n', type=int, required=True,
                        help='Related issue number')

    update.add_argument('--status', '-s', type=str, required=True,
                        help='Status of the user story entry')


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    command_parser = parser.add_subparsers(
        dest='command',
        help='Action to perform',
        required=True
    )

    # Create subcommand
    create = command_parser.add_parser(
        'create',
        help='Create a new user story entry'
    )

    # Update subcommand
    update = command_parser.add_parser(
        'update',
        help='Update an existing user story entry'
    )

    add_create_args(create)
    add_update_args(update)

    # Common arguments
    # File to read/write
    parser.add_argument(
        '--file', '-f',
        type=pathlib.Path,
        default=pathlib.Path('docs/user-stories/README.md').resolve(),
        help='File to read from and add user story to'
    )

    # Skip lines (2 by default)
    parser.add_argument(
        '--skip-lines', '-l',
        type=int,
        default=2,
        help='Number of lines to skip before parsing the user story table'
    )

    return parser.parse_args()


def read_file(filepath: str | pathlib.Path) -> str:
    with open(filepath) as f:
        content = f.read()

    return content


def write_file(filepath: str | pathlib.Path, content: str) -> None:
    with open(filepath, 'w+') as f:
        f.write(content)


def add_user_story(table: MarkDownTable,
                   description: str,
                   issue_number: int,
                   html_url: str,
                   status: str) -> MarkDownTable:
    # Collapse description into one line if it isn't already
    # Multiline text will break markdown tables
    description = ' '.join(description.splitlines())
    headers = table.headers

    fmt_str: str
    if platform.system() == 'Windows':
        fmt_str = '%e %b, %Y'
    else:
        fmt_str = '%-d %b, %Y'

    time_str = datetime.datetime.today().strftime(fmt_str)

    row_str = ' | '.join((
        description,
        time_str,
        f'[#{issue_number}]({html_url})' if html_url else f'#{issue_number}',
        status
    ))

    row_str = f'| {row_str} |'

    row = Row.genfromstr(headers=headers, line=row_str)
    table.append(row)

    return table


def update_user_story(table: MarkDownTable,
                      issue_number: int,
                      status: str) -> MarkDownTable:
    pattern = re.compile(r'\[#(\d+)\]')

    def predicate(row: Row) -> bool:
        match = pattern.match(row['Tracked by Issue'])
        print(match, row)

        if match is None:
            return False

        print(match.group(1).strip())

        num = int(match.group(1).strip())
        print(type(num), type(issue_number))
        return num == issue_number

    idx, row = table.find(predicate)

    if row is None:
        raise ValueError(f'No entry with issue number {issue_number} found')

    row['Status'] = status

    return table


def main():
    args = parse_arguments()

    source = read_file(args.file)
    lines = source.splitlines()

    keep = '\n'.join(lines[:args.skip_lines])

    table_str = '\n'.join(lines[args.skip_lines:])

    table = MarkDownTable.genfromtxt(table_str)

    if args.command == 'create':
        content = args.content

        config = Config(
            start_marker=r'##',
            end_marker=r'!!',
        )
        description = extract_content(config=config, text=content)

        assert description is not None, 'Description is not available'

        add_user_story(
            table=table,
            description=description,
            issue_number=args.issue_number,
            html_url=args.issue_html_url,
            status=args.status
        )
    elif args.command == 'update':
        update_user_story(
            table=table,
            issue_number=args.issue_number,
            status=args.status
        )

    table_str = table.to_text()

    write_file(args.file, f'{keep}\n{table_str}')


if __name__ == '__main__':
    main()
