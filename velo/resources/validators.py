import onctuous


def validate_isinstance(cls):

    def validate(obj):
        if not isinstance(obj, cls):
            raise onctuous.Invalid('%s is not an instance of %s' % (obj, cls))
        return obj
    return validate
