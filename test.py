from src.applogger import get_logger
from src.specialExceptionHandling import CustException
import sys

logger = get_logger(__name__)
def test_exception_handling():
    try:
        logger.info("Starting test_exception_handling")
        a = 1 / 0
    except Exception as e:
        raise CustException("An error occurred in test_exception_handling", sys)



if __name__ == "__main__":
    try:
        test_exception_handling()
    except CustException as ce:
        logger.error(ce)

# we are in God's hands 



'''
  besmilah 



'''