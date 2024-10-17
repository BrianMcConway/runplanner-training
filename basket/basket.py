from products.models import TrainingPlan

class Basket:
    def __init__(self, request):
        """
        Initialize the basket from the session. If it doesn't exist, create an empty basket
        with an 'items' list.
        """
        self.session = request.session
        self.basket = self.session.get('basket', {'training_plans': []})  # Default to empty basket

        if 'training_plans' not in self.basket:  # Ensure 'training_plans' key exists
            self.basket['training_plans'] = []

        self.save()  # Save initial state

    def add(self, training_plan, quantity=1, price=None):
        """
        Add a training plan to the basket.
        """
        plan_id = str(training_plan.id)
        item = {
            'id': plan_id,
            'training_plan': training_plan,  # Save the full object for easier access
            'quantity': quantity,
            'price': price or training_plan.calculate_price(),
        }

        self.basket['training_plans'].append(item)
        self.save()

    def remove(self, training_plan_id):
        """
        Remove a training plan from the basket by its ID.
        """
        self.basket['training_plans'] = [item for item in self.basket['training_plans'] if item['id'] != training_plan_id]
        self.save()

    def get_total_price(self):
        """
        Calculate the total price of the basket items.
        """
        return sum(item['price'] * item['quantity'] for item in self.basket['training_plans'])

    def save(self):
        """
        Mark the session as modified to ensure it gets saved.
        """
        self.session['basket'] = self.basket
        self.session.modified = True

    def clear(self):
        """
        Clear the entire basket.
        """
        self.session['basket'] = {'training_plans': []}  # Reset the 'training_plans' list
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the basket.
        """
        for item in self.basket['training_plans']:
            yield item
