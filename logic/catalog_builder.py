def catalog_builder(parent_id, all_categories):
    html_output = ''

    # ищем дочерние элементы (children) для текущего parent_id
    children = [c for c in all_categories if c.get('parent_id') == parent_id]
    
    if not children: #если не нашли
        return ""

    #main для корня (parent_id=NULL), sub для вложенных
    list_class = 'class="sub"' if parent_id else 'class="main"'
    html_output += f'<ul {list_class}>\n'

    # сортирую  дочерние элементы по order_index
    children.sort(key=lambda c: c.get('order_index', 0))

    for category in children:
        
        # открываем элемент списка (<li>) с ссылкой
        html_output += f'<li><a href="#{category["slug"]}">{category["category_name"]}</a>'
        
        # поиск детишек для текущей категории
        html_output += catalog_builder(category['category_id'], all_categories)
        
        # закрываем элемент списка (</li>)
        html_output += '</li>\n'

    html_output += '</ul>\n'
    
    return html_output