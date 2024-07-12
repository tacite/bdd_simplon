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
        item=self.clean_region(item)
        item=self.clean_start_date(item)
        item=self.clean_niveau_sortie(item)
        item=self.clean_duree(item)
        item=self.clean_type_formation(item)
        item=self.clean_lieu_formation(item)
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

    def clean_prix(self,item):
        adapter = ItemAdapter(item)
        prix_min = adapter.get("prix_min")
        prix_max = adapter.get("prix_max")
        if prix_min:
            adapter['prix_min'] = ''.join(filter(str.isdigit, prix_min))
        if prix_max:
            adapter['prix_max'] = ''.join(filter(str.isdigit, prix_max))
        return item


    def clean_region(self,item):
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        if region:
            adapter['region'] = adapter['region'].replace('\n', '').strip()
        return item
    
    
    def clean_start_date(self,item):
        adapter = ItemAdapter(item)
        start_date = adapter.get("start_date")
        if start_date:
            adapter['start_date'] = adapter['start_date'].replace('\n', '').strip()
        return item

    def clean_niveau_sortie(self,item):
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("start_date")
        if niveau_sortie:
            adapter['niveau_sortie'] = adapter['niveau_sortie'].strip().replace("Sortie :", "").strip()
        return item
    
    def clean_duree(self,item):
        adapter = ItemAdapter(item)
        duree = adapter.get("start_date")
        if duree :
            adapter['duree'] = adapter['duree'].strip()
        return item

    def clean_type_formation(self,item):
        adapter = ItemAdapter(item)
        type_formation = adapter.get("type_formation")
        if type_formation:
            adapter['type_formation'] = adapter['type_formation'].strip()
        return item
    
    def clean_lieu_formation(self,item):
        adapter = ItemAdapter(item)
        lieu_formation = adapter.get("lieu_formation")
        if lieu_formation:
             adapter['lieu_formation'] = adapter['lieu_formation'].replace('\n', '').strip()
        return item