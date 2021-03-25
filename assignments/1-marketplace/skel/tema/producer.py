"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        super(Producer, self).__init__(kwargs=kwargs, daemon=True)
        # Thread.__init__(self=self, kwargs=kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.name = kwargs['name']
        self.producer_id = marketplace.register_producer()

    def run(self):
        while True:
            for product_pack in self.products:
                product, quantity, time = product_pack
                for _ in range(quantity):
                    sleep(time)
                    while not self.marketplace.publish(self.producer_id, product):
                        # print(product)
                        sleep(self.republish_wait_time)
