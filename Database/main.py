import Dataset
import Database


if __name__ == '__main__':

    dataset = Dataset.Dataset()
    dataset.drop_unused_columns()
    dataset.convert_wind_to_degree()
    dataset.convert_humidity()
    dataset.convert_pressure()

    data = dataset.get_data()

    database = Database.Database()
    database.create_table()
    database.insert_data(data)