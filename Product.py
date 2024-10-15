from pydantic import BaseModel

class Product(BaseModel):
      brands_label : int
      category_label: int
      item_category_1 : bool
      item_category_2: bool
      item_category_3: bool
      item_category_4: bool
      item_category_5: bool
      shipping_by_buyer: bool
      shipping_by_seller: bool
      main_category : int
      sub_category_1 : int
      sub_category_2 : int
      name : str
      item_description : str




