class Factor:
    """Factor

The Factor class holds information about an individual Factor in
Stat-Ease 360. Instances of this class are typically created by
:func:`statease.client.SEClient.get_factor`

Attributes:
    name (str): the name of the factor

    units (str): the units of the factor

    values (tuple): the values of the factor, in run order

    low (str, **read only**): the actual low that corresponds to the *coded* low (this is usually, but not necessarily, the minimum observed value)

    high (str, **read only**): the actual high that corresponds to the *coded* high (this is usually, but not necessarily, the maximum observed value)

    coded_low (str, **read only**): the coded low value, typically -1 or 0

    coded_high (str, **read only**): the coded high value, typically 1
"""

    def __init__(self, client = None, name = ""):
        if client:
            self.GetFactorInfo(client, name)

    def GetFactorInfo(self, client, name):

        self.__client = client
        self.__name = name

        result = self.__client.send_payload({
            "method": "GET",
            "uri": "design/factor/" + self.__name,
        })

        # overwrite the user entered name with the properly capitalized one
        self.__name = result['payload'].get('name', self.name)
        self.__variable_id = result['payload'].get('variable_id',None)
        self.__units = result['payload'].get('units', '')
        self.__type = result['payload'].get('type', '')
        self.__subtype = result['payload'].get('subtype', '')
        self.__values = tuple(result['payload'].get('values', []))
        self.__coded_low = result['payload'].get('coded_low', -1)
        self.__coded_high = result['payload'].get('coded_high', 1)
        self.__actual_low = result['payload'].get('actual_low', -1)
        self.__actual_high = result['payload'].get('actual_high', 1)
        self.__is_categorical = result['payload'].get('is_categorical', None)
        self.__coded_values = tuple(result['payload'].get('coded_values', []))
        self.__is_block = result['payload'].get('is_block', None)
        self.__contrasts = tuple(result['payload'].get('contrasts', []))
        if (self.__is_categorical):
            # Convert inner nested lists to tuples for efficiency
            self.__levels = tuple(result['payload'].get('levels', []))
            self.__coded_values = tuple([ tuple(sublist) if sublist is not None else None for sublist in self.__coded_values])
        
    def GetBlockInfo(self, client):

            self.__client = client
            result = self.__client.send_payload({
                "method" : "GET",
                "uri": "design/block"
            })

            self.__name = result['payload'].get('name', self.name)
            self.__variable_id = result['payload'].get('variable_id',None)
            self.__units = result['payload'].get('units', '')
            self.__type = result['payload'].get('type', '')
            self.__subtype = result['payload'].get('subtype', '')
            self.__values = tuple(result['payload'].get('values', []))
            self.__coded_low = result['payload'].get('coded_low', -1)
            self.__coded_high = result['payload'].get('coded_high', 1)
            self.__actual_low = result['payload'].get('actual_low', -1)
            self.__actual_high = result['payload'].get('actual_high', 1)
            self.__is_categorical = result['payload'].get('is_categorical', None)
            self.__is_block = result['payload'].get('is_block', None)
            self.__coded_values = tuple(tuple(sublist) for sublist in result['payload'].get('coded_values', []))
            self.__levels = tuple(result['payload'].get('levels', []))
            self.__contrasts = tuple(result['payload'].get('contrasts', []))

    def __str__(self):
        return 'name: "{}"\nunits: "{}"\nvariable_id:"{}"\ntype: "{}" subtype: "{}"\ncoded low: {} <-> {}\ncoded high: {} <-> {}\nis_categorical: {}'.format(
            self.__name,
            self.__variable_id,
            self.__units,
            self.__type,
            self.__subtype,
            self.__actual_low,
            self.__coded_low,
            self.__actual_high,
            self.__coded_high,
            self.__is_categorical,
            self.__is_block,
            self.__levels
        )

    @property
    def name(self):
        return self.__name

    @property
    def variable_id(self):
        return self.__variable_id

    @property
    def units(self):
        return self.__units

    @property
    def type(self):
        return self.__type

    @property
    def subtype(self):
        return self.__subtype

    @property
    def coded_high(self):
        return self.__coded_high

    @property
    def coded_low(self):
        return self.__coded_low

    @property
    def low(self):
        return self.__actual_low

    @property
    def high(self):
        return self.__actual_high

    @property
    def actual_low(self):
        return self.__actual_low

    @property
    def actual_high(self):
        return self.__actual_high

    @property
    def values(self):
        """Get or set the factor values. When setting the factor values, you may use
        either a list or a dictionary. If fewer values are assigned than there are rows
        in the design, they will be filled in starting with first row. If a dictionary
        is used, it must use integers as keys, and it will fill factor values in rows
        indexed by the dictionary keys. The indices are 0-based, so the first row is
        index 0, the second index 1, and so on.

        :Example:
            >>> # sets the first 4 rows to a list of values
            >>> factor.values = [.1, .2, .3, .4]
            >>> # sets the 7th through 10th rows to specific values
            >>> factor.values = { 6: .1, 7: .2, 8: .3, 9: .4 }
            >>> # sets the 6th run to a specific value
            >>> factor.values = { 5: .8 }
        """
        return self.__values

    @values.setter
    def values(self, factor_values):
        result = self.post("set", {"factor_values": factor_values })
        self.__values = tuple(result['payload']['values'])
        self.__coded_values = tuple(result['payload']['coded_values'])
        self.__coded_high = result['payload'].get('coded_high', 1)
        self.__coded_low = result['payload'].get('coded_low', -1)
        self.__actual_low = result['payload'].get('actual_low', -1)
        self.__actual_high = result['payload'].get('actual_high', 1)

    @property
    def coded_values(self):
        """Get the coded factor values in the current coding.

        :Example:
            >>> # get a list of the coded values
            >>> xc = factor.coded_values
        """
        return self.__coded_values
    
    @property
    def is_block(self):
        return self.__is_block
    
    @property
    def levels(self):
        return self.__levels
    
    @levels.setter
    def levels(self,levels_values):
        self.post("setlevels", {"levels_values" : levels_values})
    
    @property
    def contrasts(self):
        return self.__contrasts
    
    def is_categorical(self):
      """Test for categorical factor type.

        :Example:
            >>> # get a list of the coded values
            >>> #  values if the factor is categorical
            >>> x = []
            >>> if (factor.is_categorical):
            >>>   x = factor.coded_values
            >>> else: # Factor is not categorical
            >>>   x = factor.values
        """
      return self.__is_categorical

    def post(self, endpoint, payload):
        return self.__client.send_payload({
            "method": "POST",
            "uri": "design/factor/{}/{}".format(self.__name, endpoint),
            **payload,
        })

    def set_name(self, name):
        self.__name = name

    def set_units(self, units):
        self.__units = units

    def set_low(self, low):
        self.__actual_low = low

    def set_high(self, high):
        self.__actual_high = high

    def to_dict(self):
        data = {}
        data["name"] = self.__name
        data["units"] = self.__units
        data["actual_low"] = self.__actual_low
        data["actual_high"] = self.__actual_high
        return data;
