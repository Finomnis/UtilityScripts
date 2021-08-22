#!/usr/bin/env python3

import click


@click.command()
@click.argument('username')
def main(username):
    print(f"Test! {username}")


if __name__ == "__main__":
    main()
