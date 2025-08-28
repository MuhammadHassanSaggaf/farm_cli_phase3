from farm_cli.db.session import get_session
from farm_cli.db.models import Feed, Animal, AnimalFeed
from farm_cli.utils.validators import to_float
from tabulate import tabulate

def feeds_menu():
    while True:
        print('\n--- Feeds Menu ---')
        print('1. Create feed')
        print('2. List all feeds')
        print('3. Delete feed by id')
        print('4. Record feed given to an animal')
        print('5. View feed events for feed')
        print('0. Back')
        choice = input('Choose: ').strip()
        if choice == '0':
            break
        if choice == '1':
            name = input('Name: ').strip()
            unit = input('Unit (kg): ').strip() or 'kg'
            cost = input('Cost per unit (0): ').strip() or '0'
            stock = input('Starting stock qty (0): ').strip() or '0'
            try:
                costf = to_float(cost, 'cost')
                stockf = to_float(stock, 'stock')
            except ValueError as e:
                print(e)
                continue
            with get_session() as session:
                try:
                    feed = Feed.create(session, name=name, unit=unit, cost_per_unit=costf, stock_quantity=stockf)
                    print(f'Created feed id={feed.id} name={feed.name}')
                except Exception as e:
                    print('Error creating feed:', e)
        elif choice == '2':
            with get_session() as session:
                feeds = Feed.get_all(session)
                rows = [(f.id, f.name, f.unit, f.cost_per_unit, f.stock_quantity) for f in feeds]
                print(tabulate(rows, headers=['id', 'name', 'unit', 'cost', 'stock']))
        elif choice == '3':
            id_ = input('Feed id to delete: ').strip()
            try:
                idn = int(id_)
            except ValueError:
                print('id must be integer')
                continue
            with get_session() as session:
                ok = Feed.delete_by_id(session, idn)
                print('Deleted' if ok else 'Not found')
        elif choice == '4':
            animal_id = input('Animal id: ').strip()
            feed_id = input('Feed id: ').strip()
            qty = input('Quantity: ').strip()
            try:
                aid = int(animal_id); fid = int(feed_id); qf = float(qty)
            except Exception:
                print('Invalid numeric input')
                continue
            with get_session() as session:
                animal = Animal.find_by_id(session, aid)
                feed = Feed.find_by_id(session, fid)
                if not animal or not feed:
                    print('Animal or Feed not found')
                    continue
                try:
                    ev = AnimalFeed.create(session, animal=animal, feed=feed, quantity=qf)
                    print('Recorded feed event id=', ev.id)
                except Exception as e:
                    print('Error:', e)
        elif choice == '5':
            id_ = input('Feed id: ').strip()
            try:
                idn = int(id_)
            except ValueError:
                print('id must be integer')
                continue
            with get_session() as session:
                events = AnimalFeed.get_for_feed(session, idn)
                rows = [(e.id, e.animal.tag if e.animal else '', e.quantity, e.date_given.isoformat()) for e in events]
                print(tabulate(rows, headers=['id', 'animal', 'qty', 'date']))
        else:
            print('Unknown option')
