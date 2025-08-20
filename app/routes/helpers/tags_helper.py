from ...database.models import Tag, TagProduct
from ...database import db 



def is_new_product_tag(prod, tag_name):
    for p_tag in prod.tags:
        if tag_name == p_tag.name:
            return False
    return True
            


def create_new_tag_for_product(product, tag_name: str):
    tag = Tag(name=tag_name.strip())
    tag_link = TagProduct(tag=tag)
    product.tag_links.append(tag_link)


def add_tag_to_product(product, existing_tag: str):
    tag_link = TagProduct(tag=existing_tag)
    product.tag_links.append(tag_link)

def get_unexisting_tags(product, tag_name):
    existing_tags = db.session.execute(db.select(Tag).order_by(Tag.name)).scalars()
    for existing_tag in existing_tags:
        if existing_tag.name == tag_name :
            if is_new_product_tag(prod=product,tag_name=tag_name):
                add_tag_to_product(product, existing_tag=existing_tag)
            return
    create_new_tag_for_product(product, tag_name=tag_name)


def tags_helper(product, tags):
    # Get all the exitings tags
    for tag_name in tags.split(','):
        # For each user added tag , try to get it in the existings tag to use it
        get_unexisting_tags(product, tag_name=tag_name)
          
 
        