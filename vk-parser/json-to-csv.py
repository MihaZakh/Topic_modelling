import ijson
import pandas as pd


prefix_list = ['id', 'date', 'owner_id', 'text', 'likes', 'reposts', 'comments']

filenames = ['vk_data_Тюменский государственный университет ТюмГУ', 'vk_data_Тюменский государственный университет',
             'vk_data_ТюмГУ']

row_to_add = []
for name in filenames:
    with open(name + '.json', 'r', encoding='utf-8') as read_file:
        data = ijson.items(read_file, 'item')

        for obj in data:
            row = []
            for col in prefix_list:
                if col in ['likes', 'comments', 'reposts']:
                    val = obj[col]['count']
                    row.append(val)
                else:
                    val = obj[col]
                    row.append(val)
            row_to_add.append(row)

vk_posts = pd.DataFrame(data=row_to_add, columns=prefix_list)
vk_posts.to_csv('vk_posts.csv', encoding='utf-8')
