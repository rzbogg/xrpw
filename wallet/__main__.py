from wallet.cli import cli


if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print('ops')

