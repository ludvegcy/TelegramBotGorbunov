class NutritionCalculator:
    @staticmethod
    def calculate_bmr(weight, height, age, gender):
        """Базовый обмен веществ (формула Миффлина-Сан Жеора)"""
        if gender == "male":
            return (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            return (10 * weight) + (6.25 * height) - (5 * age) - 161

    @staticmethod
    def calculate_maintenance(bmr, activity):
        """Поддержание веса"""
        activity_multipliers = {
            "minimal": 1.2,  # Сидячий образ жизни
            "light": 1.375,  # Легкая активность 1-3 раза в неделю
            "moderate": 1.55,  # Умеренная активность 3-5 раз
            "high": 1.725,  # Высокая активность 6-7 раз
            "extreme": 1.9  # Очень высокая активность/спортсмены
        }
        return bmr * activity_multipliers.get(activity, 1.2)

    @staticmethod
    def get_goal_calories(maintenance, goal):
        """Калории для цели"""
        if goal == "weight_loss":
            return maintenance * 0.85  # Дефицит 15%
        elif goal == "weight_gain":
            return maintenance * 1.15  # Профицит 15%
        else:  # maintenance
            return maintenance