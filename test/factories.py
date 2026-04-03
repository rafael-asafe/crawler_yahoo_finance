import factory

from data_handler.models import EquitiesSchema


class EquityFactory(factory.Factory):
    class Meta:
        model = EquitiesSchema

    symbol = factory.Faker("lexify", text="????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    name = factory.Faker("company")
    price = factory.Faker("pyfloat", right_digits=2, positive=True, min_value=1.0, max_value=9999.99)