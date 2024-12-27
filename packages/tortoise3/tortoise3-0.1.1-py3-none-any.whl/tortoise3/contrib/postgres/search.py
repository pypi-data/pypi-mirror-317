from tortoise3.pypika.enums import Comparator
from tortoise3.pypika.terms import BasicCriterion, Term

from tortoise3.contrib.postgres.functions import ToTsQuery, ToTsVector


class Comp(Comparator):  # type: ignore
    search = " @@ "


class SearchCriterion(BasicCriterion):  # type: ignore
    def __init__(self, field: Term, expr: Term):
        super().__init__(Comp.search, ToTsVector(field), ToTsQuery(expr))
