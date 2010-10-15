from registry import register
import numpy
    
@register('create_chart', type='sparse', quality=1.0)
def _sparse_chart(x, y):
    return []
