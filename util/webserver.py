from flask import Flask, render_template, request
import os

from .finances import Finances
import datetime


class WebServer(Flask):
    """
    Handles web server and endpoints.
    """

    def __init__(self, *, finances: Finances):
        super().__init__(__name__, template_folder="../templates", static_folder="../static", static_url_path="")
        self.finances = finances  # store fiances
        self.add_url_rule("/", view_func=self.index)
        self.add_url_rule("/add-transaction", view_func=self.add_transaction)
        # this filter is used to convert unix timestamp to Date string by Jinja2
        self.add_template_filter(name="from_timestamp",
                                 f=lambda timestamp, _: datetime.datetime.fromtimestamp(timestamp).strftime('%B %d'))

    def index(self):
        data = self.finances.query_all()
        return render_template("index.html", expenses=data["expenses"], income=data["income"],
                               balance=self.finances.balance(), earnable=self.finances.earnable,
                               buyable=self.finances.buyable)

    def add_transaction(self):
        """
        Adds transaction
        :return:
        """
        item = self.finances.find_item(name=request.args["name"])  # find item from url args
        if item is None:  # if no item is found, return
            return
        # if the price entered is different from the default price

        if item.price != int(request.args["price"]): item.price = request.args["price"]
        self.finances.make_transaction(item)  # make transaction
        return "", 200  # success
