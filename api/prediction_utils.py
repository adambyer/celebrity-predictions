

def get_prediction_points(prediction_amount: int, actual_amount: int) -> int:
    # Points range from 100 to -100.
    # Points are based on how close the prediction came to the actual amount.
    # <20% gets positive points.
    # >=20% and <=50% gets zero points.
    # >50% gets negative points.
    #
    # Examples:
    #
    # prediction_amount = 9
    # actual_amount = 10
    # points: 100 - (10 * 5) = 50
    #
    # prediction_amount = 13
    # actual_amount = 10
    # points: -((70 - 50) * 2) = -40

    if actual_amount == 0:
        return -100

    distance = abs(prediction_amount - actual_amount) / actual_amount
    distance_amount = int(round(distance * 100))

    if distance < 0.2:
        return 100 - (distance_amount * 5)
    elif distance > 0.5:
        return -((distance_amount - 50) * 2)

    return 0
