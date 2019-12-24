# Это вспомогательный класс, созданный, чтобы выкидывать исключения в едином стиле
# Пример приминения : Exceptions.throw(Exceptions.argument_type)
class Exceptions: #static
    argument_type = "Argument type exception"
    argument = "Argument exception"
    null_argument = "Null argument exception"
    not_implemented = "Not implemented exception"
    return_type = "Unexpected type returned exception"
    invalid_operation = "Invalid operation exception"

    @staticmethod
    def throw(exception, message = None):
        if message == None:
            raise TypeError(exception + '!')
        raise TypeError("{}: {}!".format(exception, message))