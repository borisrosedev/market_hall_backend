from ...database.models import Tag, TagProduct
from ...database import db 

def tags_helper(product, tags):
    for tag_name in tags.split(','):
        existing_tags = db.session.execute(db.select(Tag).order_by(Tag.name)).scalars()
        for existing_tag in existing_tags:
                if existing_tag.name == tag_name :
                    tag_link = TagProduct(tag=existing_tag)
                    product.tag_links.append(tag_link)
                    product.tag_links.append(tag_link)
                    break
        else:
                tag = Tag(name=tag_name.strip())
                tag_link = TagProduct(tag=tag)
                product.tag_links.append(tag_link)