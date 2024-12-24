from inspect import getmembers

class MultipleMembersMatchedException(Exception)
    def __init__(self, module, matches, member):
        super().__init__(f"Multiple members found matching {member} in {module}.  Matched members were {matches}")


class NoMembersMatchedExcedption(Exception):
    def __init__(self, module, member, name):
        super().__init__(f"No members found matching member {member}{f' or name {name}' if name is not None else ''} in {module}.")

    
def at(module):
    """Returns an object with a single method named member.
    Calling member with anything, or name, will search for the
    member on the provided module by instance comparison with
    the results from inspect.getmembers.

    If the member is not found, it will be looked up by name instead.

    This is meant to replace use of bare strings in mock.patch calls,
    so that an IDE will have a much easier time finding references that
    need updated during refactorings.
    """
    class MockAt:
        @staticmethod
        def member(member, *, name=None):
            matches = (
                [name for name, value in getmembers(module) if value is member]
                if name is None
                else [candidate for candidate, _ in getmembers(module) if candidate == name]
            )

            if len(matches) == 1:
                return f"{module.__name__}.{matches[0]}"
            elif len(matches) > 1:
                raise MultipleMembersMatchedException(module, matches, member, name)
            else:
                raise NoMembersMatchedExcedption(module, member, name)

    return MockAt()