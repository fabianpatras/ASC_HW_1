Name: Patraș Anton-Fabian

Group: 334CB

# Assignment 1

## Main idea

This assignment is was solved only modifying:
* `marketplace.py`
* `consumer.py`
* `producer.py`

The only thing I did was to complete the methods made available by the base code.

What I did, in chronological order, was:
1) initialize the threads:
	* this actually was  a bit of a pain because of non-existent prior knowledge of `**kwargs`
2) register the producers: 
	* In marketplace there is a lock to make sure this is done atomically because registering the producer means generating an unique id for the producer
3) generate cart for the consumer:
	* this also requires a lock (a different one from the last one because registering a producer should not have to wait for generating a cart and vice versa)
	* it requires a lock because it generates also an unique cart id
4) add product to cart:
	* the marketplace searches for the desired product in all the producers queues
	* there is a lock associated with each producer queue because one consumer looking in a queue should not stop the other consumers/producers looking at/adding products in the other queues (doing so would make the algorithm almost sequential)
	* when the product is found, it is added to the respective cart, maintaining the information about from which queue was taken (is case it has to be returned)
5) remove from cart:
	* pretty straight-forward:  returing a product ignores the queue limit to avoid livelocking
6) run methods of the Producers and Consumers:
	* just iterate through what is has to do and just do it  


## Final thoughts

This assignment was easy to implement. The approach taken by me is, I think, pretty correct. It could be done without locking each producer queue individually, but that just doesn't sound right to me.

Could it have been done better? Maybe

This code solves the assignment: it checks all the requirements.

## Feedback

The code base was easy to follow and the teaching assistants answered all the questions promptly and *almost* unambiguously. Kudos for this.