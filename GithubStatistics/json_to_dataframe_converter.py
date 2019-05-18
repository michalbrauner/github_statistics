from typing import List
import pandas as pd


class JsonToDataFrameConverter(object):
    @staticmethod
    def create_dataframe_item_from_json_data(json_data: dict) -> dict:
        item = {
            'url': json_data['url'],
            'id': json_data['id'],
            'author': json_data['id'],
            'number': json_data['number'],
            'state': json_data['state'],
            'title': json_data['title'],
            'user_login': json_data['user']['login'],
            'user_id': json_data['user']['id'],
            'created_at': json_data['created_at'],
            'closed_at': json_data['closed_at'],
            'merged_at': json_data['merged_at'],
            'additions': json_data['detail_info']['additions'],
            'deletions': json_data['detail_info']['deletions'],
            'changed_files': json_data['detail_info']['changed_files'],
            'commits': json_data['detail_info']['commits'],
            'comments': json_data['detail_info']['comments'],
            'author_id': json_data['user']['id'],
            'author_login': json_data['user']['login'],
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
            'additions',
            'deletions',
            'changed_files',
            'commits',
            'comments',
            'author_id',
            'author_login',
        ]

    @staticmethod
    def get_dataframe(data: List[dict]) -> pd.DataFrame:
        columns = JsonToDataFrameConverter.get_dataframe_columns()
        items = list(map(JsonToDataFrameConverter.create_dataframe_item_from_json_data, data))

        dataframe = pd.DataFrame(data=items, columns=columns)

        index = pd.Index(dataframe['number'])
        dataframe.set_index(index, drop=False, verify_integrity=True, inplace=True)

        return dataframe
