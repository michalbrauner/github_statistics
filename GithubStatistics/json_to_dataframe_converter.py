from typing import List
import pandas as pd


class JsonToDataFrameConverter(object):
    @staticmethod
    def create_dataframe_item_from_json_data(json_data: dict) -> dict:
        item = {
            'url': json_data['url'],
            'id': json_data['id'],
            'number': json_data['number'],
            'state': json_data['state'],
            'title': json_data['title'],
            'user_login': json_data['user']['login'],
            'user_id': json_data['user']['id'],
            'created_at': json_data['created_at'],
            'closed_at': json_data['closed_at'],
            'merged_at': json_data['merged_at'],
        }

        return item

    @staticmethod
    def get_dataframe_columns() -> List[str]:
        return [
            'url',
            'id',
            'number',
            'state',
            'title',
            'user_login',
            'user_id',
            'created_at',
            'closed_at',
            'merged_at',
        ]

    @staticmethod
    def get_dataframe(data: List[dict]) -> pd.DataFrame:
        columns = JsonToDataFrameConverter.get_dataframe_columns()
        items = list(map(JsonToDataFrameConverter.create_dataframe_item_from_json_data, data))

        dataframe = pd.DataFrame(data=items, columns=columns)

        return dataframe
