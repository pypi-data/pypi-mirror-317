import zazzle

def test_1():
    configure_logger = zazzle.ZZ_Init.configure_logger
    log = zazzle.ZZ_Logging.log

    try:
        configure_logger(function_tracking=True, function_tracking_style="curved")
        #test_print()
        log(0)
        log(1)
        log(2)
        log(3)

    except:
        log(4, f"This is a 'CRITICAL' message.")

def test_2():
    log = zazzle.ZZ_Logging.log

    try:
        #test_print()
        log(0)
        log(1)
        log(2)
        log(3)
        x = 1/0

    except:
        log(4, f"This is a 'CRITICAL' message.")

if __name__ == "__main__":
    test_1()
    test_2()
