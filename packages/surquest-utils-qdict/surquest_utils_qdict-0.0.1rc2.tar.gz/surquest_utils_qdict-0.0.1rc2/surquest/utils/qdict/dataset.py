from .attribute import Attribute


class Dataset:

    def __init__(self, data: list[dict]):
        self.data = data

    def __len__(self):
        return len(self.data)
    
    def count(self):
        """Method to count number of items in the dataset
        """
        return len(self.data)
    
    def count_distinct(self, *attributes):
        """Method to count number of distinct items in the dataset

        Args:
            attributes (list[str]): List of attributes to count distinct on

        Returns:
            int: Number of distinct items
        """
        distinct_data = set()
        attrs = [self.get_attribute(attr) for attr in attributes]

        for item in self.data:
            distinct_data.add(tuple([self.get_nested_value(item, attr.names) for attr in attrs]))
        
        return len(distinct_data)
    
    def select(self, *attributes) -> 'Dataset':
        """Method to select attributes from the dataset

        Args:
            attributes (list[str]): List of attributes to select

        Returns:
            Dataset: New dataset with selected attributes

        Example:

        ```python

        dataset = Dataset([
            {'id': 1, 'name': 'Charles Dickens', 'yearOfBirth': 1812, 'yearOfDeath': 1870, 'location': {'city': 'London', 'country': 'UK'}},
            {'id': 2, 'name': 'Jane Austen', 'yearOfBirth': 1775, 'yearOfDeath': 1817, 'location': {'city': 'Steventon', 'country': 'UK'}},
            {'id': 3, 'name': 'Mark Twain', 'yearOfBirth': 1835, 'yearOfDeath': 1910, 'location': {'city': 'Florida', 'country': 'USA'}},
            {'id': 4, 'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'yearOfDeath': 1961, 'location': {'city': 'Oak Park', 'country': 'USA'}},
            {'id': 5, 'name': 'F. Scott Fitzgerald', 'yearOfBirth': 1896, 'yearOfDeath': 1940, 'location': {'city': 'St. Paul', 'country': 'USA'}}
        ])
        
        # Select attributes 'name', 'yearOfBirth', 'location.city'
        out = dataset.select('name', 'yearOfBirth', 'location.city')

        # Output:
        out.show()
        # [
        #    {'name': 'Charles Dickens', 'yearOfBirth': 1812, 'location': {'city': 'London'}},
        #    {'name': 'Jane Austen', 'yearOfBirth': 1775, 'location': {'city': 'Steventon'}},
        #    {'name': 'Mark Twain', 'yearOfBirth': 1835, 'location': {'city': 'Florida'}},
        #    {'name': 'Ernest Hemingway', 'yearOfBirth': 1899, 'location': {'city': 'Oak Park'}},
        #
        # ]
        ```
        """

        selected_data = []
        for item in self.data:
            new_item = {}
            for attr in attributes:
                
                attribute = self.get_attribute(attr)

                new_item.update(self.get_nested(item, attribute))
            
            selected_data.append(new_item)
        
        return Dataset(selected_data)
    
    def filter(self, condition):
        """Method to filter dataset by condition

        Args:
            condition (function): Condition to filter

        Returns:
            Dataset: New dataset with filtered data
        """
        return Dataset([item for item in self.data if condition(item)])
    
    def join(self, other: 'Dataset', on: str|Attribute=None, how="inner", left_on=None, right_on=None):
        """Method to join two datasets

        Args:
            other (Dataset): Dataset to join
            on (str|Attribute): Attribute to join on
            how (str, optional): Type of join. Defaults to "inner".
            left_on (str|Attribute, optional): Attribute from left dataset to join on. Defaults to None.
            right_on (str|Attribute, optional): Attribute from right dataset to join on. Defaults to None.

        Returns:
            Dataset: New dataset with joined data
        """

        # Get attributes
        if left_on is None:
            left_on = on
        if right_on is None:
            right_on = on
        
        left_on = self.get_attribute(left_on)
        right_on = other.get_attribute(right_on)

        joined_data = []

        # Convert data to dictionaries with keys as values of left_on
        left_data = self.hash_key_value(self.data, left_on)
        right_data = other.hash_key_value(other.data, right_on)

        if how == "inner":
            joined_data = self.inner_join(left_data, right_data)

        elif how == "left":
            joined_data = self._left_join(left_data, right_data)

        elif how == "right":
            joined_data = self._right_join(left_data, right_data)

        return Dataset(joined_data)
    
    @staticmethod
    def hash_key_value(data: list, on: Attribute):
        """Method to hash data by key

        Args:
            data (list): List of dictionaries to hash
            on (Attribute): Attribute to hash on

        Returns:
            dict: Hashed data
        """

        hash_data = {}

        for item in data:
            key = on.get_value(item)
            if key in hash_data:
                hash_data[key].append(item)
            else:
                hash_data[key] = [item]
        
        return hash_data
    
    @staticmethod
    def inner_join(left_data, right_data):
        
        joined_data = []

        for key in left_data:
            if key in right_data:
                for left_item in left_data[key]:
                    for right_item in right_data[key]:
                        joined_data.append({**left_item, **right_item})

        return joined_data
    
    @staticmethod
    def _left_join(left_data, right_data):

        joined_data = []

        for key in left_data:
            if key in right_data:
                for left_item in left_data[key]:
                    for right_item in right_data[key]:
                        joined_data.append({**left_item, **right_item})
            else:
                for left_item in left_data[key]:
                    joined_data.append({**left_item, **{key: None for key in right_data}})

        return joined_data
    

    @staticmethod
    def _right_join(left_data, right_data):
            
        joined_data = []

        for key in right_data:
            if key in left_data:
                for right_item in right_data[key]:
                    for left_item in left_data[key]:
                        joined_data.append({**left_item, **right_item})
            else:
                for right_item in right_data[key]:
                    joined_data.append({**{key: None for key in left_data}, **right_item})
        
        return joined_data
    
    def show(self, pretty=False):
        """Method to print dataset
        """
        
        if pretty:
            import json
            print(json.dumps(self.data, indent=4, default=str))
        else:
            print(self.data)
    
    @staticmethod
    def get_attribute(attribute):
        """Method to get attribute from a string
        
        Args:
            attribute (str): Attribute to get

        Returns:
            Attribute: Attribute object
        """

        if isinstance(attribute, Attribute):
            return attribute
        
        else:
            keys = attribute.split('.')
            
            if len(keys) == 1:
                attribute = Attribute(keys[0])

            else:
                attribute = Attribute(keys[0])
                for key in keys[1:]:
                    attribute.get(key)
            
            return attribute

    @staticmethod
    def get_nested(d, attribute):
        """Method to get nested value from a dictionary

        Args:
            d (dict): Dictionary to get nested value from
            attribute Attribute: Attribute object

        Returns:
            dict: Nested value from the dictionary
        """
    
        names = attribute.names
        aliases = attribute.aliases

        nested_value = Dataset.get_nested_value(d, names)
        
        renamed_dict = nested_value
        for key, alias in zip(reversed(names), reversed(aliases)):
            renamed_dict = {alias: renamed_dict}
        
        return renamed_dict
    
    @staticmethod
    def get_nested_value(d, keys):
        """Method to get nested value from a dictionary

        Args:
            d (dict): Dictionary to get nested value from
            keys (list[str]): List of keys to get nested value from

        Returns:
            dict: Nested value from the dictionary
        """

        for idx, key in enumerate(keys):
            if idx == len(keys) - 1:
                return d.get(key)
            d = d.get(key, {})
        return d