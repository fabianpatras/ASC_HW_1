"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self=self, kwargs=kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs['name']
        self.crt_cart_id = None

    def run(self):
        crt_cart_id = None

        for cart in self.carts:
            crt_cart_id = self.marketplace.new_cart()

            for actions in cart:
                comm_type = actions['type']
                product = actions['product']
                quantity = actions['quantity']

                if comm_type == "add":
                    for _ in range(quantity):
                        while not self.marketplace.add_to_cart(crt_cart_id, product):
                            sleep(self.retry_wait_time)
                            # print(self.name, "incerc sa bag", sep=" ")
                elif comm_type == "remove":
                    for _ in range(quantity):
                        # while not self.marketplace.remove_from_cart(crt_cart_id, product):
                        #     sleep(self.retry_wait_time)
                        #     print(self.name, "incerc sa scot", sep=" ")
                        while not self.marketplace.remove_from_cart(crt_cart_id, product):
                            sleep(self.retry_wait_time)
                            # print(self.name, "incerc sa scot", sep=" ")

            # here the cart is finished

            items = self.marketplace.place_order(crt_cart_id)

            for itm in items[::-1]:
                print(self.name, "bought", itm, sep=" ")
