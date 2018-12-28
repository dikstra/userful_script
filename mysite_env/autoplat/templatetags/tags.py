#！/usr/bin/env.python
#coding:utf-8

from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.core.exceptions import FieldDoesNotExist

register = template.Library()

@register.simple_tag
def table_row(blogs_obj):
    row = ''
    for obj in blogs_obj:
        b='''
            <tr><td>{summary}</td><td>{user}</td><td>{time}</td></tr>
            '''.format(summary=obj.summary,user=obj.user.name,time=obj.create_time)
        row += b
    return mark_safe(row)

@register.simple_tag
def build_paginators(contacts):
    page_btns = '''<nav aria-label="Page navigation" class='pull-right'>
  <ul class="pagination">'''
    added_dot_ele = False
    if contacts.has_previous():
        page_btns += '''<li>
                        <a href="?page=%s"  aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span></a>
                        </li>'''% contacts.previous_page_number()
    for page_num in contacts.paginator.page_range:
        if page_num < 3 or page_num > contacts.paginator.num_pages - 2:#代表最前2页和最后2页
            ele_class = ""
            if contacts.number == page_num:
                ele_class = "active"
            page_btns += '''<li class='%s'><a href="?page=%s">%s</a></li>'''%(ele_class,page_num,page_num)
        elif abs(contacts.number - page_num) <=2:#判断当前页的前后2页
            ele_class = ''
            if contacts.number == page_num:
                added_dot_ele == False
                ele_class = "active"
            page_btns += '''<li class='%s'><a href="?page=%s">%s</a></li>''' % (ele_class,page_num, page_num)

        else:#其余显示...
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True
    if contacts.has_next():
        page_btns += '''<li>
                        <a href="?page=%s" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span></a>
                        </li>'''%contacts.next_page_number()
    page_btns +='''</ul>
                    </nav>'''

    return mark_safe(page_btns)

@register.simple_tag
def build_create_comment(comment_list):
    html = '<ul class="media-list">'
    for row in comment_list:
        html += '''<li class="media"><div class="media-left"><span class="glyphicon glyphicon-user"></span></div>
        <div class="media-body"><h4 class="media-heading">{username}</h4>
        <p>{comment}</p>
        <button  type="button" class="btn btn-default" id = "{id}" 
        name="comment_reply" data-toggle="modal" data-target="#exampleModal" data-comment="微博回复">回复</button>
        '''.format(username=row['user'],comment=row['content'],id=row['id'])
        if row['children']:
            html += digui(row['children'])
        html += '</div></li>'
    html += '</ul>'

    return mark_safe(html)

def digui(children_list):
    tree = ''
    for row in children_list:
        tree += '''<div class="media"><div class="media-left"><span class="glyphicon glyphicon-user"></span></div>
            <div class="media-body"><h4 class="media-heading">{username}回复:{people}</h4>
            <p>{comment}</p>
            <button  type="button" class="btn btn-default" id = "{id}" 
            name="comment_reply" data-toggle="modal" data-target="#exampleModal" data-comment="微博回复">回复</button>
            '''.format(username=row['user'],people=row['parent_name'],comment=row['content'],id=row['id'])
        if row['children']:
            tree += digui(row['children'])
        tree += '</div></div>'

    return tree