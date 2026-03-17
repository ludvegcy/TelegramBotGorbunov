from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    gender = State()
    weight = State()
    height = State()
    age = State()
    activity = State()
    goal = State()

class FoodTrackingStates(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_weight = State()

class ReviewStates(StatesGroup):
    waiting_for_type = State()
    waiting_for_target = State()
    waiting_for_text = State()
    waiting_for_rating = State()

class WeightState(StatesGroup):
    waiting_for_weight = State()