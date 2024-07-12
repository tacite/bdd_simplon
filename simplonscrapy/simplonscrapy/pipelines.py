# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


# class CsvPipeline:
#     def open_spider(self, spider):
#         self.file = open('formations.csv', 'w', newline='', encoding='utf-8')
#         self.writer = csv.DictWriter(self.file, fieldnames=['title', 'rncp', 'formacodes', 'nsf_codes'])
#         self.writer.writeheader()


#     def close_spider(self, spider):
#         self.file.close()

class SimplonscrapyPipeline:
    def process_item(self, item, spider):
        item=self.clean_rncp(item)
        item=self.clean_rs(item)
        item=self.clean_formation_id(item)
        item=self.clean_niveau_sortie(item)
        item=self.clean_prix(item)

        return item
    
    def clean_rncp(self,item):
        adapter=ItemAdapter(item)
        rncp=adapter.get("rncp")
        if rncp:
            rncp_id = rncp.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
            adapter['rncp'] = rncp_id
        else:
            adapter['rncp'] = None
        return item
        

    def clean_rs(self,item):
        adapter=ItemAdapter(item)
        rs=adapter.get("rs")
        if rs:
            rs_id = rs.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
            adapter['rs'] = rs_id
        else:
            adapter['rs'] = None
        return item
        

    def clean_formation_id(self,item):
        adapter=ItemAdapter(item)
        formation_id=adapter.get("formation_id")
        if formation_id:
            formation_id = formation_id.split('/')[-1]
            adapter['formation_id'] = formation_id
        return item

    def clean_niveau_sortie(self,item):
        adapter=ItemAdapter(item)
        niveau_sortie=adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
        return item

    def clean_prix(sel,item):
        adapter = ItemAdapter(item)
        prix_min = adapter.get("prix_min")
        prix_max = adapter.get("prix_max")
        if prix_min:
            adapter['prix_min'] = ''.join(filter(str.isdigit, prix_min))
        if prix_max:
            adapter['prix_max'] = ''.join(filter(str.isdigit, prix_max))
        return item





    

