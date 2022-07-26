from .databases import Database
import json
import typing
import pathlib


class Item:
    """
    stores the data for a single item
    """
    BUYABLE = True
    EARNABLE = False

    def __init__(self, name, price, item_type):
        self.price = int(price)
        self.name = name
        self.type = item_type

    def set_price(self, new_price):
        """
        Sets the price
        :param new_price:
        :return:
        """
        self.price = new_price

    def asDict(self) -> dict:
        """
        returns item as a dictionary
        :return:
        """
        return dict({"price": self.price, "name": self.name})

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')])})"


class Finances:
    """
    Manages all databases & items.
    """

    def __init__(self):
        # init databases
        self.expenses = Database(name="expenses", path="./data/expenses.db")
        self.income = Database(name="income", path="./data/income.db")
        # load all items
        self.earnable, self.buyable = list(), list()  # default initialization for items

    def balance(self) -> typing.Union[int, float]:
        """
        gets the balance of both databases. income - expenses = balance
        :return:
        """
        return self.income.sum() - self.expenses.sum()

    def load(self, *, itemJSON: typing.Union[str, pathlib.Path]):
        """
        Loads all items from the item file.
        Adds them to their respective lists as Item() objects.
        :param itemJSON:
        :return:
        """
        with open(itemJSON, "r+") as file:
            buyableStr, earnableStr = file.read().strip().replace("[earnable]\n", "").replace("[buyable]\n", "").split(
                "\n\n")
            self.buyable = [Item(name=i.split("-")[0], price=i.split("-")[1], item_type=Item.BUYABLE) for i in
                            buyableStr.split("\n")]
            self.earnable = [Item(name=i.split("-")[0], price=i.split("-")[1], item_type=Item.EARNABLE) for i in
                             earnableStr.split("\n")]

    def make_transaction(self, item: Item):
        """
        Makes transaction
        :param item:
        :return:
        """
        if item.type == item.EARNABLE:  # check what kind of item it is
            self.income.add(**item.asDict())  # if its earnable, just add
        elif item.type == item.BUYABLE:  # if its buyable
            if int(item.price) > self.balance():  # if insufficient funds
                return
            self.expenses.add(**item.asDict())  # add

    def query_all(self) -> dict:
        """
        queries all entries from both databases and returns as dict
        :return:
        """
        return {"expenses": self.expenses.query_all(), "income": self.income.query_all()}

    def find_item(self, name) -> typing.Union[Item, None]:
        """
        Searches for item, if it exists, returns that item.
        :param name:
        :return:
        """
        for item in (self.earnable + self.buyable):
            if item.name == name:
                return item
        return None
