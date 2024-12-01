import random
import re
import time

import scrapy

from recipe1.items import Recipe1Item


class CafoodguideSpider(scrapy.Spider):
    name = "cafoodguide"
    allowed_domains = ["food-guide.canada.ca"]
    start_urls = ["https://food-guide.canada.ca/en/recipes/"]


    def parse(self, response):
        recipe1_list = response.css("div.view-content > div > div > div> div > span")
        head_url="https://food-guide.canada.ca"
        for recipe_item in recipe1_list:
            recipe_url = recipe_item.css("a::attr(href)").extract()[0]
            full_url = head_url+recipe_url
            print("full url", full_url)
            yield scrapy.Request(full_url, callback=self.get_page_content)
        next_url = response.css("body > div.dialog-off-canvas-main-canvas > div.container > div > main > div.row > div.col-xs-12.col-sm-8.col-md-9 > div > div.views-element-container.form-group > div > nav > ul > li.pager__item.pager__item--next > a::attr(href)").extract_first()
        if next_url:
            full_next_url = self.start_urls[0]+next_url
            print("next_url: ",full_next_url)
            yield scrapy.Request(full_next_url, callback=self.parse)
        # pass

    def get_page_content(self,response):
        recipe1 = Recipe1Item()
        print("----------------------------")
        ingredients_text =''
        ingredients_list = response.css("section.block.block-ctools-block.block-entity-fieldnodefield-ingredients.clearfix > div > ul>li").getall()
        match_li_content_pattern =r'<li>(.*)<\/li>'
        sub_pattern = r'<\/?(span|sup|sub|p)>'
        sub_msoIns_pattern = r'<span\sclass\=\"msoIns\">'
        sub_CAFR_pattern =r'<span\slang\=\"FR\-CA\"\sxml\:lang\=\"FR\-CA\">'
        dict_ingredients = []
        list_ingredients = []
        for i in ingredients_list:
            match_each_li = re.match(match_li_content_pattern,i)
            if match_each_li:
                # print("find a match")
                pre_txt = match_each_li.group(1)

                sub_ingredients_text = re.sub(sub_pattern,"",pre_txt).strip()
                sub_ingredients_text0 = re.sub(sub_CAFR_pattern,"",sub_ingredients_text).strip()
                sub_ingredients_text2 = re.sub(sub_msoIns_pattern, "", sub_ingredients_text0).strip()
                list_ingredients.append(sub_ingredients_text2)
                ingredients_text += sub_ingredients_text2+";"
        for i in range(len(list_ingredients)):
            pre_dict={}
            pre_dict["order"]=i+1
            pre_dict["description"]=list_ingredients[i]
            dict_ingredients.append(pre_dict)
        fin_ingredients_text = ingredients_text[:-1]
        print("dict_ingredients\n",dict_ingredients)
        recipe1['ingredients'] = dict_ingredients
        title = response.css("#wb-cont::text").extract()[0]
        recipe1['title'] = title
        print("title:",title)
        descrip_p = response.css(" div.block.block-ctools-block.block-entity-fieldnodebody.clearfix p").getall()[0]
        descrip_txt = re.sub(sub_pattern,"",descrip_p)
        print(descrip_txt)
        recipe1['description'] = descrip_txt

        img_url = response.css("body > div.dialog-off-canvas-main-canvas > div.featured-image-wrapper > div > img::attr(src)").extract()[0]
        # print("img_url:",img_url)
        recipe1['image_url'] = img_url
        directions_div = response.css("div > section.block.block-ctools-block.block-entity-fieldnodefield-directions.clearfix > div > :first-child >li").getall()
        directions_text = ""
        dict_directions = []
        list_directions = []
        for j in directions_div:
            match_each_direc = re.match(match_li_content_pattern, j)
            if match_each_direc:
                # print("find a match")
                pre_txt = match_each_direc.group(1).strip()
                sub_direc= re.sub("<a\s.*>","",pre_txt)
                sub_direc2 = re.sub(sub_pattern, "", sub_direc).strip()
                sub_direc3 = re.sub(sub_msoIns_pattern, "", sub_direc2).strip()
                # print("sub_direc2",sub_direc2)
                list_directions.append(sub_direc3)
                directions_text+= sub_direc3+";"

        for i in range(len(list_directions)):
            pre_dict={}
            pre_dict["order"]=i+1
            pre_dict["description"]=list_directions[i]
            dict_directions.append(pre_dict)
        fin_ingredients_text = ingredients_text[:-1]
        print("dict_directions\n",dict_directions)
        fin_directions_text = directions_text[:-1]
        # print("fin_directions_text:",fin_directions_text)
        recipe1['steps']=dict_directions
                # ingredients_text = ingredients_text + sub_ingredients_text + ","
        yield recipe1
        time.sleep(random.random())
