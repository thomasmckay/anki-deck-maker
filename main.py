import genanki
import sys
import random

root_path = './'

basic = genanki.Model(
    1698742122183,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }],
    css=
    """
    .card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
    }
    """
)

def read_vocab(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        file_content = file.read()
    return file_content


def gen_notes(file_path):
    file_content = read_vocab(file_path)
    notes = []
    tag = ""
    for line in file_content.split('\n'):
        front = ''
        back = ''
        if line.strip():
            parts = line.split(' // ')

            if len(parts) == 1:
                tag = parts[0]
            elif len(parts) == 2:
                front = parts[0]
                back = parts[1]
                new_note = genanki.Note(
                    model=basic,
                    fields=[front, back],
                    tags=[tag]
                    )
                notes.append(new_note)
    return notes


def gen_deck(file_path, deck_name):
    my_deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        deck_name
    )
    notes = gen_notes(file_path)
    for note in notes:
        my_deck.add_note(note)
    return my_deck


def create_package(file_path, deck_name):
    my_deck = gen_deck(file_path, deck_name)
    genanki.Package(my_deck).write_to_file(root_path + deck_name + '.apkg')


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage: python main.py <file_name.txt> <deck_name>')
        sys.exit(1)
    file_name = sys.argv[1]
    file_path = root_path + file_name
    deck_name = sys.argv[2]
    create_package(file_path, deck_name)


if __name__ == "__main__":
    main()
