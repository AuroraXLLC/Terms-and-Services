import json
import argparse
from pathlib import Path

DATA_FILE = Path('inventory.json')

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_item(args):
    data = load_data()
    item = {
        'id': args.id,
        'brand': args.brand,
        'model': args.model,
        'purchase_price': args.purchase_price,
        'sell_price': args.sell_price,
        'quantity': args.quantity,
    }
    data.append(item)
    save_data(data)
    print(f"Added {args.brand} {args.model}")


def list_items(_args):
    data = load_data()
    for item in data:
        margin = ((item['sell_price'] - item['purchase_price']) / item['purchase_price']) * 100
        print(f"{item['id']}: {item['brand']} {item['model']} - Qty {item['quantity']} - Profit Margin {margin:.2f}%")


def main():
    parser = argparse.ArgumentParser(description='Watch inventory tracker')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a watch')
    add_parser.add_argument('--id', required=True)
    add_parser.add_argument('--brand', required=True)
    add_parser.add_argument('--model', required=True)
    add_parser.add_argument('--purchase_price', type=float, required=True)
    add_parser.add_argument('--sell_price', type=float, required=True)
    add_parser.add_argument('--quantity', type=int, default=1)
    add_parser.set_defaults(func=add_item)

    list_parser = subparsers.add_parser('list', help='List inventory')
    list_parser.set_defaults(func=list_items)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
