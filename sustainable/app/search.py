from typing import Dict, List

from sustainable.app import db, spyder_web

from attr import asdict


def addToDB(obj, collection) -> None:
    db.collection(collection).set(obj)


def getResults(term: str, dataB: str, filter: str) -> List[Dict]:
    """
    gets a list of results from given search term
    """
    results = getFromDB(term, dataB)
    if len(results) < 5:
        results = results + getFromWeb(term)

    sort_key = None
    if filter:
        if filter == "r":  # rating high to low
            sort_key = lambda item: -float(item["rating"])
        elif filter == "p":  # price low to high
            sort_key = lambda item: float(item["price"])
        elif filter == "b":  # brand alphabetical
            sort_key = lambda item: item["brand"]

    return sorted(results, key=sort_key)


def getFromDB(term: str, dataB: str) -> List[Dict]:
    """
    gets a list of results from firebase db given search term
    """
    return_list = []

    all_items = db.child(dataB).get()

    for item in all_items.each():
        if (term.lower() in item.val()["name"].lower()) or (term.lower() in item.val()["search_terms"]):
            return_list.append(item.val())

    return return_list


def explicitSearch(name:str) -> object:
    """
    looks for exact item based on passed name
    """
    print(name)
    all_items = db.child("items").get()

    for item in all_items.each():
        if name.lower() == item.val()["name"].lower():
            return item


def getFromWeb(term: str) -> List[Dict]:
    """
    gets a list of results from scraped websites given search term
    """
    web_results = spyder_web.search(term, 4)
    item_dicts = [asdict(item) for item in web_results]
    for item in item_dicts:
        add_to_db(item)
    return item_dicts


def add_to_db(item: dict) -> None:
    matches = db.child("items").order_by_child("url").equal_to(item["url"]).get().each()
    if len(matches) > 1:
        return
    if matches:
        match_item = matches[0]
        key = match_item.key()
        match_item = match_item.val()
        if item["search_terms"] in match_item["search_terms"]:
            return
        match_item["search_terms"] += (" " + item['search_terms'])
        db.child("items").child(key).update(match_item)
        return
    else:
        db.child("items").push(item)
