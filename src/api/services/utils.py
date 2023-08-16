async def set_discount(dish: dict, discount: str) -> dict:
    dish['price'] = discount

    return dish


async def set_discounts(discounts: dict, dishes: list) -> list:
    for i in range(len(dishes) - 1, -1, -1):
        dish = dishes[i]
        discount = discounts.get(f'discount:{dish["id"]}')
        if discount:
            del dishes[i]
            dish['price'] = discount
            dishes.append(dish)

    return dishes
