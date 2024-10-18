from django import template

register = template.Library()

# 탬플릿에서 배열 인덱스 접근하기 위한 필터
@register.filter
def index(array, i):
    try:
        return array[i]
    except:
        return None
