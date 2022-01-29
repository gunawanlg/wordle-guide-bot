from main import play
from guide import parse_args


if __name__ == "__main__":
    args = parse_args()
    result = play(args.path, debug=False)
    print(result)
