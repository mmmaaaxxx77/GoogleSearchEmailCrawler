from mongoengine import *
import datetime

#connect('stock', host='datashop-mongo')
connect('stock', host='www.johnnyplanet.com', port=22007)


class Stock(Document):
    stock_id = StringField(required=True)
    stock_name = StringField(required=True)
    stock_type = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.now)


class ShareHolder(Document):
    stock_id = StringField(required=True)
    stock_name = StringField(required=True)
    stock_type = StringField(required=True)
    position = StringField(required=True)
    name = StringField(required=True)
    stock_count = LongField(required=True)
    stock_percentage = StringField(required=True)
    stock_update_date = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.now)


class ShareHolderRaw(Document):
    stock_id = StringField(required=True)
    stock_name = StringField(required=True)
    stock_type = StringField(required=True)
    position = StringField(required=True)
    name = StringField(required=True)
    stock_count = LongField(required=True)
    stock_percentage = StringField(required=True)
    stock_update_date = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.now)


class CollectorCount(Document):
    stock_id = StringField(required=True)
    stock_name = StringField(required=True)
    stock_type = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.now)

    data_date = LongField(required=True)
    data_count = LongField(required=True)
    data_difference_count = FloatField(required=True)
    data_data = ListField(required=True)
