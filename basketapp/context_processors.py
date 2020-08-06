def basket(request):
    if request.user.is_authenticated:
        basket = request.user.basket.select_related().all()
    else:
        basket = []

    return {
        'basket':basket,
    }