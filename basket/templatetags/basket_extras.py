from django import template

register = template.Library()

@register.filter
def calc_total_price(basket):
    training_plans_total = sum(float(plan.get('price', 0)) for plan in basket.get('training_plans', []))
    return training_plans_total
