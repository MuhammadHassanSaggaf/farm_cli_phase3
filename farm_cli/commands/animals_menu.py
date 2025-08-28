from farm_cli.db.session import get_session
from farm_cli.db.models import Animal, AnimalFeed, Feed
from farm_cli.utils.validators import parse_date, to_float
from tabulate import tabulate

def animals_menu():
    while True:
        print('\n--- Animals Menu ---')
        print('1. Create animal')
        print('2. List all animals')
        print('3. Delete animal by id')
        print('4. View feed history for animal')
        print('5. Find animal by tag')
        print('0. Back')
        choice = input('Choose: ').strip()
        if choice == '0':
            break
        if choice == '1':
            tag = input('Tag: ').strip()
            species = input('Species: ').strip()
            breed = input('Breed (optional): ').strip() or None
            dob_in = input('DOB (YYYY-MM-DD) optional: ').strip()
            dob = None
            try:
                dob = parse_date(dob_in) if dob_in else None
            except ValueError as e:
                print('Bad date:', e)
                continue
            with get_session() as session:
                try:
                    animal = Animal.create(session, tag=tag, species=species, breed=breed, dob=dob)
                    print(f'Created animal id={animal.id} tag={animal.tag}')
                except Exception as e:
                    print('Error creating animal:', e)
        elif choice == '2':
            with get_session() as session:
                animals = Animal.get_all(session)
                rows = [(a.id, a.tag, a.species, a.breed or '', a.dob.isoformat() if a.dob else '') for a in animals]
                print(tabulate(rows, headers=['id', 'tag', 'species', 'breed', 'dob']))
        elif choice == '3':
            id_ = input('Animal id to delete: ').strip()
            try:
                idn = int(id_)
            except ValueError:
                print('id must be integer')
                continue
            with get_session() as session:
                ok = Animal.delete_by_id(session, idn)
                print('Deleted' if ok else 'Not found')
        elif choice == '4':
            id_ = input('Animal id: ').strip()
            try:
                idn = int(id_)
            except ValueError:
                print('id must be integer')
                continue
            with get_session() as session:
                events = AnimalFeed.get_for_animal(session, idn)
                rows = [(e.id, e.feed.name, e.quantity, e.date_given.isoformat()) for e in events]
                print(tabulate(rows, headers=['id', 'feed', 'qty', 'date']))
        elif choice == '5':
            tag = input('Tag to search: ').strip()
            with get_session() as session:
                a = Animal.find_by_tag(session, tag)
                if not a:
                    print('Not found')
                else:
                    print('Found:', a.id, a.tag, a.species)
        else:
            print('Unknown option')
