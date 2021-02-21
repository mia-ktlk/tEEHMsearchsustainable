from attr import asdict
from sustainable.app import db, spyder_web


def add_to_db_debug(item: dict) -> None:
    name = item["name"]
    matches = db.child("items").order_by_child("url").equal_to(item["url"]).get().each()
    if len(matches) > 1:
        print(f"something wack, more than one copy of {name}")
        return
    if matches:
        match_item = matches[0]
        key = match_item.key()
        match_item = match_item.val()
        if item["search_terms"] in match_item["search_terms"]:
            print(f"found duplicate search terms for {name}")
            return
        match_item["search_terms"] += (" " + item['search_terms'])
        db.child("items").child(key).update(match_item)
        print(f"found new search term ({item['search_terms']}) for {name}")
        return
    else:
        db.child("items").push(item)
        print(f"pushed new item {name}")


print("starting web!")


web = spyder_web

while True:
    name = input(">>  ")
    if name.lower() in ["exit", "quit", "exit()"]:
        break
    items = web.search(name, 4)
    for i in items:
        add_to_db_debug(asdict(i))
