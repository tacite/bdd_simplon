# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import scrapy
import re

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
        #item=self.clean_rncp3(item)
        item=self.clean_formacodes(item)
        item=self.clean_nsf_codes(item)
        return item
    
    #@@fonctionne pour 1 et 2 def clean_rncp(self,item):
    #     adapter=ItemAdapter(item)
    #     rncp=adapter.get("rncp")
    #     if rncp:
    #         rncp_id = rncp.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
    #         adapter['rncp'] = rncp_id
    #     else:
    #         adapter['rncp'] = None
    #     return item
    
    #fonctionne pour 3:
    def clean_rncp(self, item):
        adapter = ItemAdapter(item)
        rncp = adapter.get("rncp")
        if rncp:
            # Extraire uniquement les chiffres du rncp
            rncp_numbers = ''.join(re.findall(r'\d+', rncp))
            adapter['rncp'] = rncp_numbers if rncp_numbers else None
        else:
            adapter['rncp'] = None
        return item


    ####@@@@@ def clean_rs(self,item):
    #     adapter=ItemAdapter(item)
    #     rs=adapter.get("rs")
    #     if rs:
    #         rs_id = rs.split('/')[-2]  # Récupérer le dernier segment avant le dernier '/'
    #         adapter['rs'] = rs_id
    #     else:
    #         adapter['rs'] = None
    #     return item
    def clean_rs(self, item):
        adapter = ItemAdapter(item)
        rs = adapter.get("rs")
        if rs:
            segments = rs.split('/')
            if len(segments) > 2:
                rs_id = segments[-2]
                adapter['rs'] = rs_id
            else:
                adapter['rs'] = rs  # Ou autre comportement de secours
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

    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie:
            niveau_sortie = niveau_sortie.strip()
            adapter['niveau_sortie'] = niveau_sortie
        else:
            adapter['niveau_sortie'] = None
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
    
    # def clean_rncp3(self,item):
    #     adapter = ItemAdapter(item)
    #     rncp = adapter.get("rncp")
    #     if rncp:
    #         rncp = response.urljoin(rncp)
    #         request = scrapy.Request(rncp, callback=self.parse_france_competences)
    #         request.meta['item'] = adapter
    #         yield request
    #     else:
    #         adapter['rncp'] = None
    #         adapter['formacodes'] = None
    #         adapter['nsf_codes'] = None
    #         yield item

    def clean_formacodes(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("formacodes")
        if formacodes:
            formacodes_cleaned = [fc.replace(':', '').strip() for fc in formacodes]
            adapter['formacodes'] = ', '.join(formacodes_cleaned)
        else:
            adapter['formacodes'] = None
        return item
    
    def clean_nsf_codes(self, item):
        adapter = ItemAdapter(item)
        nsf_codes = adapter.get("nsf_codes")
        if nsf_codes:
            nsf_codes_cleaned = [nsf.replace(':', '').strip() for nsf in nsf_codes]
            adapter['nsf_codes'] = ', '.join(nsf_codes_cleaned)
        else:
            adapter['nsf_codes'] = None
        return item

