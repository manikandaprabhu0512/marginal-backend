import logging

logger = logging.getLogger("marginal")

print("Marginal handlers:", logger.handlers)
print("Marginal propagate:", logger.propagate)

logger.setLevel(logging.INFO)