import typing as t


class JsonModel:
    def json(self, attrs: t.Set[str]) -> dict:
        data = {}
        for attr in attrs:
            value = getattr(self, attr)
            if value:
                if isinstance(value, JsonModel):
                    data[attr] = value.json()
                elif isinstance(value, list):
                    data[attr] = [
                        element if not isinstance(value, JsonModel) else element.json()
                        for element in value
                    ]
                else:
                    data[attr] = value
        return data
