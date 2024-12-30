import pytest
from surquest.utils.qdict import Attribute, AND, OR, Dataset

DATASET = Dataset([
    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
    {'id': 3, 'name': 'Mark Twain', 'yearOfBirth': 1835, 'yearOfDeath': 1910, 'location': {'city': 'Florida', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
    {'id': 4, 'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'yearOfDeath': 1961, 'location': {'city': 'Oak Park', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
    {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
])

AUTHORS = Dataset([
    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': 1870, 'location': {'city': 'London', 'country': 'UK'}},
    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK'}},
    {'id': 3, 'name': 'Mark Twain', 'yearOfBirth': 1835, 'yearOfDeath': 1910, 'location': {'city': 'Florida', 'country': 'USA'}},
    {'id': 4, 'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'yearOfDeath': 1961, 'location': {'city': 'Oak Park', 'country': 'USA'}},
    {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA'}},
    {'id': 6, 'name': 'Harper Lee', 'yearOfBirth': 1926, 'yearOfDeath': 2016, 'location': {'city': 'Washington', 'country': 'USA'}},
])

BOOKS = Dataset([
    {'id': 1, 'title': 'A Tale of Two Cities', 'year': 1859, "author": {"id": 1}},
    {'id': 2, 'title': 'Great Expectations', 'year': 1861, "author": {"id": 1}},
    {'id': 3, 'title': 'Pride and Prejudice', 'year': 1813, "author": {"id": 2}},
    {'id': 4, 'title': 'Sense and Sensibility', 'year': 1811, "author": {"id": 2}},
    {'id': 5, 'title': 'Adventures of Huckleberry Finn', 'year': 1884, "author": {"id": 3}},
    {'id': 6, 'title': 'The Adventures of Tom Sawyer', 'year': 1876, "author": {"id": 3}},
    {'id': 7, 'title': 'The Old Man and the Sea', 'year': 1952, "author": {"id": 4}},
    {'id': 8, 'title': 'A Farewell to Arms', 'year': 1929, "author": {"id": 4}},
    {'id': 9, 'title': 'The Great Gatsby', 'year': 1925, "author": {"id": 5}},
    {'id': 10,'title': 'Tender Is the Night', 'year': 1934, "author": {"id": 5}},
    {'id': 11,'title': 'Lord of the Rings', 'year': 1954, "author": {"id": 7}},
])


class TestDataset:

    DATASET = DATASET
    AUTHORS = AUTHORS
    BOOKS = BOOKS

    def test_count(self):

        assert self.DATASET.count() == len(self.DATASET)

    @pytest.mark.parametrize(
        "selection, output",
        [
            (
                ["name", "yearOfBirth"],
                [
                    {'name': 'Charles Dickens', 'yearOfBirth': 1812},
                    {'name': 'Jane Austen', 'yearOfBirth': 1775},
                    {'name': 'Mark Twain', 'yearOfBirth': 1835},
                    {'name': 'Ernest Hemingway', 'yearOfBirth': 1899},
                    {'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896}
                ]
            ),
            (
                ["name", "yearOfBirth", "location.city"],
                [
                    {'name': 'Charles Dickens', 'yearOfBirth': 1812, 'location': {'city': 'London'}},
                    {'name': 'Jane Austen', 'yearOfBirth': 1775, 'location': {'city': 'Steventon'}},
                    {'name': 'Mark Twain', 'yearOfBirth': 1835, 'location': {'city': 'Florida'}},
                    {'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'location': {'city': 'Oak Park'}},
                    {'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'location': {'city': 'St. Paul'}}
                ]
            ),
            (
                ["name", "yearOfBirth", "location.geo.lat"],
                [
                    {'name': 'Charles Dickens', 'yearOfBirth': 1812, 'location': {'geo': {'lat': 51.5074}}},
                    {'name': 'Jane Austen', 'yearOfBirth': 1775, 'location': {'geo': {'lat': 51.5074}}},
                    {'name': 'Mark Twain', 'yearOfBirth': 1835, 'location': {'geo': {'lat': 51.5074}}},
                    {'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'location': {'geo': {'lat': 51.5074}}},
                    {'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'location': {'geo': {'lat': 51.5074}}}
                ]
            ),
            (
                ["name", "yearOfBirth", "location"],
                [
                    {'name': 'Charles Dickens', 'yearOfBirth': 1812, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'name': 'Jane Austen', 'yearOfBirth': 1775, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'name': 'Mark Twain', 'yearOfBirth': 1835, 'location': {'city': 'Florida', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'location': {'city': 'Oak Park', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                ["name", "sex"],
                [
                    {'name': 'Charles Dickens', 'sex': None},
                    {'name': 'Jane Austen', 'sex': None},
                    {'name': 'Mark Twain', 'sex': None},
                    {'name': 'Ernest Hemingway', 'sex': None},
                    {'name': 'F. Scott Fitzgerald', 'sex': None}
                ]
            ),
            (
                ["name", "location.street"],
                [
                    {'name': 'Charles Dickens', 'location': {'street': None}},
                    {'name': 'Jane Austen', 'location': {'street': None}},
                    {'name': 'Mark Twain', 'location': {'street': None}},
                    {'name': 'Ernest Hemingway', 'location': {'street': None}},
                    {'name': 'F. Scott Fitzgerald', 'location': {'street': None}}
                ]
            )
        ]
    )
    def test_select(self, selection, output):

        out = self.DATASET.select(*selection)
        assert out.data == output

    @pytest.mark.parametrize(
        "selection, output",
        [
            (
                [Attribute("name"), Attribute("yearOfBirth")],
                [
                    {
                        'name': 'Charles Dickens',
                        'yearOfBirth': 1812
                    },
                    {
                        'name': 'Jane Austen',
                        'yearOfBirth': 1775
                    },
                    {
                        'name': 'Mark Twain',
                        'yearOfBirth': 1835
                    },
                    {
                        'name': 'Ernest Hemingway',
                        'yearOfBirth': 1899
                    },
                    {
                        'name': 'F. Scott Fitzgerald',
                        'yearOfBirth': 1896
                    }
                ]
                
            )
        ]
    )
    def test_select_with_attribute(self, selection, output):

        out = self.DATASET.select(*selection)
        assert out.data == output


    def test_get_nested_value(self):

        d = {'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
        keys = ['location', 'geo', 'lat']
        assert Dataset.get_nested_value(d, keys) == 51.5074

        d = {'location': 'London'}
        keys = ['location']
        assert Dataset.get_nested_value(d, keys) == 'London'

        d = {'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
        keys = ['location', 'city']
        assert Dataset.get_nested_value(d, keys) == 'London'

        d = {'a': 1}
        keys = ()
        assert Dataset.get_nested_value(d, keys) == d

    def test_dataset_len(self):

        assert len(self.DATASET) == 5

    @pytest.mark.parametrize(
        "condition, output",
        [
            (
                Attribute("id") == 1,
                [{'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}]
            ),
            (
                Attribute("id") < 2,
                [{'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}]
            ),
            (
                Attribute("id") <= 2,
                [
                    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("id") > 4,
                [
                    {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("id") >= 5,
                [
                    {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("location.country").is_in(["UK"]),
                [
                    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("location.country").is_not_in(["USA"]),
                [
                    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("location.country") != "USA",
                [
                    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("yearOfDeath").is_none(),
                [
                    {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            ),
            (
                Attribute("yearOfDeath").is_not_none(),
                [
                    {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 3, 'name': 'Mark Twain', 'yearOfBirth': 1835, 'yearOfDeath': 1910, 'location': {'city': 'Florida', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 4, 'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'yearOfDeath': 1961, 'location': {'city': 'Oak Park', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
                    {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
                ]
            )
        ]
        )
    def test_filter(self, condition, output):

        out = self.DATASET.filter(condition)
        assert out.data == output


    def test_filter_with_helpers(self):

        out = self.DATASET.filter(AND(Attribute("id") > 1, Attribute("id") < 4)).select("id", "name")
        assert out.data == [
            {'id': 2, 'name': 'Jane Austen'},
            {'id': 3, 'name': 'Mark Twain'}
        ]

        out = self.DATASET.filter(OR(Attribute("id") > 4, Attribute("id") < 2))
        assert out.data == [
            {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': None, 'location': {'city': 'London', 'country': 'UK', 'geo': {'lat': 51.5074, 'lon': 0.1278}}},
            {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA', 'geo': {'lat': 51.5074, 'lon': 0.1278}}}
        ]

    def test_show(self):

        assert self.DATASET.show() == None
        assert self.DATASET.show(pretty=True) == None

    @pytest.mark.parametrize(
        "join_options, output",
        [
            (
                {"left_on": "id", "right_on": "author.id", "how": "inner"},
                10
            ),
            (
                {"left_on": "id", "right_on": "author.id", "how": "left"},
                11
            ),
            (
                {"left_on": "id", "right_on": "author.id", "how": "right"},
                11
            ),
            (
                {"on": "id", "right_on": "author.id", "how": "inner"},
                10
            ),
            (
                {"on": "author.id", "left_on": "id", "how": "inner"},
                10
            )

        ]
    )
    def test_join(self, join_options, output):

        options = join_options.copy()
        options["other"] = self.BOOKS
        count_of = self.AUTHORS.join(**options).count()
        assert count_of == output


    @pytest.mark.parametrize(
        "params, output",
        [
            (
                ["location.country"],
                2
            ),
            (
                ["location.country", "yearOfBirth"],
                5
            ),
            (
                [Attribute("id")],
                5
            ),
            (
                [Attribute("location.geo.lat"), Attribute("location.geo.lon")],
                1
            )
        ]
    )
    def test_count_distinct(self, params, output):

        assert self.DATASET.count_distinct(*params) == output

