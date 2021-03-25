"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.queues = []
        self.producers = 0
        self.queue_size_per_producer = queue_size_per_producer

        self.carts = []
        self.crt_carts = 0

        self.register_producer_lock = Lock()
        self.new_cart_lock = Lock()
        self.add_remove_item_lock = Lock()

        self.lock_per_queue = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        ret_id = None

        with self.register_producer_lock:
            ret_id = self.producers
            self.queues.append([])
            self.lock_per_queue.append(Lock())
            self.producers += 1

        return ret_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        with self.lock_per_queue[producer_id]:
            if len(self.queues[producer_id]) < self.queue_size_per_producer:
                self.queues[producer_id].append(product)
                return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        ret_id = None

        with self.new_cart_lock:
            ret_id = self.crt_carts
            self.crt_carts += 1
            self.carts.append([]) # ?? TODO: what is a cart?

        return ret_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.register_producer_lock.acquire() # lock for self.producers
        for i in range(self.producers):
            self.register_producer_lock.release()

            self.lock_per_queue[i].acquire() # lock per individual queue
                                            # to let the other queues work

            for j in range(len(self.queues[i])):
                q_product = self.queues[i][j]
                if q_product == product:
                    self.queues[i].pop(j) # remove from prod_queueu
                    self.carts[cart_id].append((i, product)) # add to cart
                    self.lock_per_queue[i].release()
                    return True

            self.lock_per_queue[i].release()

            self.register_producer_lock.acquire()
        self.register_producer_lock.release()

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        # cart is unique per consumer so he's the only one to get here
        # no need to lock per cart_id, but we need to lock for queue

        for i in range(len(self.carts[cart_id])):
            idx, cart_product = self.carts[cart_id][i]

            if cart_product == product:
                self.queues[idx].append(cart_product)
                self.carts[cart_id].pop(i)
                return True
                # self.lock_per_queue[idx].acquire()
                # if len(self.queues[idx]) >= self.queue_size_per_producer:
                #     self.lock_per_queue[idx].release()
                #     return False
                # else:
                #     self.queues[idx].append(cart_product)
                #     self.lock_per_queue[idx].release()
                #     self.carts[cart_id].pop(i)
                #     return True


        print("this is wrong in so many ways")
        return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        return [x for _, x in self.carts[cart_id]]
